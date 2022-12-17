"""
AOC 2022 -- Jour 17
S. Hoarau
"""

from puzzle import Puzzle

EMPTY = '.'
EMPTY_LINE = EMPTY * 7
FLOOR = '-' * 9

ROCK = '#'
MOVING = '@'
SPACE = '.'

DOWN = -1, 0
LEFT = 0, -1
RIGHT = 0, 1
NO_MOVE = 0, 0

DIRECTIONS = {'v': DOWN, '<': LEFT, '>':RIGHT}

class Rock:

    def __init__(self, puzzle, shape):
        self.shape = [list(line) for line in shape]
        self.height = len(self.shape)
        self.width = len(self.shape[0])
        self.upperleft = puzzle.chamber.size + 3 + self.height - 1, 2
        self.puzzle = puzzle 

    def cell(self, i, j):
        return self.puzzle.chamber.grid[i][j] 

    def inside(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width

    def translate(self, i, j):
        top, left = self.upperleft
        return i + top - self.height + 1, j + left

    def free(self, i, j, di, dj):
        ti, tj = self.translate(i, j)
        return ti+di >= self.puzzle.height() or self.puzzle.chamber.inside(ti+di, tj+dj) and (self.cell(ti+di, tj+dj) != ROCK or self.shape[i][j] == SPACE)

    def can_move(self):
        di, dj = self.puzzle.direction
        for i in range(self.height):
            for j in range(self.width):
                if not self.free(i, j, di, dj):
                    return False
        return True

    def move(self):
        if self.can_move():
            ti, tj = self.upperleft
            di, dj = self.puzzle.direction
            self.upperleft = ti+di, tj+dj
            return True
        return False

    def rest(self):
        for i in range(self.height):
            for j in range(self.width):
                ti, tj = self.translate(i,  j)
                if self.shape[i][j] == MOVING:
                    self.puzzle.chamber.mark(ti, tj)


class Chamber:

    def __init__(self, puzzle):
        self.puzzle = puzzle
        self.grid = []
        self.size = 0

    def more_spaces(self):
        for _ in range(3):
            self.grid.append([SPACE] * 7)

    def inside(self, i, j):
        return 0 <= i and 0 <= j < 7

    def update_size(self, top):
        self.size = max(self.size, top+1)

    def translate(self, i, j):
        top, left = self.puzzle.rock.upperleft
        return i - top + self.puzzle.rock.height - 1, j - left 

    def fusion(self, rock_unit, chamber_unit):
        return ROCK if chamber_unit == ROCK else rock_unit

    def direction(self):
        return self.puzzle.direction

    def aff_line(self, i):
        print('|', end='')
        for j in range(7):
            line = EMPTY_LINE if i >= self.puzzle.height() else self.grid[i]
            rock_i, rock_j = self.translate(i, j)
            # print(rock_i, rock_j)
            if self.puzzle.rock.inside(rock_i, rock_j):
                print(self.fusion(self.puzzle.rock.shape[rock_i][rock_j], line[j]), end='')
            else:
                print(line[j], end='')
        print('|', end='')

    def aff(self, no_limit=True):
        top, _ = self.puzzle.rock.upperleft
        bottom = top - self.puzzle.rock.height + 1
        end = -1 if no_limit else top - 15
        start = max(self.size, top) #- 1
        for i in range(start, end, -1):
            if i == top:
                print('T>', end=' ')
            else:
                print(f'  ', end=' ')

            self.aff_line(i)
            if i == bottom:
                print('<B')
            elif i == self.size - 1:
                print('<S')
            else:
                print()
        print('   '+FLOOR)

    def mark(self, i, j):
        self.grid[i][j] = ROCK


class P17(Puzzle):

    SHAPES = [['@@@@'], 
              ['.@.', '@@@', '.@.'], 
              ['@@@', '..@', '..@'], 
              ['@', '@', '@', '@'],
              ['@@', '@@']]

    def __init__(self, part):
        Puzzle.__init__(self, 17, part)
        self.chamber = Chamber(self)
        self.nb_rocks = 0
        self.rock = None
        self.directions = ''
        self.index = 0
        # self.configs = []

    def height(self):
        return len(self.chamber.grid)

    def load_datas(self, filename):
        with open(filename) as datas:
            for c in datas.readline().strip():
                self.directions += f'{c}v'
        self.next_direction()            

    def aff(self, no_limit=True):
        self.chamber.aff(no_limit)
    
    def next_direction(self):
        self.direction = DIRECTIONS[self.directions[self.index]]
        self.index = (self.index + 1) % len(self.directions)

    def new_rock(self):
        # self.configs.append((self.nb_rocks, self.index, ))
        self.chamber.more_spaces()
        self.rock = Rock(self, P17.SHAPES[self.nb_rocks % 5])
        self.nb_rocks += 1

    def solve(self, filename, *args):
        self.load_datas(filename)
        limit = 2023 if self.part == 0 else 1000000000000
        self.new_rock()
        while self.nb_rocks < 1441:
            #print(f'{self.nb_rocks:013}', end='\b'*13)
            if self.index % len(self.directions) ==  2 and self.nb_rocks % 5 == 2:
            #if self.nb_rocks % 35 == 15:
                self.aff(no_limit=False)
                print(self.nb_rocks)
                print(self.chamber.size)
                input()
            if not self.rock.move():
                if self.direction == DOWN:
                    self.rock.rest()
                    self.chamber.update_size(self.rock.upperleft[0])
                    self.new_rock()
            self.next_direction()
        print(self.chamber.size)
        self.solution = self.chamber.size



# -- MAIN

# p_one = P17(0)

# p_one.test()
# print(p_one)
# p_one.validate()
# print(p_one)

p_two = P17(1)
# p_two.test()
# print(p_two)
p_two.validate()
print(p_two)

