FREE = '.'

class Map:

    def __init__(self):
        self.width = 0
        self.height = 0
        self.antennas = {}
        self.antinodes = set()

    def set_size(self, h, w):
        self.width = w
        self.height = h

    def inside(self, position):
        i, j = position
        return 0 <= i < self.height and 0 <= j < self.width
    
    def add_antenna(self, frequency, i, j):
        position = i, j
        if frequency in self.antennas:
            self.antennas[frequency].append(Antenna(self, frequency, position))
        else:
            self.antennas[frequency] = [Antenna(self, frequency, position)]

    def calculate_antinodes(self, only_one):
        for freq in self.antennas:
            antennas = self.antennas[freq]
            for antenna_1 in antennas:
                for antenna_2 in antennas:
                    if antenna_1 != antenna_2:
                        self.antinodes |= antenna_1.calculate_antinodes(antenna_2, only_one)
        

class Antenna:

    def __init__(self, the_map, frequency, position):
        self.map = the_map
        self.position = position
        self.frequency = frequency

    def __eq__(self, antenna):
        return self.position == antenna.position

    def calculate_antinodes(self, antenna, only_one):
        antinodes = set()
        i1, j1 = self.position
        i2, j2 = antenna.position
        di, dj = i1 - i2, j1 - j2
        if only_one:
            antinode = 2*i1 - i2, 2*j1 - j2
            if self.map.inside(antinode):
                antinodes.add(antinode)
        else:    
            k = 0
            antinode = i1 + k*di, j1 + k*dj
            while self.map.inside(antinode):
                antinodes.add(antinode)
                k += 1
                antinode = i1 + k*di, j1 + k*dj
        return antinodes


class P8(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 8, part)
        self.map = Map()

    def reset(self):
        self.map = Map()
    
    def load(self, filename):
        self.reset()
        with open(filename) as datas:
            for i, line in enumerate(datas):
                for j, value in enumerate(line.strip()):
                    if value != FREE:
                        self.map.add_antenna(value, i, j)
            self.map.set_size(i+1, j+1)

    def solve(self, filename):
        self.load(filename)
        only_one = self.part == 0
        self.map.calculate_antinodes(only_one)
        self.solution = len(self.map.antinodes)

def main():
    for part in (0, 1):
        pb = P8(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 