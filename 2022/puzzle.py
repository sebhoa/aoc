class Puzzle:
    """Un puzzle c'est une id (entre 1 et 25), une part 0 (part one) ou 1 (part two)
    une solution un petit fichier de test et un gros fichier"""
    
    def __init__(self, num, part):
        self.id = num
        self.part = part
        self.solution = None
        self.test_in = f'{num:02}_small.txt'
        self.validation_in = f'{num:02}_big.txt'
        
    def solve(self, filename):
        """Chaque puzzle doit coder sa méthode de résolution"""
        pass
    
    def test(self):
        """Teste la résolution sur le petit fichier"""
        self.solve(self.test_in)
        
    def validate(self):
        """Valide la solution sur le gros fichier"""
        self.solve(self.validation_in)
    
    def __str__(self):
        part_test = ('One', 'Two')[self.part]
        s = f'Puzzle {self.id:02}\n'
        s += f'-- Part {part_test}\n'
        s += f'-- Solution: {self.solution}\n'
        return s
        