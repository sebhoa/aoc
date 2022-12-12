NORTH = -1, 0
SOUTH = 1, 0
EAST = 0, 1
WEST = 0, -1

DIRECTIONS = NORTH, EAST, SOUTH, WEST
INF = float('inf')

class PathFinder:
    """Code un AStar pour la partie I (on cherche à aller de S vers E)
    code un Dijkstra pour la partie II : on a le départ (E) et on va calculer
    tous les plus courts chemins jusqu'à tomber sur un point 'a'
    """
    
    def __init__(self, puzzle, heuristic):
        self.puzzle = puzzle
        self.start = puzzle.start
        self.end = puzzle.end
        self.__cout = {self.start: 0}
        self.pred = {self.start: None}
        self.closed = set()
        self.opened = {self.start}
        self.last = self.start
        self.heuristic = puzzle.heuristic if not self.puzzle.reverse else (lambda x: 0)

    def finished(self):
        if self.puzzle.reverse:
            return self.puzzle.altitude(self.last) == 0
        else:
            return self.end in self.closed
    
    def cout(self, node):
        return self.__cout.get(node, INF)
    
    def estimation(self, node):
        return self.cout(node) + self.heuristic(node)
    
    def select_node(self):
        best = min(self.opened, key=self.estimation)
        self.opened.remove(best)
        self.closed.add(best)
        self.last = best
                
    def update(self):
        for s in self.puzzle.neighbors(self.last):
            if s not in self.closed:
                cout = self.cout(self.last) + 1
                if self.cout(s) > cout:
                    self.__cout[s] = cout
                    self.pred[s] = self.last
                    self.opened.add(s)

    def solve(self):
        while not self.finished():
            node = self.select_node()
            self.update()
            
    def path(self):
        res = [self.last]
        pred = self.pred[res[-1]] 
        while pred is not None:
            res.append(pred)
            pred = self.pred[res[-1]]
        res.reverse()
        return res
    
    def cost(self):
        return self.cout(self.last)
    
    

class P12(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 12, part)
        self.grid = []
        self.width = 0
        self.height = 0
        self.start = None                        
        self.end = None
        self.solver = None
        self.reverse = part==1
        
    def is_start(self, point):
        return point == self.start

    def is_end(self, i, j):
        if self.reverse:
            return self.grid[i][j] == 'a'
        else:
            return self.grid[i][j] == 'E'

    def inside(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width
    
    def altitude(self, point):
        i, j = point
        if self.reverse:
            return (ord('z') - ord('a')) if self.is_start(point) else (ord(self.grid[i][j]) - ord('a'))
        else:
            return (ord('z') - ord('a')) if self.is_end(i, j) else (ord(self.grid[i][j]) - ord('a'))
    
    def reachable(self, dep, arr):
        if self.reverse:
            dep, arr = arr, dep
        return self.is_start(dep) or self.altitude(arr) <= self.altitude(dep) + 1
    
    def neighbors(self, position):
        i, j = position
        return ((i+di, j+dj) for di, dj in DIRECTIONS if self.inside(i+di, j+dj) and self.reachable((i, j), (i+di, j+dj)))
    
    def load_datas(self, filename):
        with open(filename) as datas:
            for i, line in enumerate(datas):
                self.grid.append([])
                for j, alt in enumerate(line.strip()):
                    if alt == 'S':
                        if not self.reverse:
                            self.start = i, j
                    elif alt == 'E':
                        if self.reverse:
                            self.start = i, j
                        else:
                            self.end = i, j
                    self.grid[i].append(alt)
            self.height = len(self.grid)
            self.width = len(self.grid[0])
            self.solver = PathFinder(self, self.heuristic)
    
    def reset(self):
        self.grid = []
        
    def heuristic(self, position):
        return abs(position[0] - self.end[0]) + abs(position[1] - self.end[1])
            
    def solve(self, filename=None):
        self.reset()
        self.load_datas(filename)
        self.solver.solve()
        self.solution = len(self.solver.path()) - 1
        print(self)