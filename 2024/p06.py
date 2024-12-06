WALL = '#'
FREE = '.'
OBSTACLE = 'O'
UP = (-1, 0)
RIGHT = (0, 1)
DOWN = (1, 0)
LEFT = (0, -1)
DIRECTIONS = {'^': UP, '>': RIGHT, 'v': DOWN, '<': LEFT}
TURN_RIGHT = {UP: RIGHT, RIGHT: DOWN, DOWN: LEFT, LEFT: UP}
TURN_LEFT = {UP: LEFT, LEFT: DOWN, DOWN: RIGHT, RIGHT: UP}
LABELS = {UP: '^', RIGHT: '>', DOWN: 'v', LEFT: '<'}


class Ghost:
    """comme un garde : fait une patrouille dans *son* labyrinthe ; patrouille
    qui se termine si le fantome sort de la zone ou si on détecte une boucle
    il y a une boucle lorsqu'un couple (position, direction) est présente dans la mémoire
    """

    def __init__(self, laby, position, direction):
        self.laby = laby
        self.position = position
        self.direction = direction
        self.memory = {(position, direction)}

    def turn(self):
        self.direction = TURN_RIGHT[self.direction]
    
    def forward(self):
        new_position = self.laby.new_position(self.position, self.direction)
        if self.laby.inside(new_position):
            if self.laby.is_free(new_position):
                self.position = new_position
                if (self.position, self.direction) in self.memory:
                    return True, True
                else:
                    self.memory.add((self.position, self.direction))
                    return True, False
            else:
                self.turn()
                return True, False
        else:
            return False, False

    def patrol(self):
        inside, loop = True, False
        while inside and not loop:
            inside, loop = self.forward()
        return loop


class Laby:

    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def copy(self):
        return Laby([line.copy() for line in self.grid])
    
    def __str__(self):
        return '\n'.join(' '.join(line) for line in self.grid)
    
    def inside(self, position):
        i, j = position
        return 0 <= i < self.height and 0 <= j < self.width
    
    def new_position(self, position, direction):
        i, j = position
        di, dj = direction
        return i+di, j+dj

    def is_free(self, position):
        i, j = position
        return self.grid[i][j] != WALL
    
    def wall(self, position):
        i, j = position
        self.grid[i][j] = WALL

    def obstacle(self, position):
        i, j = position
        self.grid[i][j] = OBSTACLE


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

    def loop_test(self):
        """si on peut avancer, on fait une copie du labyrinthe, on place un mur
        à la nouvelle position, on lance un fantome sur ce labyrinthe
        si on détecte une boucle, on ajoute la position à un ensemble
        """
        new_position = self.laby.new_position(self.position, self.direction)
        if self.laby.inside(new_position) and self.laby.is_free(new_position):
            new_laby = self.laby.copy()
            new_laby.wall(new_position)
            position, direction = self.initial
            ghost = Ghost(new_laby, position, direction)
            if ghost.patrol():
                self.obstructions.add(new_position)
    
    def forward(self, with_loop_test):
        """move guard one step forward and return True if guard is still inside the area"""
        if with_loop_test:
            self.loop_test()
        new_position = self.laby.new_position(self.position, self.direction)
        if self.laby.inside(new_position):
            if self.laby.is_free(new_position):
                self.memory.add(new_position)
                self.position = new_position
            else:
                self.turn()
            return True
        else:
            return False

    def patrol(self, with_loop_test=False):
        inside = True
        while inside:
            inside = self.forward(with_loop_test)

            
class P6(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 6, part)
        self.laby = None
        self.guard = None
        
    def load(self, filename):
        grid = []
        with open(filename) as datas:
            for i, line in enumerate(datas):
                grid.append([])
                for j in range(len(line)-1):
                    grid[-1].append(line[j])
                    if line[j] in DIRECTIONS:
                        guard_position = i, j
                        guard_direction = DIRECTIONS[line[j]]
        self.laby = Laby(grid)
        self.guard = Guard(self.laby, guard_position, guard_direction)

    def solve(self, filename):
        self.load(filename)
        if self.part == 0:
            self.guard.patrol(with_loop_test=False)
            self.solution = len(self.guard.memory)
        else:
            self.guard.patrol(with_loop_test=True)
            self.solution = len(self.guard.obstructions)

    def show(self):
        for position in self.guard.obstructions:
            self.laby.obstacle(position)
        print(self.laby)

def main():
    for part in (0, 1):
        pb = P6(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 