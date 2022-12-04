BASE_NAME = 'input'
SMALL_NAME = 'small'

class Puzzle:
    
    def __init__(self, num):
        self.id = num
        self.solutions = [None, None, None, None]
        self.tests = [f'{SMALL_NAME}{num:02}a.txt', f'{SMALL_NAME}{num:02}b.txt', f'{BASE_NAME}{num:02}a.txt', f'{BASE_NAME}{num:02}b.txt']
            
    def __str__(self):
        type_test = ('test', 'test', 'part', 'part')
        part_test = ('I', 'II', 'I', 'II')
        s = f'Puzzle {self.id:02}\n'
        for i in range(4):
            s += f'-- {type_test[i]} {part_test[i]:2} : {self.solutions[i]}\n'
        return s
        