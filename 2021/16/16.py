import sys
import functools

FILE = 'input16.txt'
HEX_TO_DEC = {digit:decimal for decimal, digit in enumerate('0123456789ABCDEF')}
SEUIL = 7

class Packet:

    LITERAL = 4
    MODE_15_BITS = '0'
    MODE_11_BITS = '1'

    def __init__(self, all_bits, begin=0):
        self.begin = begin
        self.all_bits = all_bits
        self.bits = ''
        self.version = int(all_bits[begin:begin+3], 2)
        self.type_id = int(all_bits[begin+3:begin+6], 2)

    def __len__(self):
        return len(self.bits)


class Literal(Packet):

    def __init__(self, *args):
        Packet.__init__(self, *args)

    def parse(self):
        """Parcours l'entrée binaire et récupère les bits
        de ce paquet"""
        i = self.begin+6
        end = False
        while not end:
            end = self.all_bits[i] == '0'
            self.bits += self.all_bits[i+1:i+5]
            i += 5
        return i

    def eval(self):
        return int(self.bits, 2)

    def cumul_version(self):
        return self.version


class Operator(Packet):

    SUM = sum
    MUL = lambda t: functools.reduce(lambda x,y: x*y, t, 1)
    MIN = min
    MAX = max
    GREATER = lambda t: 1 if t[0] > t[1] else 0
    LESSER = lambda t: 1 if t[0] < t[1] else 0
    EQUAL = lambda t: 1 if t[0] == t[1] else 0

    OP = [SUM, MUL, MIN, MAX, None, GREATER, LESSER, EQUAL]

    def __init__(self, *args):
        Packet.__init__(self, *args)
        self.sub_packets = []
    
    def cumul_version(self):
        return self.version + sum(p.cumul_version() for p in self.sub_packets)

    def eval(self):
        return Operator.OP[self.type_id]([sp.eval() for sp in self.sub_packets])


class Operator15(Operator):

    def __init__(self, *args):
        Operator.__init__(self, *args)
        self.length = int(self.all_bits[self.begin+7:self.begin+22], 2)
        self.bits = self.all_bits[self.begin+22:self.begin+22+self.length]

    def parse(self):
        i = self.begin + 22
        while i < self.begin + 22 + self.length:
            type_id = int(self.all_bits[i+3:i+6], 2)
            if type_id == Packet.LITERAL:
                packet = Literal(self.all_bits, i)
            else:
                mode = self.all_bits[i+6]
                if mode == Packet.MODE_15_BITS:
                    packet = Operator15(self.all_bits, i)
                else:
                    packet = Operator11(self.all_bits, i)
            i = packet.parse()
            self.sub_packets.append(packet)
        return i
    

class Operator11(Operator):

    def __init__(self, *args):
        Operator.__init__(self, *args)
        self.length = int(self.all_bits[self.begin+7:self.begin+18], 2)
        self.bits = ''
    
    def parse(self):
        i = self.begin + 18
        for k in range(self.length):
            type_id = int(self.all_bits[i+3:i+6], 2)
            if type_id == Packet.LITERAL:
                packet = Literal(self.all_bits, i)
            else:
                mode = self.all_bits[i+6]
                if mode == Packet.MODE_15_BITS:
                    packet = Operator15(self.all_bits, i)
                else:
                    packet = Operator11(self.all_bits, i)
            i = packet.parse()
            self.sub_packets.append(packet)
        self.bits = self.all_bits[self.begin:i]
        return i
    

class Transmission:

    @classmethod
    def hex_to_bin(self, digit):
        return f'{bin(HEX_TO_DEC[digit])[2:]:>04}'

    def __init__(self, filename):
        self.filename = filename
        self.hexa = ''
        self.bits = ''
        self.packet = None

    def load(self):
        with open(self.filename, 'r') as datas:
            self.hexa = datas.readline().strip()

    def parse(self):
        if self.hexa == '':
            self.load()
        self.bits = ''.join([Transmission.hex_to_bin(d) for d in self.hexa])
        type_packet = int(self.bits[3:6], 2)
        if type_packet == Packet.LITERAL:
            self.packet = Literal(self.bits)
        else:
            mode = self.bits[6]
            if mode == Packet.MODE_15_BITS:
                self.packet = Operator15(self.bits)
            else:
                self.packet = Operator11(self.bits)
        self.packet.parse()

    def solve(self):
        self.load()
        self.parse()
        return self.packet.cumul_version()

    def solve_two(self):
        self.load()
        self.parse()
        return self.packet.eval()

def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    transmission = Transmission(fichier)
    if version == '1':
        print(transmission.solve())
    else:
        print(transmission.solve_two())

if __name__ == '__main__':
    main() 