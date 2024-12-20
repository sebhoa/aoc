import re

NW = (True, True)
NE = (True, False)
SW = (False, True)
SE = (False, False)

ROBOT_REGEX = r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)"

class Robot:

    def __init__(self, the_map, position, velocity):
        self.map = the_map
        self.position = position
        self.velocity = velocity

    def forward(self):
        x, y = self.position
        vx, vy = self.velocity
        self.position = (x + vx) % self.map.width, (y + vy) % self.map.height


class Map:

    def __init__(self, width, height):
        self.height = height
        self.width = width
        self.middle_y = height // 2 if height%2 == 1 else height // 2 - 0.5
        self.middle_x = width // 2 if width%2 == 1 else width // 2 - 0.5
        self.robots = []

    def __str__(self):
        grid = [[0] * self.width for _ in range(self.height)]
        for robot in self.robots:
            x, y = robot.position
            grid[y][x] += 1
        return '\n'.join(''.join(str(e) if e > 0 else '.' for e in line) for line in grid)
    
    def add_robot(self, position, velocity):
        self.robots.append(Robot(self, position, velocity))

    def steps(self, seconds=1):
        for _ in range(seconds):
            for robot in self.robots:
                robot.forward()

    def only_ones(self):
        seen = set()
        for robot in self.robots:
            if robot.position in seen:
                return False
            else:
                seen.add(robot.position)
        return True
    
    def safety_factor(self):
        counts = {NW: 0, NE: 0, SW: 0, SE: 0}
        for robot in self.robots:
            x, y = robot.position
            if x != self.middle_x and y != self.middle_y:
                quarter = (x < self.middle_x, y < self.middle_y)
                counts[quarter] += 1
        factor = 1
        for q in (NW, NE, SW, SE):
            factor *= counts[q]
        return factor
        

class P14(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 14, part)
        self.map = None
    
    def load(self, filename):
        with open(filename) as datas:
            w, h = datas.readline().split()
            self.map = Map(int(w), int(h))
            for line in datas:
                x, y, vx, vy = re.findall(ROBOT_REGEX, line)[0]
                position = int(x), int(y)
                velocity = int(vx), int(vy)
                self.map.add_robot(position, velocity)
        
    def solve(self, filename):
        self.load(filename)
        if self.part == 0:
            seconds = 100
            self.map.steps(seconds)
            self.solution = self.map.safety_factor()        
        else:
            self.solution = 0
            while not self.map.only_ones():
                self.solution += 1
                self.map.steps()            

def main():
    for part in (0, 1):
        pb = P14(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 