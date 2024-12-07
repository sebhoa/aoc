ADD = int.__add__
MUL = int.__mul__
CONCAT = lambda a, b: int(str(a) + str(b))

class Test:

    def __init__(self, result, values):
        self.result = result
        self.values = values[::-1]

    def __str__(self):
        return f'{self.result}: {self.values}'
    
    def is_valid(self, operators):
        computations = [self.values.copy()]
        while len(computations) > 0:
            values = computations.pop()
            
            if len(values) == 1 and values[-1] == self.result:
                return True

            if len(values) > 1:
                for op in operators:
                    new_values = values.copy()
                    a = new_values.pop()
                    b = new_values.pop()
                    c = op(a, b)
                    if c <= self.result:
                        new_values.append(c)
                        computations.append(new_values)
        return False
    

class P7(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 7, part)
        self.tests = []

    def reset(self):
        self.tests = []
    
    def load(self, filename):
        self.reset()
        with open(filename) as datas:
            for line in datas:
                result, str_values = line.strip().split(':')
                self.tests.append(Test(int(result), [int(e) for e in str_values.split()]))

    def solve(self, filename):
        self.load(filename)
        operators = (ADD, MUL) if self.part == 0 else (ADD, MUL, CONCAT)
        self.solution = sum(test.result for test in self.tests if test.is_valid(operators))
        
def main():
    for part in (0, 1):
        pb = P7(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 