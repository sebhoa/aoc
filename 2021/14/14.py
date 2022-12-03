import sys

FILE = 'input14.txt'
MAX_STEPS = 10

class Polymer:

    def __init__(self, filename):
        self.filename = filename
        self.rules = {}
        self.template = {}
        self.histo = {}

    def load(self):
        with open(self.filename, 'r') as datas:
            # template
            self.template = datas.readline().strip()
            
            datas.readline() # the blank line
            
            # rules
            for line in datas:
                pattern, insertion = line.strip().split(' -> ')
                self.rules[pattern] = insertion
        for car in self.template:
            self.histo[car] = self.histo.get(car, 0) + 1


    def step(self):
        """Algo naïf suffisant pour la première partie, pas la 2e"""
        tmp = ''
        for i in range(len(self.template)-1):
            double = self.template[i:i+2]
            insertion = self.rules[double]
            self.histo[insertion] = self.histo.get(insertion, 0) + 1
            tmp += double[0]+insertion
        tmp += self.template[-1]
        self.template = tmp


    def solve(self, nb_steps):
        self.load()
        # print(self.template)
        # print(self.rules)
        # print('-'*30)
        for _ in range(nb_steps):
            self.step()
        frequencies = self.histo.values()
        return max(frequencies) - min(frequencies)



def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    poly = Polymer(fichier)
    print(poly.solve(MAX_STEPS))

if __name__ == '__main__':
    main() 
