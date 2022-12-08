NORD = -1, 0
SUD = 1, 0
EST = 0, 1
OUEST = 0, -1

DIRECTIONS = NORD, EST, SUD, OUEST

class P8(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 8)
        self.grille = []
        self.height = 0
        self.width = 0
        
    def load_datas(self, part, filename=None):
        if filename is None:
            filename = self.tests[part]
        with open(filename) as datas:
            self.grille = [[int(e) for e in ligne.strip()] for ligne in datas]
        self.height = len(self.grille)
        self.width = len(self.grille[0])
        
    def inside(self, i, j):
        return 0 <= i < self.height and 0 <= j < self.width
    
    def bordure(self, i, j):
        return i == 0 or i == self.height - 1 or j == 0 or j == self.width - 1
    
    def visible_depuis(self, i0, j0, direction):
        """Renvoie True si la case intérieure i0, j0 est visible depuis la direction donnée"""
        di, dj = direction
        i, j = i0, j0 
        est_visible = True
        while self.inside(i, j) and est_visible:
            i, j = i + di, j + dj
            est_visible = not self.inside(i, j) or self.grille[i][j] < self.grille[i0][j0]
        return est_visible
        
    def scenic_score_une_dir(self, i0, j0, direction):
        """Calcule la valeur scénique de la case intérieure i0, j0 dans une direction donnée"""
        di, dj = direction
        i, j = i0 + di, j0 + dj 
        scenic_score = 1
        while self.inside(i, j) and self.grille[i][j] < self.grille[i0][j0]:
            scenic_score += 1
            i, j = i + di, j + dj
        if not self.inside(i, j):
            scenic_score -= 1
        return scenic_score
        
    def visible(self, i, j):
        return self.bordure(i, j) or any(self.visible_depuis(i, j, d) for d in DIRECTIONS)

    def scenic_score(self, i, j):
        prod = 1
        for d in DIRECTIONS:
            prod *= self.scenic_score_une_dir(i, j, d)
        return prod
            
    def solve(self, part, filename=None):
        self.load_datas(part, filename)
        if part % 2 == 0:
            self.solutions[part] = sum(self.visible(i, j) for i in range(self.height) for j in range(self.width))
        else:
            self.solutions[part] = max(self.scenic_score(i, j) for i in range(1, self.height-1) for j in range(1, self.width-1))
    
    
    
    