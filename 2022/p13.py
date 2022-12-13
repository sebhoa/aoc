"""
AOC 2022 -- Jour 13
S. Hoarau
"""

import sys
from functools import cmp_to_key
from puzzle import Puzzle

def cmp_int(left, right):
    """Renvoie -1 si left < right 1 si left > right et 0 sinon"""
    if left < right:
        return -1
    elif left > right:
        return 1
    else:
        return 0
        

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
        narg_1, narg_2 = len(arg_1), len(arg_2)
        for i in range(min(narg_1, narg_2)):
            answer = self.__cmp_content(arg_1[i], arg_2[i])
            if answer != 0:
                return answer
        return cmp_int(narg_1, narg_2)

    def __lt__(self, p):
        return self.__cmp_content(self.content, p.content) == -1


class P13(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 13, part)
        self.packets = []
        self.sorted_packets = []

    def load_datas(self, filename):
        with open(filename) as datas:
            for couple in datas.read().strip().split('\n\n'):
                left, right = couple.split('\n')
                self.packets.append(Packet(left))
                self.packets.append(Packet(right))

    def insert(self, divider):
        """insérer le paquet divider dans la liste self.packets triée et
        renvoie la position d'insertion
        """
        packets = self.packets
        packets.append(divider)
        i = len(packets) - 1
        while i > 0 and divider < packets[i-1]:
            packets[i] = packets[i-1]
            i -= 1
        packets[i] = divider
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
            index_1 = self.insert(Packet('[[2]]')) + 1
            index_2 = self.insert(Packet('[[6]]')) + 1
            self.solution = index_1 * index_2


# -- MAIN

def main():
    mode = 0 if len(sys.argv) < 2 else int(sys.argv[1])
    p13 = P13(mode)
    p13.test()
    print(p13)
    p13.validate()
    print(p13)

if __name__ == "__main__":
    main()