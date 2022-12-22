"""
AOC 2022 -- Jour 20
S. Hoarau
"""

import re
from collections import deque
from puzzle import Puzzle

ENCRYPTION_KEY = 811589153

class Node:

    def __init__(self, val, initial_position):
        self.val = val
        self.next = self
        self.previous = self
        self.id = initial_position

    def bye(self):
        """quitte la liste circulaire en reconnectant les restant"""
        self.previous.next = self.next
        self.next.previous = self.previous
        self.previous = self
        self.next = self

    def new_previous(self, node):
        """Insère un nouveau node comme previous"""
        node.previous = self.previous
        node.next = self
        self.previous.next = node
        self.previous = node


class Circular:

    def __init__(self, encryption_key):
        self.start = None
        self.size = 0
        self.key = encryption_key

    def empty(self):
        return self.size == 0

    def __str__(self):
        node = self.start
        s = ''
        for _ in range(self.size):
            s += f'{node.val} ({node.id}) '
            node = node.next
        return s

    def insert_many(self, elements):
        for i, elt in enumerate(elements):
            self.insert_one(elt * self.key, i)


    def insert_one(self, elt, initial_position):
        """l'insertion se fait à gauche du nœud entrée"""
        node = Node(elt, initial_position)
        if self.empty():
            self.start = node
        else:
            self.start.new_previous(node)
        self.size += 1

    def reach_next_to_move(self, node_id):
        """Atteindre le prochain dans la liste à devoir bouger"""
        while self.start.id != node_id:
            self.start = self.start.next

    def left(self, node_id):
        self.reach_next_to_move(node_id)
        node = self.start
        if node.val % (self.size - 1) != 0:
            neighbor = node
            steps = node.val % (self.size - 1)
            for _ in range(steps + 1):
                neighbor = neighbor.next
            if neighbor is not node:
                node.bye()
                neighbor.new_previous(node)


class P20(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 20, part)
        self.key = 1 if self.part == 0 else ENCRYPTION_KEY        
        self.coordinates = Circular(self.key)
        self.nb_rounds = 0

    def load_datas(self, filename):
        with open(filename) as datas:
            self.coordinates.insert_many([int(e.strip()) for e in datas])

    def move(self):
        for round in range(1, self.nb_rounds+1):
            node_id = 0
            for _ in range(self.coordinates.size):
                self.coordinates.left(node_id)
                node_id += 1

    def reset(self):
        self.coordinates = Circular(self.key)

    def zero(self):
        while self.coordinates.start.val != 0:
            self.coordinates.start = self.coordinates.start.next

    def solve(self, filename, *args):
        self.reset()
        if len(args) > 0:
            filename = args[0]
        self.load_datas(filename)

        self.nb_rounds = 1 if self.part == 0 else 10
        self.move()
        self.zero()
        self.solution = 0
        size = self.coordinates.size
        big_steps = (0, 1000, 2000, 3000)
        for i in range(1, 4):
            steps = ((big_steps[i] % size) - (big_steps[i-1] % size)) % size
            for _ in range(steps):
                self.coordinates.start = self.coordinates.start.next
            self.solution += self.coordinates.start.val






# -- MAIN

p_one = P20(0)

p_one.test()
print(p_one)
p_one.validate()
print(p_one)

p_two = P20(1)
p_two.test()
print(p_two)
p_two.validate()
print(p_two)

