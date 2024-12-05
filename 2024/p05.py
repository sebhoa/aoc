class P5(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 5, part)
        self.lt = {}  # la partie 1 des données : les règles de précédences
        self.arrays = []  # la partie 2 des données la liste des update

    def reset(self):
        self.lt = {}
        self.arrays = []
        
    def load(self, filename):
        with open(filename) as datas:
            first_part = True
            for line in datas:
                if line == '\n':
                    first_part = False
                    continue
                if first_part:
                    small, big = [int(e) for e in line.strip().split('|')]
                    self.lt[small] = self.lt.get(small, set()) | {big}
                else:
                    self.arrays.append([int(e) for e in line.strip().split(',')])

    def before(self, a, b):
        return (a not in self.lt or b in self.lt[a]) and (b not in self.lt or a not in self.lt[b])
        
    def get_middle(self, array):
        n = len(array)
        middle = array[n//2]
        for i in range(n):
            for j in range(i+1, n):
                if not self.before(array[i], array[j]):
                    return 0
        return middle

    def count_greater(self, array):
        """pour chaque valeur du tableau, compte le nombre de valeurs
        qui lui sont imposées plus grandes dans les règles. C'est cette
        valeur qui va déterminer la place de la valeur dans une version
        correctement triée du tableau
        """
        n = len(array)
        greater_than = {a: 0 for a in array}
        for i in range(n):
            for j in range(n):
                if i != j and self.before(array[i], array[j]):
                    greater_than[array[i]] += 1
        return greater_than
    
    def solve(self, filename):
        self.reset()
        self.load(filename)
        self.solution = 0
        self.incorrects = []
        for array in self.arrays:
            m = self.get_middle(array)
            if m > 0:
                self.solution += m
            else:
                self.incorrects.append(array)
        if self.part == 1:
            self.solution = 0
            for array in self.incorrects:
                n = len(array)
                counts = self.count_greater(array)
                gt = sorted((k for k in counts), key=lambda e: counts[e], reverse=True)
                self.solution += gt[n//2]

def main():
    for part in (0, 1):
        pb = P5(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 