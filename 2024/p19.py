class P19(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 19, part)
        self.patterns = []
        self.towels = []
        self.memory = {}
    
    def load(self, filename):
        self.memory = {}
        self.patterns = []
        with open(filename) as datas:
            self.towels = datas.readline().strip().split(', ')
            datas.readline()
            for line in datas:
                self.patterns.append(line.strip())

    def prefix(self, s, pattern, i):
        """return True if s is prefix of word starting at index i"""
        return len(s) <= len(pattern) - i and all(s[k] == pattern[i+k] for k in range(len(s)))

    def usable_towels(self, pattern, i):
        return [towel for towel in self.towels if self.prefix(towel, pattern, i)]
    
    def count_designs(self, pattern, i):
        if (pattern, i) in self.memory:
            return self.memory[pattern, i]
        if i == len(pattern):
            return 1
        towels = self.usable_towels(pattern, i)
        n = 0
        for towel in towels:
            n += self.count_designs(pattern, i+len(towel))
        self.memory[pattern, i] = n
        return n
    
    def solve(self, filename):
        self.load(filename)
        nb_designs = [self.count_designs(pattern, 0) for pattern in self.patterns]
        if self.part == 0:
            self.solution = sum(1 for e in nb_designs if e > 0)
        else:
            self.solution = sum(nb_designs)
            

def main():
    for part in (0, 1):
        pb = P19(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 