from puzzle import Puzzle

class Machine:

    def __init__(self, registers, program):
        self.registers = registers
        self.program = program
        self.pointer = 0
        self.output = []
        self.langage = None

    def __str__(self):
        s = f'Register A: {self.A()}\n'
        s += f'Register B: {self.B()}\n'
        s += f'Register C: {self.C()}\n'
        s += '--------------------------\n'
        s += f'{self.output}'
        return s

    
    def set_A(self, value):
        self.registers[0] = value

    def set_B(self, value):
        self.registers[1] = value

    def set_C(self, value):
        self.registers[2] = value

    def A(self):
        return self.registers[0]

    def B(self):
        return self.registers[1]

    def C(self):
        return self.registers[2]

    def adv(self, operand):
        self.set_A(int(self.A() / (2 ** self.combo(operand))))
        self.pointer += 2

    def bxl(self, operand):
        self.set_B(self.B() ^ operand)
        self.pointer += 2

    def bst(self, operand):
        self.set_B(self.combo(operand) % 8)
        self.pointer += 2

    def jnz(self, operand):
        if self.A() == 0:
            self.pointer += 2
        else:
            self.pointer = operand

    def bxc(self, operand):
        self.set_B(self.B() ^ self.C())
        self.pointer += 2

    def out(self, operand):
        self.output.append(self.combo(operand) % 8)
        self.pointer += 2

    def bdv(self, operand):
        self.set_B(int(self.A() / 2 ** self.combo(operand)))
        self.pointer += 2

    def cdv(self, operand):
        self.set_C(int(self.A() / 2 ** self.combo(operand)))
        self.pointer += 2

    def set_langage(self):
        self.langage = [self.adv, self.bxl, self.bst, self.jnz, self.bxc, self.out, self.bdv, self.cdv]

    def combo(self, value):
        if value < 4:
            return value
        else:
            return self.registers[value-4]

    def reset(self):
        self.registers = [0, 0, 0]
        self.output = []
        self.pointer = 0
    
    def exec(self):
        while self.pointer < len(self.program): 
            instruction = self.langage[self.program[self.pointer]]
            operand = self.program[self.pointer+1]
            instruction(operand)
            

class P17(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 17, part)
        self.machine = None
    
    def load(self, filename):
        registers = []
        with open(filename) as datas:
            for _ in range(3):
                registers.append(int(datas.readline()[12:]))
            datas.readline()
            program = [int(e) for e in datas.readline()[8:].split(',')]
        self.machine = Machine(registers, program)
        self.machine.set_langage()
                
    def solve(self, filename):
        self.load(filename)
        self.machine.exec()
        if self.part == 0:
            self.solution = ','.join(str(e) for e in self.machine.output)
        else:
            # force brute... ça passe pas :)
            a = 1
            while self.machine.output != self.machine.program:
                self.machine.reset()
                a += 1
                if a%1000000 == 0:
                    print(a)
                self.machine.set_A(a)
                self.machine.exec()
            self.solution = a
            
def main():
    for part in (0, 1):
        pb = P17(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 