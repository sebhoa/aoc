class P2(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 2, part)
        self.reports = []

    def reset(self):
        self.reports = []
    
    def load(self, filename):
        self.reset()
        with open(filename) as datas:
            for line in datas:
                self.reports.append([int(e) for e in line.split()])

    def sens(self, a, b):
        return 1 if b > a else -1
    
    def safe(self, levels):
        ref = self.sens(levels[0], levels[1])
        for i in range(len(levels)-1):
            dif = abs(levels[i+1] - levels[i])
            sens = self.sens(levels[i], levels[i+1])
            if sens != ref or dif > 3 or dif < 1:
                    return False, i
        return True, None
    
    def solve(self, filename):
        self.load(filename)
        self.solution = 0
        if self.part == 0:
            for levels in self.reports:
                safe, _ = self.safe(levels)
                if safe:
                    self.solution += 1
        else:
            for levels in self.reports:
                safe, ind = self.safe(levels)
                if safe:
                    self.solution += 1
                else:
                    safe, _ = self.safe(levels[1:])
                    if safe:
                        self.solution += 1
                    else:
                        safe, _ = self.safe(levels[:ind]+levels[ind+1:])
                        if safe:
                            self.solution += 1
                        else:
                            safe, _ = self.safe(levels[:ind+1]+levels[ind+2:])
                            if safe:
                                self.solution += 1

def main():
    for part in (0, 1):
        pb = P2(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 