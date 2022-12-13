from collections import deque
from puzzle import Puzzle

NORTH = -1, 0
SOUTH = 1, 0
EAST = 0, 1
WEST = 0, -1

DIRECTIONS = NORTH, EAST, SOUTH, WEST
INF = float('inf')
        
ALT_MAX = 25
ALT_MIN = 0

class P12(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 12, part)
        self.grid = []
        self.width = 0
        self.height = 0
        self.start = None                        
        self.end = None
        self.reverse = part==1
        self.cost = {}

    def exit(self, node):
        if self.reverse:
            return self.altitude(node) == ALT_MIN
        else:
            return node == self.end

    def is_end(self, node):
        i, j = node
        end_mark = 'a' if self.reverse else 'E'
        return self.grid[i][j] == end_mark

    def is_start(self, node):
        return node == self.start

    def inside(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width
    
    def ascii_code(self, node):
        i, j = node
        return ord(self.grid[i][j]) - ord('a')

    def altitude(self, node):
        if self.reverse:
            return ALT_MAX if self.is_start(node) else self.ascii_code(node)
        else:
            return ALT_MAX if self.is_end(node) else self.ascii_code(node)
    
    def reachable(self, dep, arr):
        if self.reverse:
            dep, arr = arr, dep
        return self.is_start(dep) or self.altitude(arr) <= self.altitude(dep) + 1
    
    def neighbors(self, node):
        i, j = node
        return ((i+di, j+dj) for di, dj in DIRECTIONS if self.inside(i+di, j+dj) and self.reachable((i, j), (i+di, j+dj)))
    
    def coordinates(self):
        return ((i, j) for i in range(self.height) for j in range(self.width))
    
    def load_datas(self, filename):
        with open(filename) as datas:
            self.grid = datas.readlines()
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        for i, j in self.coordinates():
            self.cost[i, j] = INF
            if self.grid[i][j] == 'S' and not self.reverse:
                self.start = i, j
            if self.grid[i][j] == 'E':
                if self.reverse:
                    self.start = i, j
                else:
                    self.end = i, j
        self.cost[self.start] = 0
    
    def reset(self):
        self.grid = []
        self.cost = {}
                
    def bfs(self):
        file = deque([self.start])
        while len(file) > 0:
            node = file.popleft()
            if self.exit(node):
                return self.cost[node]
            for v in self.neighbors(node):
                if self.cost[v] > self.cost[node] + 1:
                    self.cost[v] = self.cost[node] + 1
                    file.append(v)
                          
    def solve(self, filename=None):
        self.reset()
        self.load_datas(filename)
        self.solution = self.bfs()
    

p12 = P12(0)
p12.test()
print(p12)
p12.validate()
print(p12)

p12two = P12(1)
p12two.test()
print(p12two)
p12two.validate()
print(p12two)
