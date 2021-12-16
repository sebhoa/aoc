import sys
import heapq

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


    def __str__(self):
        return '\n'.join([''.join([str(e) for e in line]) for line in self.graph])

    def inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def neighboors(self, x, y):
        return ((x+dx, y+dy) for dx, dy in DELTAS if self.inside(x+dx, y+dy))

    def load(self):
        small_graph = []
        with open(self.filename, 'r') as datas:
            for line in datas:
                small_graph.append([int(e) for e in line.strip()])
        small_w = len(small_graph[0])
        small_h = len(small_graph)

        self.width = 5 * small_w
        self.height = 5 * small_h

        self.end = self.width - 1, self.height - 1

        for y in range(self.height):
            self.graph.append([])
            small_y = y % small_h
            dy = y // small_h
            for x in range(self.width):
                small_x = x % small_w
                dx = x // small_w
                val = small_graph[small_y][small_x] + dx + dy
                self.graph[-1].append(val if val <= 9 else val - 9)

    def update_cost(self, n1, n2, heap, nodes_cost, n2_weight):
        """update cost of n2, neighboor of n1"""
        old_cost = nodes_cost.get(n2, INF)
        new_cost = min(old_cost, nodes_cost[n1] + n2_weight)
        if new_cost < old_cost:
            nodes_cost[n2] = new_cost
            heapq.heappush(heap, (new_cost, n2))

    def select_min(self, heap):
        return

    def dijkstra(self):
        to_explore = {self.start: 0}
        heap = [(0, self.start)]
        heapq.heapify(heap)
        marked = set()
        while self.end not in to_explore:
            cost, node = heapq.heappop(heap)
            marked.add(node)
            for neighboor in self.neighboors(*node):
                if neighboor not in marked:
                    x, y = neighboor
                    weight = self.graph[y][x]
                    self.update_cost(node, neighboor, heap, to_explore, weight)
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

