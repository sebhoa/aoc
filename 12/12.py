import sys
import collections

FILE = 'input12.txt'
START = 'start'
END = 'end'

class Graph:

    def __init__(self, filename):
        self.filename = filename
        self.adj = {}  # listes d'adjacences
        self.paths = []
    
    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for data in datas:
                node_1, node_2 = data.strip().split('-')
                if node_2 != START:
                    self.adj[node_1] = self.adj.get(node_1, set()) | {node_2}
                if node_1 != START:
                    self.adj[node_2] = self.adj.get(node_2, set()) | {node_1}
            self.adj[END] = set()

    def add_new_path(self, l_path):
        self.paths.append(','.join(l_path))

    def control_version_1(self, s, a_path, locked):
        return s.isupper() or s not in a_path, locked

    def control_version_2(self, s, a_path, locked):
        count = a_path.count(s)
        if s.isupper():
            return True, locked
        elif count > 1:
            return False, locked
        elif count == 1:
            return not locked, True
        elif count == 0:
            return True, locked

    def explore(self, control_function):
        paths = collections.deque([([START],False)])
        while paths:
            a_path, locked = paths.popleft()
            last_node = a_path[-1]
            if last_node == END:
                self.add_new_path(a_path)
            else:
                for s in self.adj[last_node]:
                    can_be_added, new_locked = control_function(s, a_path, locked)
                    if can_be_added:
                        new_path = a_path.copy()
                        new_path.append(s)
                        paths.append((new_path, new_locked))

    def solve(self):
        self.load()
        self.explore(self.control_version_1)
        
    def solve_two(self):
        self.load()
        self.explore(self.control_version_2)

def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    graph = Graph(fichier)
    if version == '1':
        graph.solve()
        print(len(graph.paths))
    else:
        graph.solve_two()
        print(len(graph.paths))

if __name__ == '__main__':
    main() 