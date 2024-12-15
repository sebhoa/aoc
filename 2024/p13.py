import re

COST_A = 3
COST_B = 1

BUTTON_REGEX = r"X\+(\d+), Y\+(\d+)"
PRIZE_REGEX = r"X=(\d+), Y=(\d+)"

class Machine:

    def __init__(self, button_A, button_B, prize):
        self.position = 0, 0
        self.A = button_A
        self.B = button_B
        self.nb_A = 0
        self.nb_B = 0
        self.prize = prize

    def __str__(self):
        s = f'Button A: X+{self.A[0]}, Y+{self.A[1]}\n'
        s += f'Button B: X+{self.B[0]}, Y+{self.B[1]}\n'
        s += f'Prize: X={self.prize[0]}, Y={self.prize[1]}\n'
        s += f'Position: {self.position}, Coût: {self.cost()}'
        return s
    
    def press_A(self):
        dx, dy = self.A
        self.position = self.position[0] + dx, self.position[1] + dy
        self.nb_A += 1

    def press_B(self):
        dx, dy = self.B
        self.position = self.position[0] + dx, self.position[1] + dy
        self.nb_B += 1

    def cost(self):
        return self.nb_A * COST_A + self.nb_B * COST_B

    def moves_min(self):
        p_x, p_y = self.prize
        a_x, a_y = self.A
        b_x, b_y = self.B
        nb_b = (p_y * a_x - p_x * a_y) // (b_y * a_x - b_x * a_y)
        nb_a = (p_x - b_x * nb_b) // a_x
        return nb_a, nb_b

    def move(self, nb_a, nb_b):
        a_x, a_y = self.A
        b_x, b_y = self.B
        self.position = nb_a * a_x + nb_b * b_x, nb_a * a_y + nb_b * b_y 
    
    def cost_min(self):
        nb_a, nb_b = self.moves_min()
        self.move(nb_a, nb_b)
        return nb_a * COST_A + nb_b * COST_B if self.win() else 0
    
    def win(self):
        return self.position == self.prize


class P13(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 13, part)
        self.machines = []
    
    def load(self, filename):
        self.machines = []
        correction = 0 if self.part == 0 else 10000000000000
        with open(filename) as datas:
            line = ' '
            while line:
                button_A = tuple(int(e) for e in re.findall(BUTTON_REGEX, datas.readline())[0])
                button_B = tuple(int(e) for e in re.findall(BUTTON_REGEX, datas.readline())[0])
                prize = tuple(int(e) + correction for e in re.findall(PRIZE_REGEX, datas.readline())[0])
                self.machines.append(Machine(button_A, button_B, prize))
                line = datas.readline()
        
    def solve(self, filename):
        self.load(filename)
        self.solution = sum(m.cost_min() for m in self.machines)

def main():
    for part in (0, 1):
        pb = P13(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 