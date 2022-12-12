from puzzle import Puzzle

MOVES = {(i, j): (0, 0) for i in (-1, 0, 1) for j in (-1, 0, 1)}
MOVES[0, 2] = (0, 1)
MOVES[0, -2] = (0, -1)
MOVES[2, 0] = (1, 0)
MOVES[-2, 0] = (-1, 0)
MOVES[-2, 1] = MOVES[-1, 2] = MOVES[-2, 2] = (-1, 1)
MOVES[-2, -1] = MOVES[-1, -2] = MOVES[-2, -2] = (-1, -1)
MOVES[2, -1] = MOVES[1, -2] = MOVES[2, -2] = (1, -1)
MOVES[2, 1] = MOVES[1, 2] = MOVES[2, 2] = (1, 1)

DIRECTIONS = {'R': (0, 1), 'U': (-1, 0), 'L': (0, -1), 'D': (1, 0)}

class P9(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 9, part)
        self.visited = set()
        self.instructions = []
        self.head = [0, 0]
        self.tail = [0, 0]
        
    def reset(self):
        self.head = [0, 0]
        self.tail = [0, 0]
        self.visited = set()
        self.instructions = []
        
    def move(self, point, direction):
        di, dj = direction
        point[0] += di
        point[1] += dj
                
    def delta(self, a, b):
        """Calcule le delta de déplacement entre le point de départ a et celui d'arrivée b"""
        return b[0] - a[0], b[1] - a[1]
            
    def moves(self, tail):
        """Lit les instructions du style R 8 et fait bouger l'ensemble du snake"""
        for instruction in self.instructions:
            code_direction = instruction[0]
            nb = int(instruction[2:])
            for i in range(nb):
                # mvt de la tête
                self.move(self.head, DIRECTIONS[code_direction])
                
                # mvt du reste du corps
                for j in range(1, len(tail)):
                    di, dj = self.delta(tail[j], tail[j-1])
                    self.move(tail[j], MOVES[di, dj])
            
                self.visited.add(tuple(self.tail))
        
    def load_datas(self, filename):
        with open(filename) as datas:
            self.instructions = datas.read().strip().split('\n')

        
    def solve(self, filename):
        self.reset()
        self.load_datas(filename)
        if self.part == 0:
            snake = [self.head, self.tail]
        else:
            snake = [self.head] + [[self.head[0], self.head[1]] for _ in range(8)] + [self.tail]
        self.moves(snake)
        self.solution = len(self.visited)
        print(self)

p9one = P9(0)
p9one.validate()
p9two = P9(1)
p9two.validate()