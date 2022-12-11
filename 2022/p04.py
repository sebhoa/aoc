class P4(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 4)
        
    def inclus(self, x1, y1, x2, y2):
        return x1 <= x2 <= y2 <= y1 or x2 <= x1 <= y1 <= y2
    
    def overlap(self, x1, y1, x2, y2):
        return x1 <= x2 <= y1 or x2 <= x1 <= y2    
    
    def solve(self, part):
        critere = (self.inclus, self.overlap, self.inclus, self.overlap)[part]
        nb_paires = 0
        with open(self.tests[part]) as datas:
            for ligne in datas:
                pair_1, pair_2 = ligne.strip().split(',')
                min_1, max_1 = [int(e) for e in pair_1.split('-')]
                min_2, max_2 = [int(e) for e in pair_2.split('-')]
                if critere(min_1, max_1, min_2, max_2):
                    nb_paires += 1
        self.solutions[part] = nb_paires
