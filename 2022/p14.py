"""
AOC 2022 -- Jour 14
S. Hoarau
"""

from puzzle import Puzzle

DOWN = 0, 1
LEFT = -1, 1
RIGHT = 1, 1

AIR = '.'
ROCK = '#'
SAND = 'o'
START = '+'
START_POINT = 500, 0

INF = float('inf')

DIRECTIONS = DOWN, LEFT, RIGHT

class Unit:

    def __init__(self,puzzle):
        self.puzzle = puzzle
        self.position = START_POINT
        self.lost = False
        self.blocked = False

    def fall(self):
        while not self.lost and not self.blocked:
            i, j = self.position
            #print(self.position)
            for di, dj in DIRECTIONS:
                new_position = i+di, j+dj
                if self.puzzle.is_air(new_position):
                    self.position = new_position
                    break
            if not self.puzzle.inside(self.position):
                self.lost = True
            elif self.puzzle.is_structure(new_position):
                self.blocked = True
            

class P14(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 14, part)
        self.grid = {}
        self.segments = []
        self.min_i = None
        self.max_i = None
        self.min_j = 0
        self.max_j = None
        self.units = 0
        self.end = False

    def aff_grid(self):
        max_j = max(pos[1] for pos in self.grid)
        min_i = min(k[0] for k in self.grid)
        max_i = max(k[0] for k in self.grid)
        for j in range(max_j+1):
            for i in range(min_i, max_i+1):
                print(self.grid.get((i, j), AIR), end=' ')
            print()

    def load_datas(self, filename):
        with open(filename) as datas:
            groups_of_segments = datas.readlines()
            #min_j, max_j = INF, -INF
            for group in groups_of_segments:
                self.segments.append([tuple(int(x) for x in e.split(','))  for e in group.strip().split(' -> ')])
            self.set_grid()

    def line_of_rocks(self, dep, arr):
        i1, j1 = dep
        i2, j2 = arr
        self.grid[i2, j2] = ROCK
        di = 0 if i1 == i2 else -1 if i1 > i2 else 1
        dj = 0 if j1 == j2 else -1 if j1 > j2 else 1
        while (i1, j1) != (i2, j2):
            self.grid[i1, j1] = ROCK
            i1, j1 = i1+di, j1+dj

    def set_grid(self):
        self.grid[START_POINT] = START
        for segment in self.segments:
            point_A = segment[0]
            for k in range(1, len(segment)):
                point_B = segment[k]
                self.line_of_rocks(point_A, point_B)
                point_A = point_B
        self.min_i = min(k[0] for k in self.grid)
        self.max_i = max(k[0] for k in self.grid)
        self.max_j = max(k[1] for k in self.grid)

    def inside(self, position):
        i, j = position
        return self.part == 1 or self.min_i < i < self.max_i and 0 <= j < self.max_j

    def is_air(self, position):
        return position not in self.grid 

    def is_structure(self, position):
        return position[1] == self.max_j + 2 or self.grid.get(position, AIR) in (ROCK, SAND) 

    def reset(self):
        self.grid = {}
        self.segments = []
        self.units = 0
        self.end = False

    def fill(self):
        while not self.end:
            unit = Unit(self)
            unit.fall()
            if unit.lost:
                self.end = True
            elif unit.position == START_POINT:
                self.end = True
                self.grid[unit.position] = SAND
                self.units += 1
            elif unit.position[1] == self.max_j + 2:
                self.grid[unit.position] = ROCK
            else:
                self.grid[unit.position] = SAND
                self.units += 1

    def solve(self, filename):
        self.reset()
        self.load_datas(filename)
        self.fill()
        self.solution = self.units



# -- MAIN

p_one = P14(0)
p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P14(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

