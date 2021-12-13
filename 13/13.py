import sys

FILE = 'input13.txt'
FOLD = 'fold'
FOLD_SEP = '='

DOT = '#'
EMPTY = '.'

ANSWER2 = 'UCLZRAZU'

class Paper:

    def __init__(self, filename):
        self.filename = filename
        self.dots = set()
        self.width = 0
        self.height = 0
        self.folds = []


    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                if line == '\n':
                    pass
                elif line.startswith(FOLD):
                    msg, value = line.strip().split(FOLD_SEP)
                    x_or_y = msg[-1]
                    self.folds.append((x_or_y, int(value)))
                else:
                    x, y = [int(e) for e in line.strip().split(',')]
                    self.dots.add((x,y))
                    if x > self.width:
                        self.width = x
                    if y > self.height:
                        self.height = y

            self.width += 1
            self.height += 1


    def hfold(self, y):
        for x in range(self.width):
            for dy in range(1, y+1):
                point = (x, y+dy)
                symetric = (x, y-dy)
                if point in self.dots:
                    self.dots.discard(point)
                    self.dots.add(symetric)
        self.height = y

    def vfold(self, x):
        for y in range(self.height):
            for dx in range(1, x+1):
                point = (x+dx, y)
                symetric = (x-dx, y)
                if point in self.dots:
                    self.dots.discard(point)
                    self.dots.add(symetric)
        self.width = x

    def apply_folds(self, nb=None):
        if nb is None:
            nb = len(self.folds)
        for i in range(nb):
            direction, value = self.folds[i]
            if direction == 'y':
                self.hfold(value)
                self.heigth = value
            else:
                self.vfold(value)
                self.width = value

    
    def sizes(self):
        return self.width, self.height


    def __str__(self):
        s = ''
        for y in range(self.height):
            for x in range(self.width):
                s += DOT if (x,y) in self.dots else EMPTY
            s += '\n'
        return s


    def solve(self, nb=None):
        self.load()
        self.apply_folds(nb)


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    paper = Paper(fichier)
    if version == '1':
        paper.solve(1)
        print(len(paper.dots))
    else:
        paper.solve()
        print(paper)

if __name__ == '__main__':
    main() 

