class P4(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 4, part)
        
    def inclus(self, x1, y1, x2, y2):
        return x1 <= x2 <= y2 <= y1 or x2 <= x1 <= y1 <= y2
    
    def overlap(self, x1, y1, x2, y2):
        return x1 <= x2 <= y1 or x2 <= x1 <= y2    
    
    def solve(self, filename):
        critere = self.inclus if self.part == 0 else self.overlap
        nb_paires = 0
        with open(filename) as datas:
            for ligne in datas:
                pair_1, pair_2 = ligne.strip().split(',')
                min_1, max_1 = [int(e) for e in pair_1.split('-')]
                min_2, max_2 = [int(e) for e in pair_2.split('-')]
                if critere(min_1, max_1, min_2, max_2):
                    nb_paires += 1
        self.solution = nb_paires
