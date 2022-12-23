"""
AOC 2022 -- Jour 22
S. Hoarau
"""

import re
from time import time
from puzzle import Puzzle

WALL = '#'
SPACE = '.'
NA = ' '

RIGHT = 0, 1
LEFT = 0, -1
DOWN = 1, 0
UP = -1, 0

DIRECTIONS_TO_INT = {RIGHT: 0, DOWN: 1, LEFT: 2, UP: 3}
OPPOSITE_DIRS = {RIGHT: LEFT, DOWN: UP, LEFT: RIGHT, UP: DOWN}
DIRS_STAMP = {RIGHT: '>', LEFT: '<', DOWN: 'v', UP: '^'}
COMPASS = {(RIGHT, 'R'): DOWN, (RIGHT, 'L'): UP, (LEFT, 'R'): UP, (LEFT, 'L'): DOWN,
        (UP, 'R'): RIGHT, (UP, 'L'): LEFT, (DOWN, 'R'): LEFT, (DOWN, 'L'): RIGHT}


class Map:

    def __init__(self, informations):
        self.tiles = {(i, j):info for i, row in enumerate(informations[:-1]) 
                                    for j, info in enumerate(row[:-1]) if info != NA}
        self.height = len(informations) - 1
        self.width = max(len(informations[i]) for i in range(self.height)) - 1 

        # pour chaque row : donne la colonne min et la colonne max
        self.rows = list(zip([min(j for j in range(self.width) if self.is_available(i, j)) for i in range(self.height)], 
                             [max(j for j in range(self.width) if self.is_available(i, j)) for i in range(self.height)]))
        
        # pour chaque col : donne la ligne min et la ligne max
        self.cols = list(zip([min(i for i in range(self.height) if self.is_available(i, j)) for j in range(self.width)], 
                             [max(i for i in range(self.height) if self.is_available(i, j)) for j in range(self.width)]))

    def is_available(self, i, j):
        return (i, j) in self.tiles

    def stamp(self, i, j, trace):
        return DIRS_STAMP[trace[i, j]] if (i, j) in trace else self.tiles[i, j]

    def aff(self, trace):
        for i in range(self.height):
            for j in range(self.width):
                char = self.stamp(i, j, trace) if self.is_available(i, j) else NA
                print(char, end='')
            print()

    def min_row(self, i):
        return self.rows[i][0]

    def max_row(self, i):
        return self.rows[i][1]

    def min_col(self, j):
        return self.cols[j][0]

    def max_col(self, j):
        return self.cols[j][1]

    def is_wall(self, i, j):
        return self.tiles[i, j] == WALL

    def next_on_plan(self, position, direction):
        """Renvoie True si on peut avancer dans la direction, ainsi que les nouvelles coordonnées, False et les anciennes sinon"""
        i, j = position
        di, dj = direction
        new_i, new_j = i + di, j + dj 
        if new_j > self.max_row(i):
            new_j = self.min_row(i)
        elif new_j < self.min_row(i):
            new_j = self.max_row(i)

        if new_i > self.max_col(j):
            new_i = self.min_col(j)
        elif new_i < self.min_col(j):
            new_i = self.max_col(j)

        if self.is_wall(new_i, new_j):
            return False, i, j
        else:
            return True, new_i, new_j

    def next_on_small_cube(self, position, direction):
        i, j = position
        di, dj = direction
        new_i, new_j, new_direction = i + di, j + dj, direction

        # print(f'{i},{j} -> Avant : {new_i},{new_j}', end=' ')

        # -- rouge, sens a -> a'
        if new_i == 3 and (4 <= new_j < 8) and direction == UP:
            # print("rouge a->a'")
            new_i = new_j - 4
            new_j, new_direction = 8, RIGHT

        # -- rouge, sens a' -> a 
        if 0 <= new_i < 4 and new_j == 7 and direction == LEFT:
            # print("rouge a'->a")
            new_j = 4 + new_i
            new_i, new_direction = 4, DOWN

        # -- bleu foncé, sens a -> a'
        if 0 <= new_i < 4 and new_j == 12:
            # print("bleu foncé a->a'")
            new_j, new_i, new_direction = 15, new_i + 8, LEFT

        # -- bleu foncé, sens a' -> a
        if new_j == 16 and (8 <= new_i < 12):
            # print("bleu foncé a'->a")
            new_i, new_j, new_direction = 11 - new_i, 11, LEFT

        # -- jaune, sens a -> a' 
        if 4 <= new_i < 8 and new_j == 12 and direction == RIGHT:
            # print("jaune a->a'")
            new_j = 19 - new_i
            new_i, new_direction = 8, DOWN

        # -- jaune, sens a' -> a 
        if new_i == 7 and (12 <= new_j < 16) and direction == UP:
            # print("jaune a'->a")
            new_i = 19 - new_j
            new_j, new_direction = 11, LEFT

        # -- bleu clair, sens a -> a'
        if new_i == 8 and (0 <= new_j < 4):
            # print("bleu clair a->a'")
            new_i, new_j, new_direction = 11, 11 - new_j, UP

        # -- bleu clair, sens a' -> a
        if new_i == 12 and (8 <= new_j < 12):
            # print("bleu clair a'->a")
            new_i, new_j, new_direction = 7, 11 - new_j, UP

        # -- orange, sens a -> a'
        if new_i == 8 and (4 <= new_j < 8) and direction == DOWN:
            # print("orange a->a'")
            new_i = 15 - new_j
            new_j, new_direction = 8, RIGHT

        # -- orange, sens a' -> a
        if 8 <= new_i < 12 and new_j == 7 and direction == LEFT:
            # print("orange a'->a")
            new_j = 15 - new_i
            new_i, new_direction = 7, UP

        # -- vert, sens a -> a'
        if new_i == 3 and 0 <= new_j < 4:
            # print("vert a->a'")
            new_i, new_j, new_direction = 0, 11 - new_j, DOWN

        # -- vert, sens a' -> a
        if new_i == -1 and 8 <= new_j < 12:
            # print("vert a'->a")
            new_i, new_j, new_direction = 4, 11 - new_j, DOWN

        # -- violet, sens a -> a'
        if 4 <= new_i < 8 and new_j == -1:
            # print("violet a->a'")
            new_j = 19 - new_i
            new_i, new_direction = 11, UP
        
        # -- violet, sens a' -> a
        if new_i == 12 and (12 <= new_j < 16):
            # print("violet a'->a")
            new_i =  19 - new_j
            new_j, new_direction = 0, RIGHT
        
        # print(f'Après : {new_i},{new_j}')
        # input()
        if self.is_wall(new_i, new_j):
            return False, i, j, direction
        else:
            return True, new_i, new_j, new_direction
        
    def next_on_big_cube(self, position, direction):
        i, j = position
        di, dj = direction
        new_i, new_j, new_direction = i + di, j + dj, direction

        # print(f'{i},{j} -> Avant : {new_i},{new_j}', end=' ')

        # -- rouge, sens a -> a'
        if new_i == 99 and (0 <= new_j < 50) and direction == UP:
            # print("rouge a->a'")
            new_i = 50 + new_j
            new_j, new_direction = 50, RIGHT

        # -- rouge, sens a' -> a 
        elif 50 <= new_i < 100 and new_j == 49 and direction == LEFT:
            # print("rouge a'->a")
            new_j = new_i - 50
            new_i, new_direction = 100, DOWN

        # -- vert, sens a -> a'
        elif new_i == -1 and 50 <= new_j < 100:
            # print("vert a->a'")
            new_i = 100 + new_j
            new_j, new_direction = 0, RIGHT

        # -- vert, sens a' -> a
        elif 150 <= new_i < 200 and new_j == -1:
            # print("vert a'->a")
            new_j = new_i - 100
            new_i, new_direction = 0, DOWN

        # -- violet, sens a -> a'
        elif 100 <= new_i < 150 and new_j == -1:
            # print("violet a->a'")
            new_i, new_j, new_direction = 149 - new_i, 50, RIGHT
        
        # -- violet, sens a' -> a
        elif 0 <= new_i < 50 and new_j == 49:
            # print("violet a'->a")
            new_i, new_j, new_direction = 149 - new_i, 0, RIGHT

        # -- bleu, sens a -> a'
        elif new_i == 200 and 0 <= new_j < 50:
            # print("bleu a->a'")
            new_i, new_j, new_direction = 0, new_j + 100, DOWN

        # -- bleu, sens a' -> a
        elif new_i == -1 and 100 <= new_j < 150:
            # print("bleu a'->a")
            new_i, new_j, new_direction = 199, new_j - 100, UP

        # -- orange, sens a -> a'
        elif new_i == 150 and (50 <= new_j < 100) and direction == DOWN:
            # print("orange a->a'")
            new_i = new_j + 100
            new_j, new_direction = 49, LEFT

        # -- orange, sens a' -> a
        elif 150 <= new_i < 200 and new_j == 50 and direction == RIGHT:
            # print("orange a'->a")
            new_j = new_i - 100
            new_i, new_direction = 149, UP

        # -- bleu foncé, sens a -> a'
        elif 0 <= new_i < 50 and new_j == 150:
            # print("bleu foncé a->a'")
            new_i, new_j, new_direction = 149 - new_i, 99, LEFT

        # -- bleu foncé, sens a' -> a
        elif 100 <= new_i < 150 and new_j == 100:
            # print("bleu foncé a'->a")
            new_i, new_j, new_direction = 149 - new_i, 149, LEFT

        # -- jaune, sens a -> a' 
        elif 50 <= new_i < 100 and new_j == 100 and direction == RIGHT:
            # print("jaune a->a'")
            new_j = 50 + new_i
            new_i, new_direction = 49, UP

        # -- jaune, sens a' -> a 
        elif new_i == 50 and (100 <= new_j < 150) and direction == DOWN:
            # print("jaune a'->a")
            new_i = new_j - 50
            new_j, new_direction = 99, LEFT

        
        # print(f'Après : {new_i},{new_j}')
        # if new_j == -87:
        #     input()
        if self.is_wall(new_i, new_j):
            return False, i, j, direction
        else:
            return True, new_i, new_j, new_direction        


