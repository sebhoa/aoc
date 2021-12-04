import sys

EOF = ''
FILE = 'input04.txt'

class Grid:

    SIZE = 5

    def __init__(self):
        self.values = {}
        self.last_called = None
        self.winning_grid = False
        self.count_by_line = [0] * Grid.SIZE
        self.count_by_col = [0] * Grid.SIZE

    def load(self, line_of_values, line_id):
        for col_id, str_value in enumerate(line_of_values.split()):
            self.values[int(str_value)] = (line_id, col_id)

    def mark_and_check(self, value):
        if value in self.values:
            line, col = self.values.pop(value)
            self.last_called = value
            self.count_by_col[col] += 1
            self.count_by_line[line] += 1
            self.winning_grid = self.count_by_line[line] == Grid.SIZE or self.count_by_col[col] == Grid.SIZE

    def score(self):
        return sum(self.values) * self.last_called


class Bingo:

    def __init__(self, filename=FILE):
        self.filename = filename
        self.end = False
        self.numbers = []
        self.grids = []

    def load(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            self.numbers = [int(e) for e in datas.readline().strip().split(',')]
            ligne = datas.readline() # la ligne séparatrice blanche
            while ligne != EOF:
                grid = Grid()
                for ligne_id in range(5):
                    ligne = datas.readline()
                    grid.load(ligne, ligne_id)
                ligne = datas.readline() # passer la ligne blanche entre 2 grilles
                self.grids.append(grid)

    def catch_first_grid_winning(self, number):
        for grid in self.grids:
            grid.mark_and_check(number)
            if grid.winning_grid:
                return grid

    def check_and_remove(self, number):
        """pour la partie 2"""
        for grid in self.grids:
            grid.mark_and_check(number)
        self.grids = [grid for grid in self.grids if not grid.winning_grid]        

    def solve(self):
        self.load()
        for number in self.numbers:
            grid = self.catch_first_grid_winning(number)
            if grid is not None:
                return grid.score()

    def solve_two(self):
        """partie 2"""
        self.load()
        number_id = 0
        
        # find the last...
        while len(self.grids) > 1:
            number = self.numbers[number_id]
            self.check_and_remove(number)
            number_id += 1

        # Make the last wins...
        last = self.grids[0]
        while not last.winning_grid:
            number = self.numbers[number_id]
            last.mark_and_check(number)
            number_id += 1
        return last.score()


def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    bingo = Bingo(fichier)
    if version == '1':
        print(bingo.solve())
    else:
        print(bingo.solve_two())

if __name__ == '__main__':
    main()    

