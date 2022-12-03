import sys

FILE = 'input11.txt'
CRITICAL = 10
EMPTY = 0
MAX_STEPS = 100
DELTAS = (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0)

class Octopuss:

    def __init__(self, line_id, col_id, energy):
        self.line_id = line_id
        self.col_id = col_id
        self.energy = energy

    def pos(self):
        return self.line_id, self.col_id

    def energy_up(self):
        self.energy = min(self.energy+1, CRITICAL)

    def critical(self):
        return self.energy == CRITICAL

    def flash(self):
        self.energy = EMPTY

class Colony:

    def __init__(self, filename):
        self.filename = filename
        self.width = 0
        self.height = 0
        self.octopusses = {}  # dictionnaire des octopuss
        self.nb_flashes = 0
        self.flash_positions = set() # positions where octopuss is ready to flash

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            self.octopusses = [[Octopuss(l, c, int(data)) for c,data in enumerate(line.strip())] for l,line in enumerate(datas)]
            self.height = len(self.octopusses)
            self.width = len(self.octopusses[0])
    
    def __str__(self):
        s = ''
        for line_id in range(self.height):
            for col_id in range(self.width):
                octo = self.octo((line_id, col_id))
                s += '+' if octo.critical() else str(octo.energy) 
            s += '\n'
        return s

    def inside(self, x, y):
        return 0 <= x < self.height and 0 <= y < self.width
    
    def coords(self):
        return ((line_id, col_id) for line_id in range(self.height) for col_id in range(self.width))

    def octo(self, position):
        line_id, col_id = position
        return self.octopusses[line_id][col_id]

    def neighboors(self, x, y):
        """iterateur d'octopuss voisins d'une position donnée"""
        return (self.octo((x+dx, y+dy)) for dx, dy in DELTAS if self.inside(x+dx, y+dy))

    def energy_up(self):
        for position in self.coords():
            octopuss = self.octo(position)
            octopuss.energy_up()
            if octopuss.critical():
                self.flash_positions.add(position)

    def flash(self):
        """propage l'effet du flash"""
        just_flashed = set()
        while self.flash_positions:
            position = self.flash_positions.pop()
            octopuss = self.octo(position)
            octopuss.flash()
            self.nb_flashes += 1
            just_flashed.add(position)
            for neighboord in self.neighboors(*position):
                if neighboord.pos() not in just_flashed:
                    neighboord.energy_up()
                    if neighboord.critical():
                        self.flash_positions.add(neighboord.pos())

    def step(self):
        self.energy_up()
        self.flash()
        
    def all_flash(self):
        """pour partie 2"""
        return all(self.octo(position).energy == EMPTY for position in self.coords())

    def solve(self, nb_steps=None):
        self.load()
        if nb_steps is None:
            count = 0
            while not self.all_flash():
                self.step()
                count += 1
        else:
            for i in range(nb_steps):
                self.step()
            count = self.nb_flashes
        return count


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    colony = Colony(fichier)
    if version == '1':
        print(colony.solve(MAX_STEPS))
    else:
        print(colony.solve())


if __name__ == '__main__':
    main() 
