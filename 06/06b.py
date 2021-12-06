import sys

FILE = 'input06.txt'
NB_DAYS = 80
NB_DAYS_TEST = 18

class Population:

    def __init__(self, filename):
        self.filename = filename
        self.fishes = [0] * 10

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for e in datas.readline().strip().split(','):
                self.fishes[int(e)] += 1

    def one_step(self):
        """on fait une permutation circulaire des valeurs de self.fishes
        entre les indices 0 et 8, l'indice 9 servant de tampon"""
        n = len(self.fishes)
        self.fishes[9] = self.fishes[0] # on mémorise dans un tampon 
        for i in range(n-1):
            self.fishes[i] = self.fishes[i+1]
        self.fishes[6] += self.fishes[9]

    def solve(self, nb):
        self.load()
        for _ in range(nb):
            self.one_step()
        return sum(self.fishes) - self.fishes[-1]

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
