"""
AOC 2022 -- Jour 21
S. Hoarau
"""

import re
from puzzle import Puzzle

MATHS_OP = {'+': int.__add__, '-': int.__sub__, '*': int.__mul__, '/': int.__floordiv__}
MATHS_RES = {'+': int.__sub__, '-': int.__add__, '*': int.__floordiv__, '/': int.__mul__}

class Expression:
    """Arbre binaire modélisant l'expression arithmétique d'un singe et ses potes : ceux dont il attend un nombre"""

    def __init__(self, monkey_name=None, math_info=None, left=None, right=None):
        self.monkey_name = monkey_name
        self.math_info = math_info # un entier ou une opération parmi +, -, *, /
        if monkey_name is not None:
            self.left = Expression() if not isinstance(left, Expression) else left
            self.right = Expression() if not isinstance(left, Expression) else right

    def aff(self, tab=0):
        if not self.is_empty():
            print(' '*tab + f'BinTree({self.monkey_name}, {self.math_info}', end='')
            if self.is_leaf():
                print(')')
            else:
                print()
                self.left.aff(tab+3)
                self.right.aff(tab+3)
                print(' '*tab + ')')

    def is_empty(self):
        return self.monkey_name is None

    def is_leaf(self):
        return self.left.is_empty() and self.right.is_empty()

    def contains(self, name):
        if self.is_empty():
            return False
        elif self.monkey_name == name:
            return True
        else:
            return self.left.contains(name) or self.right.contains(name)

    # -- Les 2 principales méthodes
    # --
    def eval(self):
        """évalue l'arbre syntaxique ne contenant pas de variable ('humn') """
        if self.is_leaf():
            return int(self.math_info)
        else:
            return MATHS_OP[self.math_info](self.left.eval(), self.right.eval())
    
    def simplify(self, b):
        """Pour résoudre une équation ax = b, ou a + x = b, ou ..."""
        # cas x = b
        if self.monkey_name == 'humn':
            return b

        # cas où x est à gauche (x * a = b, x/a = b, x + a = b, x - a = b)
        elif self.left.contains('humn'):
            a = self.right.eval()
            return self.left.simplify(MATHS_RES[self.math_info](b, a))
        
        # cas où x est à droite (ça change pour / et - par ex. a / x = b -> x = a / b)
        else:
            a = self.left.eval()
            if self.math_info in '-/':
                return self.right.simplify(MATHS_OP[self.math_info](a, b))
            else:
                return self.right.simplify(MATHS_RES[self.math_info](b, a))




class P21(Puzzle):

    PATTERN_OP = re.compile(r'(\w{4}): (\w{4}) (\+|\-|\/|\*) (\w{4})')
    PATTERN_INT = re.compile(r'(\w{4}): (\d+)')

    def __init__(self, part):
        Puzzle.__init__(self, 21, part)
        self.trees = {}

    def aff(self):
        self.trees['root'].aff()

    def load_datas(self, filename):
        standby_monkeys = []
        with open(filename) as datas:
            for line in datas:
                infos = P21.PATTERN_OP.findall(line.strip())
                if len(infos) > 0:
                    root, left, op, right = infos[0]
                    if left in self.trees and right in self.trees:
                        self.trees[root] = Expression(root, op, self.trees[left], self.trees[right])
                    else:
                        standby_monkeys.append((root, left, op, right))
                else:
                    root, integer = P21.PATTERN_INT.findall(line.strip())[0] 
                    self.trees[root] = Expression(root, integer)
        standby_monkeys.sort(key=lambda e: int(e[1] in self.trees) +  int(e[3] in self.trees))
        while len(standby_monkeys) > 0:
            root, left, op, right = standby_monkeys.pop()
            self.trees[root] = Expression(root, op, self.trees[left], self.trees[right])
            standby_monkeys.sort(key=lambda e: int(e[1] in self.trees) +  int(e[3] in self.trees))

    def main_tree(self):
        return self.trees['root']

    def solve(self, filename, *args):
        if len(args) > 0:
            filename = args[0]
        self.load_datas(filename)
        if self.part == 0:
            self.solution = self.main_tree().eval()
        else:
            main = self.main_tree()
            if main.left.contains('humn'):
                self.solution = main.left.simplify(main.right.eval())
            else:
                self.solution = main.right.simplify(main.left.eval())







# -- MAIN

# p_one = P21(0)

# p_one.test()
# print(p_one)
# p_one.validate()
# print(p_one)

p_two = P21(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

