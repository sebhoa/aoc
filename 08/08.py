import sys

FILE = 'input08.txt'
COUNTS = {2:{1}, 3:{7}, 4:{4}, 5:{2, 3, 5}, 6:{0, 6, 9}, 7:{8}}


class Log:

    def __init__(self, filename):
        self.filename = filename
        self.input = []
        self.output = []

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                i, o = line.strip().split('|')
                self.input.append(i.split())
                self.output.append(o.split())

    def solve(self):
        self.load()
        nb_easy_digits = 0
        for out in self.output:
            nb_easy_digits += sum(len(COUNTS[len(code)]) == 1 for code in out)
        return nb_easy_digits


def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    logs = Log(fichier)
    print(logs.solve())

if __name__ == '__main__':
    main() 
