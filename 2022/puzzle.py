BASE_NAME = 'input'
SMALL_NAME = 'small'

class Puzzle:
    
    def __init__(self, num):
        self.id = num
        self.solutions = [None, None, None, None]
        self.tests = [f'{SMALL_NAME}{num:02}a.txt', f'{SMALL_NAME}{num:02}b.txt', f'{BASE_NAME}{num:02}a.txt', f'{BASE_NAME}{num:02}b.txt']
        
    def __str_sol(self, solution):
        return 'NA' if solution is None else solution
    
    def __str__(self):
        s = f'Puzzle {self.id:02}\n'
        s += f'-- test I  : {self.__str_sol(self.solutions[0])}\n'
        s += f'-- test II : {self.__str_sol(self.solutions[1])}\n'
        s += f'-- part I  : {self.__str_sol(self.solutions[2])}\n'
        s += f'-- part II : {self.__str_sol(self.solutions[3])}\n'
        return s