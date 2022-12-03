import sys

FILE = 'input07.txt'

class Crab:

    def __init__(self, filename):
        self.filename = filename
        self.positions = []

    def load(self):
        with open(self.filename, 'r') as datas:
            self.positions = sorted(int(e) for e in datas.readline().strip().split(','))

    def solve(self):
        self.load()
        mediane = self.positions[len(self.positions) // 2]
        return sum(abs(valeur - mediane) for valeur in self.positions)

def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    crab = Crab(fichier)
    print(crab.solve())

if __name__ == '__main__':
    main()   
