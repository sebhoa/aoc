from collections import deque

SPACE = '.'
WALL = '#'
BOX = 'O'
ROBOT = '@'
LEFT_SIDE = '['
RIGHT_SIDE = ']'

MOVEMENT = {'^': (-1, 0), 'v': (1, 0), '<': (0, -1), '>': (0, 1)}
REVERSED = {LEFT_SIDE: RIGHT_SIDE, RIGHT_SIDE: LEFT_SIDE}

DIRECTION = {LEFT_SIDE: '>', RIGHT_SIDE: '<'}

    
class Robot:

    def __init__(self, warehouse, position, moves=''):
        self.warehouse = warehouse
        self.position = position
        self.moves = moves

    def add_moves(self, moves):
        self.moves = moves
    
    def cell_ahead(self, position, direction):
        di, dj = MOVEMENT[direction]
        return position[0] + di, position[1] + dj

    def dual_position(self, position, content):
        return self.cell_ahead(position, DIRECTION[content])
    
    def step(self, direction):
        new_position = self.cell_ahead(self.position, direction)
        content = self.warehouse.content(new_position)
        if content == SPACE:
            self.warehouse.mark(self.position, SPACE)
            self.warehouse.mark(new_position, ROBOT)
            self.position = new_position
        elif content == BOX:
            current_position = new_position
            while self.warehouse.content(current_position) == BOX:
                current_position = self.cell_ahead(current_position, direction)
            if self.warehouse.content(current_position) == SPACE:
                self.warehouse.mark(self.position, SPACE)
                self.warehouse.mark(new_position, ROBOT)
                self.warehouse.mark(current_position, BOX)
                self.position = new_position

    def step_2(self, direction):
        new_position = self.cell_ahead(self.position, direction)
        content = self.warehouse.content(new_position)
        if content == SPACE:
            self.warehouse.mark(self.position, SPACE)
            self.warehouse.mark(new_position, ROBOT)
            self.position = new_position
        elif content in '[]':
            if direction in '<>':
                robot_moved = self.horizontal_move(direction, new_position, content)    
            else:
                dual = self.dual_position(new_position, content)
                double_position = new_position + (dual[1],)
                robot_moved = self.vertical_move(direction, double_position)
            if robot_moved:
                self.warehouse.mark(new_position, ROBOT)
                self.position = new_position            

    def horizontal_move(self, direction, new_position, content):
        i = new_position[0]
        current_position = new_position
        while self.warehouse.content(current_position) not in (SPACE, WALL):
            current_position = self.cell_ahead(current_position, direction)
        if self.warehouse.content(current_position) == SPACE:
            self.warehouse.mark(self.position, SPACE)
            self.warehouse.mark(new_position, ROBOT)
            if direction == '>':
                last = RIGHT_SIDE 
                intervalle = range(new_position[1]+1, current_position[1])
            else:
                last = LEFT_SIDE 
                intervalle = range(current_position[1]+1, new_position[1])
            self.warehouse.mark(current_position, last)
            for j in intervalle:
                self.warehouse.switch((i, j))
            return True
        else:
            return False

    def get_all_positions(self, double_position, direction):
        to_examine = deque([double_position])
        positions = set()
        while len(to_examine) > 0:
            i, j, k = to_examine.popleft()
            if j > k:
                j, k = k, j
            for p in ((i, j), (i, k)):
                positions.add(p)
                next_position = self.cell_ahead(p, direction)
                content = self.warehouse.content(next_position) 
                if content == WALL:
                    return set()
                if content != SPACE:
                    dual = self.dual_position(next_position, content)
                    to_examine.append(next_position + (dual[1],))
        positions.add(self.position)
        return positions
                    
    def modify(self, positions, direction):
        memory = {p: self.warehouse.content(p) for p in positions}
        for p in positions:
            next_p = self.cell_ahead(p, direction)
            memory[next_p] = self.warehouse.content(next_p)
        for p in positions:
            self.warehouse.mark(p, SPACE)
        for p in positions:
            next_p = self.cell_ahead(p, direction)
            self.warehouse.mark(next_p, memory[p])
        
            
    def vertical_move(self, direction, double_position):
        positions = self.get_all_positions(double_position, direction)
        if len(positions) == 0:
            return False
        self.modify(positions, direction)
        return True

    def move(self, part):
        action = self.step if part == 0 else self.step_2
        for direction in self.moves:
            action(direction)
        

class Warehouse:

    def __init__(self):
        self.height = 0
        self.width = 0
        self.grid = {}

    def __str__(self):
        return '\n'.join(''.join(self.content((i, j)) for j in range(self.width)) for i in range(self.height))
    
    def size(self, height, width):
        self.height = height
        self.width = width
    
    def content(self, position):
        return self.grid[position]

    def mark(self, position, value):
        self.grid[position] = value

    def switch(self, position):
        self.grid[position] = REVERSED[self.grid[position]]
    
    def gps_coordinate(self):
        return sum(100 * i + j for i in range(self.height) for j in range(self.width) if self.grid[i, j] in (LEFT_SIDE, BOX))


class P15(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 15, part)
        self.warehouse = None
        self.robot = None
    
    def load(self, filename):
        self.warehouse = Warehouse()
        with open(filename) as datas:
            for i, line in enumerate(datas):
                if line == '\n':
                    break
                else:
                    for j, v in enumerate(line.strip()):
                        self.warehouse.grid[i, j] = v
                        if v == ROBOT:
                            self.robot = Robot(self.warehouse, (i, j))
            self.warehouse.size(i, j+1)
            self.robot.add_moves(datas.readline().strip())                   
                
    def solve(self, filename):
        self.load(filename)
        self.robot.move(self.part)
        self.solution = self.warehouse.gps_coordinate()

def main():
    for part in (0, 1):
        pb = P15(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 