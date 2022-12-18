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

A = 0, 0, 0
B = 1, 0, 0
C = 1, 1, 0
D = 0, 1, 0
E = 0, 0, 1
F = 1, 0, 1
G = 1, 1, 1
H = 0, 1, 1

POINTS = B, C, D, E, F, G, H

DELTAS = (0, 0, -1), (1, 0, 0), (0, 0, 1), (-1, 0, 0), (0, -1, 0), (0, 1, 0)

class Cube:

    def __init__(self, puzzle, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.puzzle = puzzle

    def __repr__(self):
        return f'Cube({self.x}, {self.y}, {self.z})'

    def origin(self):
        return self.x, self.y, self.z

    def faces(self):
        x, y, z = self.x, self.y, self.z
        return (tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (A, B, C, D))), 
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (E, F, G, H))), 
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (A, B, F, E))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (B, C, G, F))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (C, D, H, G))),
                tuple(sorted((x+dx, y+dy, z+dz) for dx, dy, dz in (D, A, E, H))))

    def neighbors(self):
        return ((self.x + dx, self.y + dy, self.z + dz) for dx, dy, dz in DELTAS)

    

class P18(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 18, part)
        self.cubes = {}
        self.faces = {}
        self.air = {}
        self.trapped_air = set()
        self.outside = None

    def set_outside(self):
        xs = set(origin[0] for origin in self.cubes)
        ys = set(origin[1] for origin in self.cubes)
        zs = set(origin[2] for origin in self.cubes)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        min_z, max_z = min(zs), max(zs)
        self.outside = (min_x, max_x, min_y, max_y, min_z, max_z)


    def load_datas(self, filename):
        with open(filename) as datas:
            for line in datas:
                x, y, z = [int(e) for e in line.strip().split(',')]
                self.cubes[x, y, z] = Cube(self, x, y, z)
        self.set_outside()

    def reset(self):
        self.cubes = {}
        self.faces = {}
        self.air = {}
        self.trapped_air = set()
        self.free = set()

    def constant_component(self, face):
        for i in (0, 1, 2):
            if all(face[k][i] == face[0][i] for k in range(len(face))):
                return i

    def is_fresh_air(self, x, y, z):
        out = self.outside
        return x <= out[0] or x >= out[1] or y <= out[2] or y >= out[3] or z <= out[4] or z >= out[5]

    def air_cubes(self):
        origins = deque(list(self.cubes.keys()))
        visited = set()
        while len(origins) > 0:
            origin = origins.popleft()
            visited.add(origin)
            if origin not in self.cubes:
                if not self.is_fresh_air(*origin):
                    self.air[origin] = Cube(self, *origin)
                    for neighbor in self.air[origin].neighbors():
                        if neighbor not in origins and neighbor not in visited:
                            origins.append(neighbor)
            else:
                for neighbor in self.cubes[origin].neighbors():
                    if neighbor not in origins and neighbor not in visited:
                        origins.append(neighbor)

    def update_trapped(self, origin):
        """retire de l'ensemble de cubes d'air supposés emprisonnés, ceux qui ne le sont pas"""
        cubes_to_explore = deque([origin])
        visited = set()
        free = False
        while len(cubes_to_explore) > 0:
            x, y, z = cubes_to_explore.popleft()
            visited.add((x, y, z))
            if self.is_fresh_air(x, y, z):
                free = True
            else:
                for dx, dy, dz in DELTAS:
                    neighbor = x+dx, y+dy, z+dz
                    if neighbor not in self.cubes and neighbor not in self.free and neighbor not in cubes_to_explore and neighbor not in visited:
                        cubes_to_explore.append(neighbor)
        if free:
            for origin in visited:
                self.trapped_air.discard(origin)
                self.free.add(origin)

    def solve(self, filename, *args):
        self.reset()
        self.load_datas(filename)
        for cube in self.cubes.values():
            for face in cube.faces():
                self.faces[face] = self.faces.get(face, 0) + 1

        if self.part == 0:
            self.solution = sum(nb for nb in self.faces.values() if nb == 1)
        else:
            self.air_cubes()

            self.trapped_air = set(self.air)
            for origin in self.air:
                self.update_trapped(origin)
            for origin in self.trapped_air:
                for f in self.air[origin].faces():
                    self.faces[f] = 0

            self.solution = sum(nb for nb in self.faces.values() if nb == 1)



# -- MAIN

p_one = P18(0)

# p_one.test()
# print(p_one)
# p_one.validate()
# print(p_one)

p_two = P18(1)
# p_two.test()
# print(p_two)
p_two.validate()
print(p_two)

