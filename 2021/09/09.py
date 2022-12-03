import sys
import collections

FILE = 'input09.txt'
INF = float('inf')

DELTAS = (1, 0), (-1, 0), (0, 1), (0, -1)

class Grid:

    def __init__(self, filename):
        self.filename = filename
        self.cases = {}
        self.width = 0
        self.height = 0
        self.minimums = set()
        self.bassins_sizes = []

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line_id, line in enumerate(datas):
                for col_id, data in enumerate(line.strip()):
                    self.cases[line_id+1, col_id+1] = int(data)
            self.width = col_id + 3
            self.height = line_id + 3
            for line_id in range(self.height):
                self.cases[line_id, 0] = INF
                self.cases[line_id, self.width-1] = INF
            for col_id in range(self.width):
                self.cases[0, col_id] = INF
                self.cases[self.height-1, col_id] = INF

    def __str__(self):
        """pour afficher la grille si on veut"""
        s = ''
        for line_id in range(self.height):
            for col_id in range(self.width):
                v = self.cases[line_id, col_id]
                if  v == INF:
                    s += '+'
                else:
                    s += str(v)
            s += '\n'
        return s

    def inside_coords(self):
        return ((line_id, col_id) for line_id in range(1, self.height-1) for col_id in range(1, self.width-1))

    def get_mins(self):
        for line_id, col_id in self.inside_coords():
            v = self.cases[line_id, col_id]
            if v < min(self.cases[line_id+dl, col_id+dc] for dl, dc in DELTAS):
                self.minimums.add((line_id, col_id))


    def solve(self):
        self.load()
        print(self)
        self.get_mins()
        return sum(self.cases[line_id, col_id]+1 for line_id, col_id in self.minimums)


    # -- Pour la partie 2

    def inside(self, pt):
        l, c = pt
        return 0 < l < self.height-1 and 0 < c < self.width-1

    def explore(self):
        """A partir des low points, explore les bassins et stocke leur taille"""
        for line_id, col_id in self.minimums:
            size = 0
            to_explore = collections.deque([(line_id, col_id)])
            seen = set()
            while to_explore:
                point = to_explore.popleft()
                seen.add(point)
                if self.cases[point] < 9:
                    size += 1
                    for dl, dc in DELTAS:
                        next_point = point[0]+dl, point[1]+dc
                        if self.inside(next_point) and next_point not in seen and next_point not in to_explore:
                            to_explore.append(next_point)
            self.bassins_sizes.append(size)

    def solve_two(self):
        self.load()
        #print(self)
        self.get_mins()
        self.explore()
        print(self.bassins_sizes)
        self.bassins_sizes.sort(reverse=True)
        a, b, c = self.bassins_sizes[:3]
        return a * b * c


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    zone = Grid(fichier)
    if version == '1':
        print(zone.solve())
    else:
        print(zone.solve_two())


if __name__ == '__main__':
    main() 
