import sys

FILE = 'input06.txt'
NB_DAYS = 80
NB_DAYS_TEST = 18

class Population:

    def __init__(self, filename):
        self.filename = filename
        self.fishes = []

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            self.fishes = [int(e) for e in datas.readline().strip().split(',')]

    def one_step(self):
        n = len(self.fishes)
        for i in range(n):
            if self.fishes[i] == 0:
                self.fishes[i] = 6
                self.fishes.append(8)
            else:
                self.fishes[i] -= 1

    def solve(self, nb):
        self.load()
        for i in range(nb):
            # print(f'day {i:2} : {self.fishes}')
            self.one_step()
        return len(self.fishes)

def main():
    if len(sys.argv) > 2:
        fichier = sys.argv[1]
        nb_days = int(sys.argv[2])
    elif len(sys.argv) > 1:
        fichier = sys.argv[1]
        nb_days = NB_DAYS_TEST
    else:
        fichier = FILE
        nb_days = NB_DAYS_TEST
    lantern = Population(fichier)
    print(lantern.solve(nb_days))

if __name__ == '__main__':
    main() 
