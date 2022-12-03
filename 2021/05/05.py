import sys


FILE = 'input05.txt'

class Segment:

    def __init__(self, point_a, point_b):
        self.A = point_a
        self.B = point_b

    def __str__(self):
        xA, yA = self.A
        xB, yB = self.B
        return f'{xA},{yA} -> {xB},{yB}'

    def horizontal(self):
        return self.A[1] == self.B[1]

    def vertical(self):
        return self.A[0] == self.B[0]

    def oblique(self):
        xA, yA = self.A
        xB, yB = self.B
        return abs(xA - xB) == abs(yA - yB)

    def direction(self):
        xA, yA = self.A
        xB, yB = self.B
        if self.horizontal():
            dx = (xB - xA) // abs(xB - xA)
            dy = 0
        elif self.vertical():
            dx = 0
            dy = (yB - yA) // abs(yB - yA)
        elif self.oblique():
            dx = (xB - xA) // abs(xB - xA)
            dy = (yB - yA) // abs(yB - yA)
        else:
            dx, dy = None, None
        return dx, dy

    def mark(self, final_count):
        dx, dy = self.direction()
        if dx == 0 or dy == 0:
            x, y = self.A
            while (x, y) != self.B:
                final_count[x,y] = final_count.get((x,y), 0) + 1
                x, y = x+dx, y+dy
            final_count[x,y] = final_count.get((x,y), 0) + 1

    def mark_two(self, final_count):
        dx, dy = self.direction()
        if dx is not None:
            x, y = self.A
            while (x, y) != self.B:
                final_count[x,y] = final_count.get((x,y), 0) + 1
                x, y = x+dx, y+dy
            final_count[x,y] = final_count.get((x,y), 0) + 1

class Zone:

    def __init__(self, filename):
        self.filename = filename
        self.segments = []

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for line in datas:
                vecteurs = line.strip().split('->')
                point_a = tuple(int(e) for e in vecteurs[0].split(','))
                point_b = tuple(int(e) for e in vecteurs[1].split(','))
                self.segments.append(Segment(point_a, point_b))

    def solve(self):
        self.load()
        final_count = {}
        for seg in self.segments:
            seg.mark(final_count)
        return sum(final_count[pt] > 1 for pt in final_count)

    def solve_two(self):
        self.load()
        final_count = {}
        for seg in self.segments:
            seg.mark_two(final_count)
        return sum(final_count[pt] > 1 for pt in final_count)

def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    zone = Zone(fichier)
    if version == '1':
        print(zone.solve())
    else:
        print(zone.solve_two())

if __name__ == '__main__':
    main()   