class Hero:
    """C'est une carte, une position gps = une ligne, une colonne et une direction"""

    def __init__(self, map, first_steps, path):
        self.map = map
        self.first_steps = first_steps
        self.path = [(char, int(steps)) for char, steps in path]
        self.position = 0, map.min_row(0)
        self.direction = RIGHT
        self.trace = {}

    def one_step(self, on_cube, size):
        if on_cube:
            next_function = self.map.next_on_small_cube if size == 'small' else self.map.next_on_big_cube
            can_move, i, j, self.direction = next_function(self.position, self.direction)
        else:
            can_move, i, j = self.map.next_on_plan(self.position, self.direction)
        self.position = i, j
        self.trace[self.position] = self.direction
        return can_move

    def move(self, on_cube=False, size='small'):
        for _ in range(self.first_steps):
            if not self.one_step(on_cube, size):
                break
        for code_direction, nb_steps in self.path:
            self.direction = COMPASS[self.direction, code_direction]
            self.trace[self.position] = self.direction
            for _ in range(nb_steps):
                if not self.one_step(on_cube, size):
                    break
            # self.map.aff(self.trace)
            # input()


class P22(Puzzle):

    P1_REGEX = re.compile('^(\d+)')
    P2_REGEX = re.compile('(R|L)(\d+)')

    def __init__(self, part):
        Puzzle.__init__(self, 22, part)
        self.map = None
        self.hero = None

    def aff(self):
        self.map.aff(self.hero.trace)

    def load_datas(self, filename):
        with open(filename) as datas:
            *map_informations, path_informations = datas.readlines()
            self.map = Map(map_informations)
            first_steps = int(P22.P1_REGEX.findall(path_informations)[0])
            other_steps = P22.P2_REGEX.findall(path_informations)
            self.hero = Hero(self.map, first_steps, other_steps)

    def passwd(self):
        i, j = self.hero.position
        return 1000 * (i + 1) + 4 * (j + 1) + DIRECTIONS_TO_INT[self.hero.direction]

    def solve(self, filename, *args):
        if len(args) > 1:
            filename, size = args[0], args[1]
        elif len(args) > 0:
            size = args[0]
        self.load_datas(filename)
        if self.part == 0:
            self.hero.move()
            i, j = self.hero.position
            print(i, j, DIRECTIONS_TO_INT[self.hero.direction])
            self.solution = self.passwd()
        else:
            self.hero.move(on_cube=True, size=size)
            i, j = self.hero.position
            print(i, j, DIRECTIONS_TO_INT[self.hero.direction])
            self.solution = self.passwd()



# -- MAIN

p_one = P22(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P22(1)
p_two.test('small')
print(p_two)
p_two.validate('big')
print(p_two)

