import sys

FILE = 'input10.txt'
OPEN = {'>':'<', ')':'(', '}':'{', ']':'['}
CLOSE = {'<':'>', '(':')', '{':'}', '[':']'}
CSCORE = {')':3, ']':57, '}':1197, '>':25137}
ASCORE = {')':1, ']':2, '}':3, '>':4}

class Subsystem:

    def __init__(self, filename):
        self.filename = filename
        self.corrupted_score = 0
        self.scores = [] # part two

    def parse(self, line):
        pile = []
        corrupted_line = False
        for c in line:
            if c in OPEN:
                if pile == [] or pile[-1] != OPEN[c]:
                    corrupted_line = True
                    self.corrupted_score += CSCORE[c]
                    break
                else:
                    pile.pop()
            else:
                pile.append(c)
        if not corrupted_line and pile != []:
            self.autocomplete(pile)


    def autocomplete(self, line):
        score = 0
        for c in line[::-1]:
            score = score * 5 + ASCORE[CLOSE[c]]
        self.scores.append(score)



    def solve(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                self.parse(line.strip())


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    logs = Subsystem(fichier)
    logs.solve()
    if version == '1':
        print(logs.corrupted_score)
    else:
        logs.scores.sort()
        print(logs.scores)
        n = len(logs.scores)
        print(logs.scores[n//2])


if __name__ == '__main__':
    main() 

