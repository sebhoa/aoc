WALL = '#'
FREE = '.'
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
DIRECTIONS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT}
TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}


class Laby:

    def __init__(self, walls, height, width):
        self.walls = walls
        self.height = height
        self.width = width
        
    def inside(self, position):
        i, j = position
        return 0 <= i < self.height and 0 <= j < self.width
    
    def is_free(self, position):
        return position not in self.walls
    
    def build_wall(self, position):
        self.walls.add(position)

    def break_wall(self, position):
        self.walls.remove(position)
    

class Guard:

    def __init__(self, laby, position, direction):
        self.laby = laby
        self.position = position
        self.direction = direction
        self.memory = {self.position}
        self.obstructions = set()
        self.initial = position, direction

    def turn(self):
        self.direction = TURN_RIGHT[self.direction]

    def have_a_look_ahead(self):
        i, j = self.position
        di, dj = self.direction
        return i+di, j+dj
            
    def forward(self, with_loop_test):
        """move guard one step (forward or turn right) and return True if guard is still inside the area
        if with_loop_test is True, a ghost is created with a modified version of the laby ; then guard 
        ask the ghost to patrol... if a loop is detected, position of the added wall is memorized
        """
        new_position = self.have_a_look_ahead()
        
        if not self.laby.inside(new_position):
            return False
        
        if not self.laby.is_free(new_position):
            self.turn()
            return True
            
        if with_loop_test:
            self.laby.build_wall(new_position)
            position, direction = self.initial
            ghost = Ghost(self.laby, position, direction)
            if ghost.patrol():
                self.obstructions.add(new_position)
            self.laby.break_wall(new_position)

        self.memory.add(new_position)
        self.position = new_position
        return True

    def patrol(self, with_loop_test=False):
        inside = True
        while inside:
            inside = self.forward(with_loop_test)

class Ghost(Guard):
    """A ghost is like a guard except that he memorize position and direction
    so he can detect a loop during patrol
    """

    def __init__(self, laby, position, direction):
        Guard.__init__(self, laby, position, direction)
        self.memory = {(position, direction)}

    def forward(self):
        new_position = self.have_a_look_ahead()
        
        if not self.laby.inside(new_position):
            return False, False
            
        if not self.laby.is_free(new_position):
            self.turn()
            return True, False
            
        self.position = new_position
        if (self.position, self.direction) in self.memory:
            return True, True
        else:
            self.memory.add((self.position, self.direction))
            return True, False

    def patrol(self):
        """for a ghost patrol's goal is to detect a loop"""
        inside, loop = True, False
        while inside and not loop:
            inside, loop = self.forward()
        return loop

            
class P6(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 6, part)
        self.laby = None
        self.guard = None
        
    def load(self, filename):
        walls = set()
        with open(filename) as datas:
            for i, line in enumerate(datas):
                for j in range(len(line)-1):
                    value = line[j]
                    if value in DIRECTIONS:
                        guard_position = i, j
                        guard_direction = DIRECTIONS[line[j]]
                    elif value == WALL:
                        walls.add((i, j))
        self.laby = Laby(walls, i+1, j+1)
        self.guard = Guard(self.laby, guard_position, guard_direction)

    def solve(self, filename):
        self.load(filename)
        if self.part == 0:
            self.guard.patrol(with_loop_test=False)
            self.solution = len(self.guard.memory)
        else:
            self.guard.patrol(with_loop_test=True)
            self.solution = len(self.guard.obstructions)