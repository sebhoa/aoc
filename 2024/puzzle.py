"""
Les fichiers de données doivent être stockés dans 
datas/XX/XX_small_0.txt pour le fichier des données exemple du jour XX part 1
datas/XX/XX_big_0.txt pour le fichier des données réelles
on remplace _0.txt par _1.txt pour la partie 2
"""

class Puzzle:
    """Un puzzle c'est une id (entre 1 et 25), une part 0 (part one) ou 1 (part two)
    une solution un petit fichier de test et un gros fichier"""
    
    def __init__(self, num, part):
        self.id = num
        self.part = part
        self.solution = None
        self.test_in = f'datas/{num:02}/{num:02}_small_{part}.txt'
        self.validation_in = f'datas/{num:02}/{num:02}_big_{part}.txt'
        
    def solve(self, filename):
        """Chaque puzzle doit coder sa méthode de résolution"""
        pass
    
    def test(self, *args):
        """Teste la résolution sur le petit fichier"""
        self.solve(self.test_in, *args)
        
    def validate(self, *args):
        """Valide la solution sur le gros fichier"""
        self.solve(self.validation_in, *args)
    
    def __str__(self):
        part_test = ('One', 'Two')[self.part]
        s = f'Puzzle {self.id:02}\n'
        s += f'-- Part {part_test}\n'
        s += f'-- Solution: {self.solution}\n'
        return s
        