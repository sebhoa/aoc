class P1(Puzzle):
    
    def __init__(self, part):
        Puzzle.__init__(self, 1, part)
        
    def solve(self, filename):
        energies = [0]
        with open(filename) as datas:
            for ligne in datas:
                if ligne == '\n':
                    energies.append(0)
                else:
                    energies[-1] += int(ligne.strip())
        energies.sort(reverse=True)
        if self.part == 0:
            self.solution = energies[0]
        else:
            self.solution = sum(energies[i] for i in range(3))