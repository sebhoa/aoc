import sys

EOF = ''
FILE = 'input03.txt'

class SubMarine:

    def __init__(self):
        self.gamma_rate = 0
        self.epsilon_rate = 0

    def most_common(self, binaries, pos):
        """renvoie la valeur (0 ou 1) la plus commune à la position pos"""
        bits_at_pos = [bits[pos] for bits in binaries]
        bits_count = [0, 0]
        for bit in bits_at_pos:
            bits_count[int(bit)] += 1
        return 0 if bits_count[0] > bits_count[1] else 1

    def filtering(self, binaries, numbits):
        return ''.join([str(self.most_common(binaries, pos)) for pos in range(numbits)])

    def not_bit(self, n, numbits):
        return (1 << numbits) - 1 - n

    def update_rates(self, binaries, numbits):
        self.gamma_rate = int(self.filtering(binaries, numbits), 2)
        self.epsilon_rate = self.not_bit(self.gamma_rate, numbits)

    def power_consumption(self):
        return self.gamma_rate * self.epsilon_rate


class Diagnostic:

    def __init__(self, filename=FILE):
        self.filename = filename
        self.sub = SubMarine()

    def all_binaries(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            binaries = [line.strip() for line in datas]
            numbits = len(binaries[0])
            return binaries, numbits

    def solve(self):
        binaries, numbits = self.all_binaries()
        self.sub.update_rates(binaries, numbits) 
        return self.sub.power_consumption()

def main():
    if len(sys.argv) > 1:
        log = Diagnostic(sys.argv[1])
    else:
        log = Diagnostic()
    print(log.solve())

if __name__ == '__main__':
    main()