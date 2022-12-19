"""
AOC 2022 -- Jour 18
S. Hoarau

Un Cube :

    H --------- G
   /           /|
  /           / |
 /           /  |
E --------- F   |  
|   D ------|-- C
|  /        |  /
| /         | /
|/          |/
A --------- B 


"""

from collections import deque
from puzzle import Puzzle

# -- Points pour décrire un cube ou une face
# --
A = 0, 0, 0
B = 1, 0, 0
C = 1, 1, 0
D = 0, 1, 0
E = 0, 0, 1
F = 1, 0, 1
G = 1, 1, 1
H = 0, 1, 1

POINTS = B, C, D, E, F, G, H

# -- Vecteurs unitaires
# --
UP = (0, 0, 1)
DOWN = (0, 0, -1)
LEFT = (-1, 0, 0)
RIGHT = (1, 0, 0)
FORWARD = (0, -1, 0)
BACKWARD = (0, 1, 0)

VECTORS = UP, DOWN, LEFT, RIGHT, FORWARD, BACKWARD

# -- Type des cubes
# --
INSIDE = 0
OUTSIDE = 1
BORDER = 2
LAVA = 3

STR_TYPE = 'IN', 'OUT', 'BORD', 'LAVE'

# -- Quelques petits utilitaires
# -- 
def first_or_last(n, integers):
    return len(integers) == 0 or n <= integers[0] or n >= integers[-1]


# -- LES CLASSES
# --------------

class Cube:

    def __init__(self, puzzle, x, y, z, type):
        self.puzzle = puzzle
        self.x = x
        self.y = y
        self.z = z
        self.type = type
        self.is_outside()
        
    def __repr__(self):
        return f'Cube({self.x}, {self.y}, {self.z}, {STR_TYPE[self.type]})'

    def origin(self):
        return self.x, self.y, self.z

    def faces(self):
        """Renvoie un générateur sur les 6 faces d'un cube"""
        x, y, z = self.x, self.y, self.z
        return (tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (A, B, C, D))), 
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (E, F, G, H))), 
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (A, B, F, E))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (B, C, G, F))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (C, D, H, G))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (D, A, E, H))))

    def neighbors(self):
        """"renvoie un générateur sur les 6 points voisins du point origine d'un cube (le point A cf schéma)"""
        return ((self.x + dx, self.y + dy, self.z + dz) for dx, dy, dz in VECTORS)

    def is_outside(self):
        if self.type != LAVA and self.infinity_sight():
            self.type = OUTSIDE
            return True
        return False

    def infinity_sight(self):
        """Renvoie True si le cube à une vue vers l'infini dans une des 6 directions"""
        cubes = self.puzzle.cubes.values()
        x_with_same_yz = sorted(cube.x for cube in cubes if cube.y == self.y and cube.z == self.z)
        y_with_same_xz = sorted(cube.y for cube in cubes if cube.x == self.x and cube.z == self.z)
        z_with_same_xy = sorted(cube.z for cube in cubes if cube.x == self.x and cube.y == self.y)

        return first_or_last(self.x, x_with_same_yz) or\
                first_or_last(self.y, y_with_same_xz) or\
                first_or_last(self.z, z_with_same_xy)


class P18(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 18, part)
        self.cubes = {}
        self.faces = {}

    def load_datas(self, filename):
        with open(filename) as datas:
            for line in datas:
                x, y, z = [int(e) for e in line.strip().split(',')]
                self.cubes[x, y, z] = Cube(self, x, y, z, LAVA)

    def reset(self):
        self.cubes = {}
        self.faces = {}

    def set_faces(self):
        """Comptabilise toutes les faces de tous les cubes de type lave"""
        for cube in self.cubes.values():
            if cube.type == LAVA:
                for face in cube.faces():
                    self.faces[face] = self.faces.get(face, 0) + 1

    def border(self):
        return (cube for cube in self.cubes.values() if cube.type == BORDER)

    def outside(self):
        return (cube for cube in self.cubes.values() if cube.type == OUTSIDE)

    def inside(self):
        return (cube for cube in self.cubes.values() if cube.type == INSIDE)

    def set_border(self):
        """Un parcours en largeur à partir des cubes lave pour déterminer les cubes frontière"""
        new_cubes = {}
        for cube in self.cubes.values():
            for xyz in cube.neighbors():
                if xyz not in self.cubes and xyz not in new_cubes:
                    new_cubes[xyz] = Cube(self, *xyz, BORDER)
        self.cubes.update(new_cubes)

    def set_inside(self):
        """La méthode la plus compliquée de la modélisation : on parcourt en largeur
        tous les cubes de type BORDER pour obtenir la composante connexe... si un des
        cubes est OUTSIDE alors ils le sont tous. Sinon c'est du INSIDE"""
        for cube in self.cubes.values():
            if cube.type == BORDER:
                to_explore = deque([cube.origin()])
                connected_xyz = set()
                type_of_connected = INSIDE
                while len(to_explore) > 0:
                    current_xyz = to_explore.popleft()
                    cube = self.cubes[current_xyz]
                    connected_xyz.add(current_xyz)
                    if cube.is_outside():
                        type_of_connected = OUTSIDE
                    else:
                        for xyz in cube.neighbors():
                            if xyz in self.cubes and self.cubes[xyz].type != LAVA and xyz not in to_explore and xyz not in connected_xyz:
                                to_explore.append(xyz)
                for xyz in connected_xyz:
                    self.cubes[xyz].type = type_of_connected


    def solve(self, filename, *args):
        self.reset()
        if len(args) > 0:
            filename = args[0]
        self.load_datas(filename)
        self.set_faces()
        self.solution = sum(nb for nb in self.faces.values() if nb == 1)

        if self.part == 1:
            # pour la Part Two (part = 1) on doit supprimer quelques faces avec de compter
            #
            self.set_border()
            self.set_inside()
            for cube in self.cubes.values():
                if cube.type == INSIDE:
                    for f in cube.faces():
                        self.faces[f] = 0

        self.solution = sum(nb for nb in self.faces.values() if nb == 1)



# -- MAIN

p_one = P18(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P18(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

