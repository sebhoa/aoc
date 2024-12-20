from collections import deque

NORTH = (-1, 0)
SOUTH = (1, 0)
EAST = (0, 1)
WEST = (0, -1)

TURN_LEFT = {NORTH: WEST, WEST: SOUTH, SOUTH: EAST, EAST: NORTH}
TURN_RIGHT = {NORTH: EAST, EAST: SOUTH, SOUTH: WEST, WEST: NORTH}

TURN_COST = 1000
FORWARD_COST = 1

ROBOT = {NORTH: '^', SOUTH: 'v', EAST: '>', WEST: '<'}

WALL = '#'
SPACE = '.'
        

class Maze:

    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end

    def __str__(self):
        return '\n'.join(''.join(v for v in line) for line in self.grid)
    
    def forward(self, position, direction):
        i, j = position
        di, dj = direction
        return (i+di, j+dj), direction, FORWARD_COST

    def turn_left(self, position, direction):
        return position, TURN_LEFT[direction], TURN_COST

    def turn_right(self, position, direction):
        return position, TURN_RIGHT[direction], TURN_COST

    def content(self, position):
        i, j = position
        return self.grid[i][j]
    
    def is_wall(self, position):
        i, j = position
        return self.grid[i][j] == WALL

    def already_in(self, position, direction, cost, paths):
        if position not in paths:
            return False
        for d, c in paths[position]:
            if direction == d and c < cost:
                return True
        return False 
    
    def lowest_cost(self):
        partial_paths = deque([([self.start], EAST, 0)])
        seen = {}
        costs = {}
        while len(partial_paths) > 0:
            positions, direction, cost = partial_paths.popleft()
            position = positions[-1]
            if position in seen:
                seen[position].add((direction, cost))
            else:
                seen[position] = {(direction, cost)}
            if position == self.end:
                if cost in costs:
                    costs[cost] |= set(positions)
                else:
                    costs[cost] = set(positions)
            else:
                for action in (self.turn_left, self.turn_right, self.forward):
                    new_position, new_direction, step_cost = action(position, direction)
                    if (not self.is_wall(new_position) and 
                        not self.already_in(new_position, new_direction, cost+step_cost, seen)):
                        new_positions = positions.copy()
                        new_positions.append(new_position)
                        partial_paths.append((new_positions, new_direction, cost+step_cost))
        return costs
                

class P16(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 16, part)
        self.maze = None
    
    def load(self, filename):
        grid = []
        start, end = None, None
        with open(filename) as datas:
            for i, line in enumerate(datas):
                grid.append([])
                for j, v in enumerate(line.strip()):
                    grid[-1].append(v)
                    if v == 'S':
                        start = i, j
                    elif v == 'E':
                        end = i, j
        self.maze = Maze(grid, start, end)
                
    def solve(self, filename):
        self.load(filename)
        costs = self.maze.lowest_cost()
        min_costs = min(costs.keys())
        if self.part == 0:
            self.solution = min_costs
        else:
            self.solution = len(costs[min_costs])

def main():
    for part in (0, 1):
        pb = P16(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 