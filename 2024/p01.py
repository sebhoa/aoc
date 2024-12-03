from puzzle import Puzzle

class P1(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 1, part)
        self.left = None
        self.right = None

    def reset(self):
        if self.part == 0:
            self.left = []
            self.right = []
        else:
            self.left = {}
            self.right = {}
        
    def load(self, filename):
        self.reset()
        with open(filename) as datas:
            if self.part == 0:
                for line in datas:
                    left, right = line.split()
                    self.left.append(int(left))
                    self.right.append(int(right))
            else:
                for line in datas:
                    left, right = [int(e) for e in line.split()]
                    self.left[left] = self.left.get(left, 0) + 1
                    self.right[right] = self.right.get(right, 0) + 1

    def solve(self, filename):
        self.load(filename)
        if self.part == 0:
            self.left.sort()
            self.right.sort()
            n = len(self.left)
            self.solution = sum(abs(self.left[i] - self.right[i]) for i in range(n))
        else:
            self.solution = 0
            for k, n in self.left.items():
                self.solution += n * k * self.right.get(k, 0)


def main():
    for part in (0, 1):
        pb = P1(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 