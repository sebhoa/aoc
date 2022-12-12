class P3(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 3, part)
        
    def priorite_lettre(self, lettre):
        code = ord(lettre)
        code_a = ord('a')
        code_A = ord('A')
        return code - code_A + 27 if code < code_a else code - code_a + 1
                    
    def solve_a(self, filename):
        total = 0
        with open(filename) as datas:
            for ligne in datas:
                m = len(ligne) // 2
                s = set(ligne[:m]) & set(ligne[m:-1])
                total += self.priorite_lettre(s.pop())
        return total
        
    def solve_b(self, filename):
        total = 0
        with open(filename) as datas:
            ligne = datas.readline()
            while ligne:
                s = set(ligne.strip())
                for _ in range(2):
                    s = s & set(datas.readline().strip())
                total += self.priorite_lettre(s.pop())
                ligne = datas.readline()
        return total
    
    def solve(self, filename):
        if self.part == 0:
            self.solution = self.solve_a(filename)
        else:
            self.solution = self.solve_b(filename)