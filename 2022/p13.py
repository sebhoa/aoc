"""
AOC 2022 -- Jour 13
S. Hoarau
"""

import sys
from puzzle import Puzzle

SMALLER = -1
GREATER = 1
EQUAL = 0

def cmp_int(a, b):
    """Renvoie SMALLER si a < b GREATER si a > b et EQUAL sinon"""
    if a < b:
        return SMALLER
    elif a > b:
        return GREATER
    else:
        return EQUAL
        

class Packet:

    def __init__(self, content):
        self.content = eval(content)

    def __cmp_content(self, arg_1, arg_2):
        """Renvoie -1 si arg_1 < arg_2, 1 si arg_1 > arg_2 et 0 sinon"""
        if isinstance(arg_1, int) and isinstance(arg_2, int):
            return cmp_int(arg_1, arg_2)
        if isinstance(arg_1, int):
            arg_1 = [arg_1]
        if isinstance(arg_2, int):
            arg_2 = [arg_2]
        # here arg_1 and arg_2 are lists
        lenght_1, lenght_2 = len(arg_1), len(arg_2)
        for i in range(min(lenght_1, lenght_2)):
            answer = self.__cmp_content(arg_1[i], arg_2[i])
            if answer != 0:
                return answer
        return cmp_int(lenght_1, lenght_2)

    def __lt__(self, packet):
        return self.__cmp_content(self.content, packet.content) == SMALLER


class P13(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 13, part)
        self.packets = []

    def load_datas(self, filename):
        with open(filename) as datas:
            for couple in datas.read().strip().split('\n\n'):
                left, right = couple.split('\n')
                self.packets.append(Packet(left))
                self.packets.append(Packet(right))

    def where_to_insert(self, divider):
        for i, packet in enumerate(self.packets):
            if divider < packet:
                return i 

    def solve(self, filename):
        self.packets = []
        self.load_datas(filename)
        if self.part == 0:
            self.solution = 0
            for i in range(0, len(self.packets), 2):
                if self.packets[i] < self.packets[i+1]:
                    self.solution += (i//2) + 1
        else:
            self.packets.sort()
            index_1 = self.where_to_insert(Packet('[[2]]')) + 1 # les positions puzzle commencent à 1 pas à 0
            index_2 = self.where_to_insert(Packet('[[6]]')) + 2 # pour tenir compte de l'insertion virtuelle de [[2]]
            self.solution = index_1 * index_2

# -- MAIN

p13one = P13(0)
p13one.test()
print(p13one)
p13one.validate()
print(p13one)

p13two = P13(1)
p13two.test()
print(p13two)
p13two.validate()
print(p13two)
