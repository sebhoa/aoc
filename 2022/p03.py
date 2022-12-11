class P3(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 3)
        
    def priorite_lettre(self, lettre):
        code = ord(lettre)
        code_a = ord('a')
        code_A = ord('A')
        return code - code_A + 27 if code < code_a else code - code_a + 1
                    
    def solve_a(self, part):
        total = 0
        with open(self.tests[part]) as datas:
            for ligne in datas:
                m = len(ligne) // 2
                s = set(ligne[:m]) & set(ligne[m:-1])
                total += self.priorite_lettre(s.pop())
        self.solutions[part] = total
        
    def solve_b(self, part):
        total = 0
        with open(self.tests[part]) as datas:
            ligne = datas.readline()
            while ligne:
                s = set(ligne.strip())
                for _ in range(2):
                    s = s & set(datas.readline().strip())
                total += self.priorite_lettre(s.pop())
                ligne = datas.readline()
        self.solutions[part] = total
    
    def solve(self, part):
        if part % 2 == 0:
            self.solve_a(part)
        else:
            self.solve_b(part)