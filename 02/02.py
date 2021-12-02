import sys

FORWARD = 'forward'
DOWN = 'down'
UP = 'up'

FILE = 'input02.txt'

class SubMarine:

    def __init__(self):
        self.position = 0
        self.profondeur = 0
        self.aim = 0 # pour la version 2
    
    def ajoute_position(self, x):
        self.position += x

    def ajoute_profondeur(self, y):
        self.profondeur += y

    def ajoute_aim(self, y):
        self.aim += y

    def automatique(self, action, valeur):
        if action == FORWARD:
            self.ajoute_position(valeur)
        elif action == DOWN:
            self.ajoute_profondeur(valeur)
        else:
            self.ajoute_profondeur(-valeur)

    def manuel(self, action, valeur):
        """Règles de déplacement version 2"""
        if action == FORWARD:
            self.ajoute_position(valeur)
            self.ajoute_profondeur(self.aim * valeur)
        elif action == DOWN:
            self.ajoute_aim(valeur)
        else:
            self.ajoute_aim(-valeur)

    def rapport(self):
        return self.position * self.profondeur


class Mission:

    def __init__(self, filename=FILE):
        self.filename = filename
        self.sub = SubMarine()

    def solve(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for ligne in datas:
                data = ligne.split()
                action, valeur = data[0], int(data[1])
                self.sub.automatique(action, valeur)
        return self.sub.rapport()

    def solve_two(self):
        with open(self.filename, 'r', encoding='utf-8') as datas:
            for ligne in datas:
                data = ligne.split()
                action, valeur = data[0], int(data[1])
                self.sub.manuel(action, valeur)
        return self.sub.rapport()

def main():
    version = sys.argv[1]
    if len(sys.argv) > 2:
        fichier = sys.argv[2]
    else:
        fichier = FILE
    mission = Mission(fichier)
    if version == '1':
        print(mission.solve())
    else:
        print(mission.solve_two())

if __name__ == '__main__':
    main()



