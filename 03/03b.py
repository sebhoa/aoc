import sys

EOF = ''
FILE = 'input03.txt'

class SubMarine:

    def __init__(self):
        self.oxygen = 0
        self.co2 = 0

    def most_common(self, binaries, pos):
        """renvoie la valeur la plus commune à la position pos"""
        bits_at_pos = [bits[pos] for bits in binaries]
        bits_count = [0, 0]
        for bit in bits_at_pos:
            bits_count[int(bit)] += 1
        return 0 if bits_count[0] > bits_count[1] else 1
    
    def least_common(self, binaries, pos):
        return 1 - self.most_common(binaries, pos)

    def filtering(self, binaries, pos, criteria):
        if len(binaries) == 1:
            return binaries[0]
        else:
            bit_criteria = criteria(binaries, pos)
            new_binaries = [value for value in binaries 
                            if int(value[pos]) == bit_criteria]
            return self.filtering(new_binaries, pos+1, criteria)

    def update_rates(self, binaries):
        self.oxygen = int(self.filtering(binaries, 0, self.most_common), 2)
        self.co2 = int(self.filtering(binaries, 0, self.least_common), 2)
    
    def life_support(self):
        return self.oxygen * self.co2


class Diagnostic:

    def __init__(self, filename=FILE):
        self.filename = filename
        self.numbits = 0
        self.sub = SubMarine()

    def all_binaries(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            binaries = [line.strip() for line in datas]
            self.numbits = len(binaries[0])
            return binaries

    def solve(self):
        binaries = self.all_binaries()
        self.sub.update_rates(binaries) 
        return self.sub.life_support()


def main():
    if len(sys.argv) > 1:
        log = Diagnostic(sys.argv[1])
    else:
        log = Diagnostic()
    print(log.solve())
    
if __name__ == '__main__':
    main()