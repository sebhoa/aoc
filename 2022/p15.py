"""
AOC 2022 -- Jour 15
S. Hoarau
"""

import re
from puzzle import Puzzle
from time import time

INF = float('inf')

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position(self):
        return self.x, self.y

    def distance(self, point):
        return P15.manhattan(self.position(), point)


class Beacon(Point):

    def __init__(self, *args):
        Point.__init__(self, *args)

    def __repr__(self):
        return f'Beacon({self.x}, {self.y})'


class Sensor(Point):

    def __init__(self, x, y, beacon):
        Point.__init__(self, x, y)
        self.beacon = beacon
        self.radius = self.distance(beacon.position())

    def __repr__(self):
        return f'Sensor({self.x}, {self.y}) -- {repr(self.beacon)} -- Radius: {self.radius}'


class P15(Puzzle):

    PATTERN = re.compile(r'[-]?\d+')

    @classmethod
    def manhattan(cls, point_a, point_b):
        x_a, y_a = point_a
        x_b, y_b = point_b
        return abs(x_a - x_b) + abs(y_a - y_b)

    def __init__(self, part):
        Puzzle.__init__(self, 15, part)
        self.sensors = {}
        self.beacons = {}
 
    def load_datas(self, filename):
        with open(filename) as datas:
            for data in datas.readlines():
                xS, yS, xB, yB = [int(e) for e in P15.PATTERN.findall(data)]
                beacon = Beacon(xB, yB)
                self.beacons[xB, yB] = beacon
                self.sensors[xS, yS] = Sensor(xS, yS, beacon)

    def reset(self):
        self.sensors = {}
        self.beacons = {}

    def intersection(self, set_of_min_max):
        """Réduit une liste triée d'intervalles pour garder des intervalles disjoints"""
        l_min_max = sorted(set_of_min_max)
        new_l = [l_min_max[0]]
        for i in range(1, len(l_min_max)):
            mini_i, maxi_i = l_min_max[i]
            mini_0, maxi_0 = new_l.pop()
            if mini_i <= maxi_0 + 1:
                a = min(mini_i, mini_0)
                b = max(maxi_i, maxi_0)
                new_l.append((a, b))
            else:
                new_l.append((mini_0, maxi_0))
                new_l.append((mini_i, maxi_i))
        return new_l

    def x_min_and_max(self, y0):
        """Crée la liste des intervalles disjoints de x interdits pour la ligne y0"""
        set_of_min_max = set()
        for sensor in self.sensors.values():
            hauteur = abs(sensor.y - y0)
            radius = sensor.radius - hauteur
            if radius > 0:
                set_of_min_max.add((sensor.x - radius, sensor.x + radius))
        return self.intersection(set_of_min_max)

    def solve(self, filename, y0):
        self.reset()
        self.load_datas(filename)
        if self.part == 0:
            list_of_min_max = self.x_min_and_max(y0)
            self.solution = sum(max_x - min_x for (min_x, max_x) in list_of_min_max)
        else:
            for y in range(y0+1):
                list_of_min_max = self.x_min_and_max(y)
                if len(list_of_min_max) > 1:
                    break
            x_uniq = list_of_min_max[0][1] + 1
            self.solution = x_uniq * 4000000 + y


# -- MAIN

p_one = P15(0)

t = time()
p_one.test(10)
print(p_one)
p_one.validate(2000000)
print(p_one)
print(time() - t)

t = time()
p_two = P15(1)
p_two.test(20)
print(p_two)
p_two.validate(4000000)
print(p_two)
print(time() - t)

