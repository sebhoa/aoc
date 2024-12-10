HIGHEST = 9
LOWEST = 0

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
DIRECTIONS = UP, RIGHT, DOWN, LEFT


class TrailHead:

    def __init__(self, start, end):
        self.start = start
        self.ends = {end}
        self.rating = 1

    def __str__(self):
        return f'{self.start}: {self.ends}'
    
    def add_end(self, end):
        self.ends.add(end)
        self.rating += 1

    def score(self):
        return len(self.ends)


class Map:

    def __init__(self, grid, height, width):
        self.grid = grid
        self.height = height
        self.width = width

    def new_position(self, position, direction):
        i, j = position
        di, dj = direction
        return i+di, j+dj
    
    def inside(self, position):
        i, j = position
        return 0 <= i < self.height and 0 <= j < self.width

    def lowest(self, position):
        return self.grid[position] == LOWEST


class P10(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 10, part)
        self.map = None    # all map informations
        self.ends = set()  # set of all highest points
        self.trails = {}   # {zero_point: TrailHead starting at this point, ...}
    
    def load(self, filename):
        grid = {}
        ends = set()
        with open(filename) as datas:
            for i, data in enumerate(datas):
                for j, height in enumerate(data.strip()):
                    height = int(height)
                    grid[i, j] = height
                    if height == HIGHEST:
                        ends.add((i, j))
        self.map = Map(grid, i+1, j+1)
        self.ends = ends
        self.trails = {}
    
    def reverse_path_from(self, end):
        paths = [[(end, self.map.grid[end])]]
        while paths != []:
            path = paths.pop()
            position, height = path[-1]
            if self.map.lowest(position):
                if position in self.trails:
                    self.trails[position].add_end(end)
                else:
                    self.trails[position] = TrailHead(position, end)
            else:
                for direction in DIRECTIONS:
                    new_path = path.copy()
                    new_position = self.map.new_position(position, direction)
                    if self.map.inside(new_position) and self.map.grid[new_position] == height - 1:
                        new_path.append((new_position, self.map.grid[new_position]))
                        paths.append(new_path)
    
    def paths_to_start(self):
        for end in self.ends:
            self.reverse_path_from(end)
            
    def solve(self, filename):
        self.load(filename)
        self.paths_to_start()
        if self.part == 0:
            self.solution = sum(trailhead.score() for trailhead in self.trails.values())
        else:
            self.solution = sum(trailhead.rating for trailhead in self.trails.values())


def main():
    for part in (0, 1):
        pb = P10(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 