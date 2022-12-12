PIERRE = 0
FEUILLE = 1
CISEAUX = 2

POINTS = (0, 3, 6)

class P2(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 2, part)
        self.part = part
        
    def str_vers_int(self, coup: str):
        if coup in 'XA':
            return PIERRE
        if coup in 'YB':
            return FEUILLE
        if coup in 'ZC':
            return CISEAUX
    
    def shape_score(self, coup):
        return coup + 1
    
    def result_score(self, resultat):
        return POINTS[resultat]
    
    def result(self, mon_coup: int, son_coup: int):
        """renvoie 0 si mon_coup perd contre son_coup,
        2 si mon_coup gagne et 1 en cas d'égalité
        """
        if mon_coup == (son_coup + 1) % 3:
            return 2
        elif mon_coup == son_coup:
            return 1
        else:
            return 0
        
    def mon_choix(self, son_coup, resultat):
        if resultat == 0:
            return (son_coup - 1) % 3
        elif resultat == 1:
            return son_coup
        else:
            return (son_coup + 1) % 3
        
    def solve(self, filename):
        score = 0
        with open(filename) as datas:
            for ligne in datas:
                son_coup, info_2 = [self.str_vers_int(c) for c in ligne.split()]
                if self.part == 0:
                    mon_coup = info_2
                    resultat = self.result(mon_coup, son_coup)
                else:
                    resultat = info_2
                    mon_coup = self.mon_choix(son_coup, resultat)
                score += self.shape_score(mon_coup) + self.result_score(resultat)
        self.solution = score        
            
