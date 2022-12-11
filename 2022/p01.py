class P1(Puzzle):
    
    def __init__(self):
        Puzzle.__init__(self, 1)
        
    def solve(self, part):
        energies = [0]
        with open(self.tests[part]) as datas:
            for ligne in datas:
                if ligne == '\n':
                    energies.append(0)
                else:
                    energies[-1] += int(ligne.strip())
        energies.sort(reverse=True)
        if part%2 == 0:
            self.solutions[part] = energies[0]
        else:
            self.solutions[part] = sum(energies[i] for i in range(3))