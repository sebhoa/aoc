import sys

FILE = 'input14.txt'
MAX_STEPS = 40

class Polymer:

    def __init__(self, filename):
        self.filename = filename
        self.rules = {}
        self.template = {}
        self.histo = {}

    def load(self):
        with open(self.filename, 'r') as datas:
            # template et histogramme des lettres
            template = datas.readline().strip()
            self.histo = {c:0 for c in template}
            for i in range(len(template) - 1):
                double = template[i:i+2]
                self.template[double] = self.template.get(double, 0) + 1
                self.histo[template[i]] += 1
            self.histo[template[-1]] += 1
            
            datas.readline() # the blank line
            
            # rules
            for line in datas:
                pattern, insertion = line.strip().split(' -> ')
                self.rules[pattern] = insertion


    def step(self):
        tmp = {}
        for double in self.template:
            frequency = self.template[double]
            insertion = self.rules[double]
            for new_double in (double[0]+insertion, insertion+double[1]):
                tmp[new_double] = tmp.get(new_double, 0) + frequency
            self.histo[insertion] = self.histo.get(insertion, 0) + frequency
        self.template = tmp


    def solve(self, nb_steps):
        self.load()
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
