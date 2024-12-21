UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = UP, DOWN, LEFT, RIGHT

SAFE = '.'
CORRUPTED = '#'

class Memory:

    def __init__(self, width, height, incoming):
        self.width = width
        self.height = height
        self.incoming = incoming
        self.grid = [[SAFE] * self.width for _ in range(self.height)]

    def __str__(self):
        s = '  ' + ''.join(str(e) for e in range(7)) + '\n'
        s += '\n'.join(str(i) + ' ' + ''.join(line) for i, line in enumerate(self.grid))
        return s

    def falling(self, n):
        for k in range(n):
            self.corrupt(k)

    def corrupt(self, k):
        x, y = self.incoming[k]
        self.grid[y][x] = CORRUPTED
    
    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def is_corrupted(self, x, y):
        return self.grid[y][x] == CORRUPTED
    
    def neighbors(self, position):
        x, y = position
        return [(x+dx, y+dy) for dy, dx in DIRECTIONS if self.inside(x+dx, y+dy) and not self.is_corrupted(x+dx, y+dy)]

    def detect_first(self):
        for k in range(len(self.incoming)):
            self.corrupt(k)
            if self.path() is None:
                return self.incoming[k]
    
    def path(self):
        partial = deque([(0, 0)])
        distances = {(0, 0): 0}
        seen = set()
        while len(partial) > 0:
            position = partial.popleft()
            distance = distances[position]
            seen.add(position)
            if position == (self.width-1, self.height-1):
                return distance
            else:
                for new_position in self.neighbors(position):
                    if new_position not in distances or distances[new_position] > distance+1:
                        partial.append(new_position)
                        distances[new_position] = distance+1
        return None
            

class P18(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 18, part)
        self.memory = None
    
    def load(self, filename):
        incoming = []
        with open(filename) as datas:
            w, h = [int(e) for e in datas.readline().split()]
            for line in datas:
                position = tuple(int(e) for e in line.strip().split(','))
                incoming.append(position)
        self.memory = Memory(w, h, incoming)

    def solve(self, filename):
        self.load(filename)
        if self.part == 0:
            size = 1024
            self.memory.falling(size)
            self.solution = self.memory.path()
        else:
            x, y = self.memory.detect_first()
            self.solution = f'{x},{y}'

def main():
    for part in (0, 1):
        pb = P18(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 