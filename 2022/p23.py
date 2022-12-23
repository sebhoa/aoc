"""
AOC 2022 -- Jour 23
S. Hoarau
"""

from puzzle import Puzzle

ELF = '#'
SPACE = '.'

N = -1, 0
NE = -1, 1
E = 0, 1
SE = 1, 1
S = 1, 0
SW = 1, -1
W = 0, -1
NW = -1, -1

DIRECTIONS = N, S, W, E, NW, NE, SW, SE
ORTHOGONALS = N, S, W, E
THREE = {N: (NW, N, NE), S: (SW, S, SE), E: (NE, E, SE), W: (NW, W, SW)}

class Map:
    """Regroupe l'information sur les positions des elves"""

    def __init__(self, map_informations):
        self.elves = {(i, j) for i, line in enumerate(map_informations) 
                                for j, info in enumerate(line.strip()) if info == ELF}

    def __str__(self):
        s = ''
        for i in range(self.min_i(), self.max_i() + 1):
            for j in range(self.min_j(), self.max_j() + 1):
                s += SPACE if self.free(i, j) else ELF
            s += '\n'
        return s

    def free(self, i, j):
        return (i, j) not in self.elves

    def free_around(self, i, j):
        return all(self.free(i+di, j+dj) for di, dj in DIRECTIONS)

    def min_i(self):
        return min(i for i, _ in self.elves)

    def max_i(self):
        return max(i for i, _ in self.elves)

    def min_j(self):
        return min(j for _, j in self.elves)

    def max_j(self):
        return max(j for _, j in self.elves)

    def area(self):
        return (self.max_i() - self.min_i() + 1) * (self.max_j() - self.min_j() + 1)

    def new_position(self, i, j, direction):
        di, dj = direction
        return i + di, j + dj

    def update_position(self, old_position, new_position):
        self.elves.discard(old_position)
        self.elves.add(new_position)


class P23(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 23, part)
        self.map = None
        self.first_id = 0

    def load_datas(self, filename):
        with open(filename) as datas:
            informations = datas.readlines()
        self.map = Map(informations)
        self.first_id = 0

    # -- Elves movements
    def proposes(self):
        proposals = {}
        count_proposals = {}
        for i, j in self.map.elves:
            if not self.map.free_around(i, j):
                nb_tries = 0
                direction_id = self.first_id
                while nb_tries < 4 and not all(self.map.free(i+di, j+dj) for di, dj in THREE[ORTHOGONALS[direction_id]]):
                    nb_tries += 1
                    direction_id = (direction_id + 1) % 4
                if nb_tries < 4:
                    new_i, new_j = self.map.new_position(i, j, ORTHOGONALS[direction_id])
                    proposals[i, j] = (new_i, new_j)
                    count_proposals[new_i, new_j] = count_proposals.get((new_i, new_j), 0) + 1
        return proposals, count_proposals

    def update_positions(self, proposals, count_proposals):
        at_least_one_move = False
        for old, new in proposals.items():
            if count_proposals[new] == 1:
                self.map.update_position(old, new)
                at_least_one_move = True
        return at_least_one_move


    def solve(self, filename, *args):
        if len(args) > 0:
            filename = args[0]
        self.load_datas(filename)
        if self.part == 0:
            for _ in range(10):
                proposals, count_proposals = self.proposes()
                self.update_positions(proposals, count_proposals)  
                self.first_id = (self.first_id + 1) % 4          
            self.solution = self.map.area() - len(self.map.elves) 
        else:
            nb_rounds = 0
            at_least_one_move = True
            while at_least_one_move:
                proposals, count_proposals = self.proposes()
                at_least_one_move = self.update_positions(proposals, count_proposals)
                nb_rounds += 1  
                self.first_id = (self.first_id + 1) % 4          
            self.solution = nb_rounds



# -- MAIN

p_one = P23(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P23(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

