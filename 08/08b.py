"""
 0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg
 """

import sys

FILE = 'input08.txt'


LETTERS = 'abcdefg'
DIGITS = [set('abcefg'), set('cf'), set('acdeg'), set('acdfg'), set('bcdf'), 
            set('abdfg'), set('abdefg'), set('acf'), set('abcdefg'), set('abcdfg')]
COUNTS = {2:[set('cf')], 3:[set('acf')], 4:[set('bcfd')], 5:[set('acdeg'), set('acdfg'), set('abdfg')], 
          6:[set('abcefg'), set('abdefg'), set('abcdfg')], 7:[set('abcdefg')]}


class Log:

    def __init__(self, filename):
        self.filename = filename
        self.input = []
        self.output = []
        self.correspondance = {}
        self.count = {count:[] for count in COUNTS}


    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                i, o = line.strip().split('|')
                self.input.append(i.split())
                self.output.append(o.split())

    def reset(self):
        self.correspondance = {}
        self.count = {count:[] for count in COUNTS}


    def group_by(self, ten_input):
        for code in ten_input:
            self.count[len(code)].append(set(code))

    def generate_output(self, output):
        partiel = ''
        for code in output:
            decode = {self.correspondance[c].copy().pop() for c in code}
            partiel += str(DIGITS.index(decode))
        return int(partiel) 

    def set_of(self, digit):
        return self.count[len(DIGITS[digit])][0]

    def update_correspondance(self):
        s1 = self.set_of(1)
        s4 = self.set_of(4)
        s7 = self.set_of(7)
        s8 = self.set_of(8)

        self.correspondance[(s7 - s1).pop()] = DIGITS[7] - DIGITS[1] 
        c17 =  s7 & s1
        d17 =  DIGITS[1] & DIGITS[7]
        sc, sd = set(), set()
        for s in self.count[6]:
            sc = sc | (s8 - s)
        d8 = DIGITS[8]
        for n in (0, 6, 9):
            sd = sd | (d8 - DIGITS[n])
        self.correspondance[(c17 & sc).pop()] = d17 & sd
        c14 =  s4 - s1
        d14 =  DIGITS[4] - DIGITS[1]
        self.correspondance[(c14 & sc).pop()] = d14 & sd
        self.correspondance[(c17 - sc).pop()] = d17 - sd
        self.correspondance[(c14 - sc).pop()] = d14 - sd
        self.correspondance[(sc - c14 - c17).pop()] = sd - d14 - d17
        s = set()
        for k in self.correspondance:
            s = s | self.correspondance[k]
        self.correspondance[(set(LETTERS) - set(self.correspondance)).pop()] = set(LETTERS) - s

    def solve(self):
        self.load()
        total = 0
        for i, ten_input in enumerate(self.input):
            self.reset()
            self.group_by(ten_input)
            self.update_correspondance()
            total += self.generate_output(self.output[i])
        return total

def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    logs = Log(fichier)
    print(logs.solve())

if __name__ == '__main__':
    main() 
