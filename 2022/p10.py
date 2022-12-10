class P10(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 10)
        self.cycle = 1
        self.register = 1
        self.strength = 0
        self.crt = [['#'] * 40 for _ in range(7)]
        
    def print_crt(self):
        print('\n'.join(''.join(pixel for pixel in self.crt[i]) for i in range(6))) 
        
    def add_cycle_1(self, value):
        self.cycle += 1
        
    def noop(self):
        self.cycle += 1
     
    def load_datas(self, part, filename=None):
        if filename is None:
            filename = self.tests[part]
        with open(filename) as datas:
            self.instructions = datas.read().strip().split('\n')

    def update_strenght(self):
        if self.cycle == 20 or (self.cycle - 20) % 40 == 0:
            self.strength += self.cycle * self.register

    def update_crt(self):
        i, j = divmod(self.cycle - 1, 40)
        if j < self.register or j >= self.register + 3:
            self.crt[i][j] = '.'        

    def execute(self, update_function):
        for instruction in self.instructions:
            #print(self.cycle)
            if instruction.startswith('noop'):
                self.cycle += 1
                update_function()
            elif instruction.startswith('addx'):
                x_value = int(instruction[5:])
                self.cycle += 1
                update_function()
                self.cycle += 1
                self.register += x_value
                update_function()
                
    def reset(self):
        self.register = 1
        self.cycle = 1
        self.strength = 0
        self.crt = [['#'] * 40 for _ in range(7)]
        
    def solve(self, part, filename=None):
        self.reset()
        self.load_datas(part, filename)
        if part % 2 == 0:
            self.execute(self.update_strenght)
            self.solutions[part] = self.strength
        else:
            self.register -= 1
            self.execute(self.update_crt)
            self.print_crt()
            self.solutions[part] = input()