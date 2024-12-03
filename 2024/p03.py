import re

class P3(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 3, part)
        self.memory = []

    def reset(self):
        self.memory = []
    
    def load(self, filename):
        self.reset()
        with open(filename) as datas:
            for line in datas:
                self.memory.append(re.findall(r"mul\(\d+,\d+\)|do\(\)|don't\(\)", line))

    def solve(self, filename):
        self.load(filename)
        self.solution = 0
        do = True
        for data in self.memory:
            for op in data:
                if op == "don't()":
                    do = False
                elif op == "do()":
                    do = True
                elif do or self.part == 0:
                    a, b = [int(e) for e in re.findall(r"\d+", op)]
                    self.solution += a * b

def main():
    for part in (0, 1):
        pb = P3(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 