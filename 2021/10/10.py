import sys

FILE = 'input10.txt'
CLOSE_TO_OPEN = {'>':'<', ')':'(', '}':'{', ']':'['}
OPEN_TO_CLOSE = {'<':'>', '(':')', '{':'}', '[':']'}
CSCORE = {')':3, ']':57, '}':1197, '>':25137} # info for Corrupted line SCORE calculation
ASCORE = {')':1, ']':2, '}':3, '>':4}         # info for Autocompleted line SCORE calculation

class Subsystem:

    def __init__(self, filename):
        self.filename = filename
        self.corrupted_score = 0
        self.scores = [] # part two

    def parse(self, line):
        pile = []
        corrupted_line = False
        for delimiter in line:
            if delimiter in CLOSE_TO_OPEN:
                # délimiteur fermant lu et l'ouvrant correspondant n'est pas sur la pile
                if pile == [] or pile[-1] != CLOSE_TO_OPEN[delimiter]: 
                    corrupted_line = True
                    self.corrupted_score += CSCORE[delimiter]
                    break
                # ou alors il l'est et on dépile gentiment
                else:
                    pile.pop()
            # on a un ouvrant, on empile
            else:
                pile.append(delimiter)
        # on a fini de parser la ligne, on lance une complétion s'il y a lieu
        if not corrupted_line and pile != []:
            self.autocomplete(pile)


    def autocomplete(self, line):
        score = 0
        for delimiter in line[::-1]:
            score = score * 5 + ASCORE[OPEN_TO_CLOSE[delimiter]]
        self.scores.append(score)


    def solve(self):
        """Le même pour les 2 parties"""
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
        middle = len(logs.scores) // 2
        print(logs.scores[middle])


if __name__ == '__main__':
    main() 

