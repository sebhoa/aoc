"""
AOC 2022 -- Jour 25
S. Hoarau
"""

from puzzle import Puzzle

class Snafu:

    TO_INT = {'2': 2, '1': 1, '0': 0, '-': -1, '=': -2}
    FROM_INT = {value: key for key, value in TO_INT.items()}

    @classmethod
    def from_int(cls, n):
        if n == 0:
            return '0'
        else:
            s = ''
            while n > 0:
                n, r = divmod(n, 5)
                if r > 2:
                    r -= 5
                    n += 1
                s += Snafu.FROM_INT[r]
            return s[::-1] 
            
    def __init__(self, value):
        self.value = value if isinstance(value, str) else Snafu.from_int(value)

    def __repr__(self):
        return self.value

    def int(self):
        nb_digits = len(self.value)
        return sum(Snafu.TO_INT[d] * 5**(nb_digits - i - 1) for i, d in enumerate(self.value))

class P25(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 25, part)

    def solve(self, filename, *args):
        if len(args) > 0:
            filename = args[0]
        #self.load_datas(filename)
        if self.part == 0:
            s = 0
            with open(filename) as datas:
                for data in datas:
                    s += Snafu(data.strip()).int()
            self.solution = Snafu(s)
        else:
            pass


# -- MAIN

p_one = P25(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

# p_two = P25(1)
# p_two.test()
# print(p_two)
# p_two.validate()
# print(p_two)

