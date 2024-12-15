from collections import deque

UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)

TURN_LEFT = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
U_TURN = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}

DIRECTIONS = UP, RIGHT, DOWN, LEFT

class Region:

    def __init__(self, point, plant):
        self.plant = plant
        self.first = point
        self.points = {point}
        self.borders = 0
        self.sides = 0
        self.surrounded_regions = []

    def __str__(self):
        s = f'{self.plant}: '
        s += '-'.join(f"{pt}" for pt in self.points)
        s += f' A{self.surface()}  P{self.perimeter()} C{self.sides}'
        return s

    def __eq__(self, region):
        return self.plant == region.plant and self.points == region.points

    def inside(self, point):
        return point in self.points
    
    def perimeter(self):
         return self.borders

    def surface(self):
        return len(self.points)

    def sides_count(self):
        return self.sides
    
    def price(self, by_side=False):
        second_parameter = self.sides_count() if by_side else self.perimeter()
        return self.surface() * second_parameter
    
    def neighbors(self, pt):
        i, j = pt
        return {(i+di, j+dj) for di, dj in DIRECTIONS}

    def internal(self, point):
        return point in self.points and all(p in self.points for p in self.neighbors(point))
    
    def forward(self, point, direction):
        i, j = point
        di, dj = direction
        return i + di, j + dj

    def surrounded_point(self, point):
        return any(point in region.points for region in self.surrounded_regions)
    
    def external_wall_on_the_right(self, point, direction):
        on_the_right = self.forward(point, TURN_RIGHT[direction])
        return not self.inside(on_the_right) and not self.surrounded_point(on_the_right)

    def wall_ahead(self, point, direction):
        ahead = self.forward(point, direction)
        return not self.inside(ahead)

    def a_wall_with_surrounded(self, point, direction):
        ahead = self.forward(point, direction)
        for region in self.surrounded_regions:
            if ahead in region.points:
                return True
        return False

    def put_an_external_wall_on_the_right(self, point):
        for direction in DIRECTIONS: 
            if self.external_wall_on_the_right(point, direction) and not self.wall_ahead(point, direction):
                return direction 

    def border_points(self):
        considered_points = self.points.copy()
        for region in self.surrounded_regions:
            considered_points |= region.points
        border = {pt for pt in self.points if any(p not in considered_points for p in self.neighbors(pt))}
        return border
    
    def count_sides(self):
        if self.surface() < 3:
            self.sides = 4
        else:
            external_points = self.border_points()
            while len(external_points) > 0:
                for first_point in external_points:   
                    first_direction = self.put_an_external_wall_on_the_right(first_point)
                    if first_direction is not None:
                        break
                point, direction = first_point, first_direction
                first_step = True
                while first_step or (point, direction) != (first_point, first_direction): 
                    first_step = False
                    if not self.wall_ahead(point, direction) or self.a_wall_with_surrounded(point, direction):
                        point = self.forward(point, direction)
                        if self.external_wall_on_the_right(point, direction):
                            external_points.discard(point)
                        else:
                            direction = TURN_RIGHT[direction]
                            point = self.forward(point, direction)
                            external_points.discard(point)
                            self.sides += 1
                    else:
                        direction = TURN_LEFT[direction]
                        if self.external_wall_on_the_right(point, direction):
                            self.sides += 1
            
        
    def update_sides(self, value):
        self.sides += value
    
    def add_point(self, point):
        self.points.add(point)

    def add_border(self):
        self.borders += 1

    def add_surrounded(self, region):
        self.surrounded_regions.append(region)
        
    def surrounded_by(self, region):
        for point in self.points:
            if not self.internal(point) and any(p not in region.points for p in self.neighbors(point)):
                return False
        return True
    

class Garden:

    def __init__(self, height, width, plants):
        self.plants = plants
        self.height = height
        self.width = width
        self.regions = {}

    def inside(self, point):
        i, j = point
        return 0 <= i < self.height and 0 <= j < self.width
    
    def new_region(self, point, plant, other_points):
        new_region = Region(point, plant)
        queue = deque([(point, plant)])
        seen = set()
        while len(queue) > 0:
            pt, _ = queue.popleft()
            seen.add((pt, plant))
            new_region.add_point(pt)
            other_points.discard((pt, plant))
            for di, dj in DIRECTIONS:
                new_point = pt[0] + di, pt[1] + dj
                if self.inside(new_point) and self.plants[new_point] == plant:
                    if (new_point, plant) not in queue and (new_point, plant) not in seen:
                        queue.append((new_point, plant))
                else:
                    new_region.add_border()
        self.regions[point] = new_region
                        
    def fill(self):
        points_to_examine = set(self.plants.items())
        while len(points_to_examine) > 0:
            point, plant = points_to_examine.pop()
            self.new_region(point, plant, points_to_examine)

    def surrounded_regions(self, region):
        for other in self.regions.values():
            if other != region and other.surrounded_by(region):
                region.add_surrounded(other)
                
    def count_sides(self):
        for region in self.regions.values():
            self.surrounded_regions(region)
            region.count_sides()
        for region in self.regions.values():
            for reg in region.surrounded_regions:
                region.update_sides(reg.sides)
        

class P12(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 12, part)
        self.garden = None  # a collection of regions
    
    def load(self, filename):
        plants = {}
        with open(filename) as datas:
            for i, line in enumerate(datas):
                for j, plant in enumerate(line.strip()):
                    plants[i, j] = plant
        self.garden = Garden(i+1, j+1, plants)
        
    def solve(self, filename):
        self.load(filename)
        self.garden.fill()
        if self.part == 0:
            self.solution = sum(region.price() for region in self.garden.regions.values())
        else:
            self.garden.count_sides()
            self.solution = sum(region.price(by_side=True) for region in self.garden.regions.values())

def main():
    for part in (0, 1):
        pb = P12(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 