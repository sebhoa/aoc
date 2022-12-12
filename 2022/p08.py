NORD = -1, 0
SUD = 1, 0
EST = 0, 1
OUEST = 0, -1

DIRECTIONS = NORD, EST, SUD, OUEST

class P8(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 8, part)
        self.grid = []
        self.height = 0
        self.width = 0
        
    def load_datas(self, filename):
        with open(filename) as datas:
            self.grid = [[int(e) for e in line.strip()] for line in datas]
        self.height = len(self.grid)
        self.width = len(self.grid[0])
        
    def inside(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width
    
    def on_edge(self, i, j):
        return i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1
    
    def neighbors(self, i, j, direction):
        """Un itérateur sur les voisins de i, j dans la direction donnée, en restant dans la zone"""
        di, dj = direction
        i, j = i + di, j + dj
        while self.inside(i, j):
            yield i, j
            i, j = i + di, j + dj
            
    def visible_from(self, i0, j0, direction):
        """Renvoie True si la case intérieure i0, j0 est visible depuis la direction donnée"""
        for i, j in self.neighbors(i0, j0, direction):
            if self.grid[i][j] >= self.grid[i0][j0]:
                return False
        return True
        
    def on_direction_scenic_score(self, i0, j0, direction):
        """Calcule la valeur scénique de la case intérieure i0, j0 dans une direction donnée"""
        di, dj = direction
        i, j = i0 + di, j0 + dj 
        scenic_score = 1
        while self.inside(i, j) and self.grid[i][j] < self.grid[i0][j0]:
            scenic_score += 1
            i, j = i + di, j + dj
        if not self.inside(i, j):
            scenic_score -= 1
        return scenic_score
        
    def visible(self, i, j):
        return self.on_edge(i, j) or any(self.visible_from(i, j, d) for d in DIRECTIONS)

    def scenic_score(self, i, j):
        prod = 1
        for d in DIRECTIONS:
            prod *= self.on_direction_scenic_score(i, j, d)
        return prod
            
    def solve(self, filename):
        self.load_datas(filename)
        if self.part == 0:
            self.solution = sum(self.visible(i, j) for i in range(self.height) for j in range(self.width))
        else:
            self.solution = max(self.scenic_score(i, j) for i in range(1, self.height-1) for j in range(1, self.width-1))
        print(self)
    
    
    