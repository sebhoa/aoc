# directions
DIRECTIONS = (-1,0), (-1,1), (0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1)
X_DIRECTIONS = (-1, 1), (1, 1), (1, -1), (-1, -1)

class P4(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 4, part)
        self.grid = []

    def reset(self):
        self.grid = []

    def load(self, filename):
        with open(filename) as datas:
            for line in datas:
                self.grid.append(line.strip())

    def inside(self, i, j):
        return 0 <= i < len(self.grid) and 0 <= j < len(self.grid[0])
    
    def word_on_direction(self, word, i, j, direction):
        n = len(word)
        di, dj = direction
        for k in range(n):
            if not self.inside(i+k*di, j+k*dj) or self.grid[i+k*di][j+k*dj] != word[k]:
                return False
        return True

    def mas_positions(self):
        mas = set()
        n, m = len(self.grid), len(self.grid[0])
        for i in range(n):
            for j in range(m):
                for d in X_DIRECTIONS:
                    if self.word_on_direction('MAS', i, j, d):
                        mas.add((i, j, d))
        return mas

    def h_flip(self, i, j, d):
        di, dj = d
        return i, j+2*dj, (di, -dj)

    def v_flip(self, i, j, d):
        di, dj = d
        return i+2*di, j, (-di, dj)
    
    def count_x_mas(self, mas):
        nb = 0
        while len(mas) > 0:
            i, j, d = mas.pop()
            h_mas = self.h_flip(i, j, d)
            v_mas = self.v_flip(i, j, d)
            if h_mas in mas:
                mas.remove(h_mas)
                nb += 1
            elif v_mas in mas:
                mas.remove(v_mas)
                nb += 1
        return nb
    
    def solve(self, filename):
        self.reset()
        self.load(filename)
        self.solution = 0
        n, m = len(self.grid), len(self.grid[0])
        if self.part == 0:
            for i in range(n):
                for j in range(m):
                    for d in DIRECTIONS:
                        if self.word_on_direction('XMAS', i, j, d):
                            self.solution += 1
        else:
            mas = self.mas_positions()
            self.solution = self.count_x_mas(mas)

def main():
    for part in (0, 1):
        pb = P4(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 