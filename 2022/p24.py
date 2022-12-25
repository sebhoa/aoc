"""
AOC 2022 -- Jour 24
S. Hoarau
"""

from puzzle import Puzzle


SPACE = '.'
EXIT = '.'
WALL = '#'

ENTRANCE = -1, 0

NOMOVE = 0, 0
EAST = 0, 1
SOUTH = 1, 0
WEST = 0, -1
NORTH = -1, 0

DIRECTIONS = EAST, SOUTH, WEST, NORTH, NOMOVE

DIRECTION_TO_TILE = {EAST: '>', SOUTH: 'v', WEST: '<', NORTH: '^'}
TILE_TO_DIRECTION = {tile: direction for direction, tile in DIRECTION_TO_TILE.items()}


class Blizzard:

    def __init__(self, width, height, i, j, tile):
        self.width = width
        self.height = height
        self.tile = tile
        self.position = i, j
        self.direction = TILE_TO_DIRECTION[tile]
        
    def move(self):
        i, j = self.position
        di, dj = self.direction
        self.position = (i + di) % self.height, (j + dj) % self.width


class Laby3D:

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.floor = {}
        self.generate_floor(ENTRANCE)

    def generate_floor(self, position):
        self.floor = {new_position: self.puzzle.counts[new_position] for new_position in self.neighbors(position)}

    def inside(self, i, j):
        return (i, j) == self.puzzle.exit or (i, j) == ENTRANCE or 0 <= i < self.puzzle.height and 0 <= j < self.puzzle.width

    def free(self, position):
        return self.floor[position] == 0

    def neighbors(self, position):
        i, j = position
        return ((i+di, j+dj) for di, dj in DIRECTIONS if self.inside(i+di, j+dj))

    def bfs(self, start, goal):
        positions = {start}
        step = -1
        while True:
            step += 1
            self.puzzle.blizzards_move()
            new_positions = set()
            for position in positions:
                if position == goal:
                    return step
                else:
                    self.generate_floor(position)
                    for new_position in self.neighbors(position):
                        if self.free(new_position) and new_position not in new_positions:
                            new_positions.add(new_position)
            positions = new_positions


class P24(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 24, part)
        self.height = 0
        self.width = 0
        self.exit = None
        self.position = ENTRANCE
        self.blizzards = []
        self.counts = {}
        self.laby = None

    def load_datas(self, filename):
        self.blizzards = []
        self.counts = {}
        with open(filename) as datas:
            informations = datas.readlines()[1:-1]
            self.height = len(informations)
            self.width = len(informations[0]) - 3
            self.exit = self.height, self.width - 1
            for i, line in enumerate(informations):
                for j, tile in enumerate(line.strip()[1:-1]):
                    self.counts[i, j] = 0
                    if tile != SPACE:
                        self.add_blizz(i, j, tile)
        self.counts[ENTRANCE] = self.counts[self.exit] = 0
        self.laby = Laby3D(self)

    def aff_blizzards(self):
        s = f"#{SPACE}{'#'*(self.width)}\n"
        for i in range(self.height):
            s += '#'
            for j in range(self.width):
                if self.counts[i, j] == 0:
                    tile = SPACE
                elif self.counts[i, j] == 1:
                    tile = self.blizzard(i, j).tile
                else:
                    tile = str(self.counts[i, j])
                s += f'{tile}'
            s += '#\n'
        s +=  f"{'#'*(self.width)}{EXIT}#\n"
        return s

    def blizzard(self, i, j):
        for blizz in self.blizzards:
            if blizz.position == (i, j):
                return blizz

    def add_blizz(self, i, j, tile):
        self.blizzards.append(Blizzard(self.width, self.height, i, j, tile))
        self.counts[i, j] += 1

    def blizzards_move(self):
        for blizz in self.blizzards:
            old = blizz.position
            blizz.move()
            self.counts[old] -= 1
            self.counts[blizz.position] += 1

    def solve(self, filename, *args):
        if len(args) > 0:
            filename = args[0]
        self.load_datas(filename)
        if self.part == 0:
            self.solution = self.laby.bfs(ENTRANCE, self.exit)
        else:
            self.solution = 2
            for start, goal in ((ENTRANCE, self.exit), (self.exit, ENTRANCE), (ENTRANCE, self.exit)):
                self.solution += self.laby.bfs(start, goal)



# -- MAIN

p_one = P24(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P24(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

