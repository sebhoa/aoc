import sys

FILE = 'input07.txt'

class Crab:

    def __init__(self, filename):
        self.filename = filename
        self.positions = {}
        self.count = 0

    def load(self):
        with open(self.filename, 'r') as datas:
            for e in datas.readline().strip().split(','):
                e = int(e)
                self.positions[e] = self.positions.get(e, 0) + 1
                self.count += 1
    
    def average(self):
        return sum(coef * val for coef, val in self.positions.items()) / self.count


    def fuel(self, pos_ref):
        total = 0
        for pos, nb_crabs in self.positions.items():
            cons = abs(pos_ref - pos)
            cons = (cons * (cons + 1)) // 2
            total += cons * nb_crabs
        return total
                    
    def solve(self):
        self.load()
        pos1 = int(self.average())
        pos2 = pos1 + 1
        return min(self.fuel(pos1), self.fuel(pos2))


def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    crab = Crab(fichier)
    print(crab.solve())

if __name__ == '__main__':
    main()   
