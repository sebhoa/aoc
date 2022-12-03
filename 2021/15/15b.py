import sys

FILE = 'input15.txt'
DELTAS = (1, 0), (0, 1), (-1, 0), (0, -1)
INF = float('inf')

class PathFinder:


    def __init__(self, filename):
        self.filename = filename
        self.graph = []
        self.width = 0
        self.height = 0
        self.start = 0, 0
        self.end = 0, 0
        self.heuristique = {}


    def __str__(self):
        return '\n'.join([''.join([str(e) for e in line]) for line in self.graph])

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def neighboors(self, x, y):
        return ((x+dx, y+dy) for dx, dy in DELTAS if self.inside(x+dx, y+dy))

    def load(self):
        self.graph = []
        with open(self.filename, 'r') as datas:
            for y, line in enumerate(datas):
                small_w = len(line) - 1
                self.graph.append([])
                for x, data in enumerate(line.strip()):
                    self.graph[-1].append(int(data))
                for dx in range(1, 5):
                    for x in range(small_w):
                        increased_val = self.graph[-1][x] + dx
                        self.graph[-1].append(increased_val if increased_val <= 9 else increased_val - 9)
            small_h = len(self.graph)
            self.width = len(self.graph[0])
            for dy in range(1, 5):
                for y in range(small_h):
                    self.graph.append([])
                    for x in range(self.width):
                        increased_val = self.graph[y][x] + dy
                        self.graph[-1].append(increased_val if increased_val <= 9 else increased_val - 9)
            self.height = len(self.graph)
            self.end = self.width - 1, self.height - 1


    def update_cost(self, n1, n2, nodes_cost, n2_weight):
        """update cost of n2, neighboor of n1"""
        old_cost = nodes_cost.get(n2, INF)
        nodes_cost[n2] = min(old_cost, nodes_cost[n1] + n2_weight)

    def select_min(self, to_explore, marked):
        return min(((node, cost) for (node, cost) in to_explore.items() if node not in marked), key=lambda e: e[1])

    def dijkstra(self):
        to_explore = {self.start: 0}
        marked = set()
        while self.end not in to_explore:
            node, cost = self.select_min(to_explore, marked)
            marked.add(node)
            for neighboor in self.neighboors(*node):
                if neighboor not in marked:
                    x, y = neighboor
                    weight = self.graph[y][x]
                    self.update_cost(node, neighboor, to_explore, weight)
        return to_explore[self.end]


    def solve(self):
        self.load()
        print(self.width, self.height)
        return self.dijkstra()


def main():
    if len(sys.argv) > 1:
        fichier = sys.argv[1]
    else:
        fichier = FILE
    pf = PathFinder(fichier)
    print(pf.solve())

if __name__ == '__main__':
    main() 

