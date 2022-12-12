from collections import deque

class Item:
    """Un item c'est un 'worry level' qui sert pour le mode facile du puzzle et
    un dictionnaire de modulos qui sert pour le mode difficile du puzzle
    l'item est mis à jour grâce une fonction mathématique f (et modulo pour le mode difficile)
    """
    
    def __init__(self, worry_level, puzzle_mode):
        self.level = worry_level
        self.modulos = {}
        self.inspected = self.__modulos_update if puzzle_mode == 1 else self.__level_update
        
    def __repr__(self):
        return f'Item({self.level}, {self.modulos})'
        
    def setting(self, div):
        self.modulos[div] = self.level % div
        
    def __modulos_update(self, f):
        for div, mod in self.modulos.items():
            self.modulos[div] = f(mod) % div

    def __level_update(self, f):
        self.level = f(self.level) // 3 
        
        
class Monkey:
    """Un singe est caractérisé par :
        - un puzzle
        - une fonction mathématique f de la forme ax ou x + a ou x^2
        - un critère de divisibilité caractérisé par un entier div et une fonction de test (2 différentes suivante le mode)
        - une liste d'items, ou plus exactement de numéros d'items rangés dans une file
        - deux numéros de singes à qui transmettre l'item traité suivant la validité du test de divisibilité
    """
    
        
    def __init__(self, puzzle, mathematical_function, div_description, true_description, false_description):
        self.puzzle = puzzle
        self.f = mathematical_function
        self.div = int(div_description[19:])
        self.item_ids = deque([])
        self.true_id = int(true_description[25:])
        self.false_id = int(false_description[26:])
        self.activity = 0
        self.divisibility_test = self.__modulos_div if puzzle.part == 1 else self.__level_div
        
    def __repr__(self):
        items = [self.puzzle.items[item_id].level for item_id in self.item_ids] 
        return f'Monkey({items}, {self.div}, {self.true_id}, {self.false_id})'
        
    def get_item(self, item_id):
        self.item_ids.append(item_id)

    def __modulos_div(self, item):
        return item.modulos[self.div] == 0

    def __level_div(self, item):
        return item.level % self.div == 0
    
    def inspect(self):
        while len(self.item_ids) > 0:
            item_id = self.item_ids.popleft()
            item = self.puzzle.items[item_id]
            item.inspected(self.f)
            if self.divisibility_test(item):
                next_monkey = self.puzzle.monkeys[self.true_id]
            else:
                next_monkey = self.puzzle.monkeys[self.false_id]
            next_monkey.get_item(item_id)
            self.activity += 1

            
class P11(Puzzle):

    @classmethod
    def create_function(cls, f_description):
        operator = f_description[21]
        operand = f_description[23:]
        if operand == 'old':
            return (lambda a: a + a) if operator == '+' else (lambda a: a * a)
        else:
            return (lambda a: a + int(operand)) if operator == '+' else (lambda a: a * int(operand))       
    
    def __init__(self, part):
        Puzzle.__init__(self, 11, part)
        self.monkeys = []
        self.items = []
        self.nb_rounds = 20 
        
    def load_datas(self, filename):
        with open(filename) as datas:
            item_id = 0
            for monkey_infos in datas.read().strip().split('\n\n'):
                _, items_description, f_description, div_description, true_description, false_description = monkey_infos.split('\n')
                mathematical_function = P11.create_function(f_description.strip())
                monkey = Monkey(self, mathematical_function, div_description.strip(), true_description.strip(), false_description.strip())
                for level in items_description.strip()[16:].split(', '):
                    self.items.append(Item(int(level), self.part))
                    monkey.get_item(item_id)
                    item_id += 1
                self.monkeys.append(monkey)
        if self.part != 0:
            self.nb_rounds = 10000
            self.set_modulos()
        
    def set_modulos(self):
        for item in self.items:
            for monkey in self.monkeys:
                item.setting(monkey.div)
                
    def reset(self):
        self.monkeys = []
        self.items = []
    
    def business_activity(self):
        activities = sorted((m.activity for m in self.monkeys), reverse=True)
        return activities[0] * activities[1]
    
    def solve(self, filename):
        self.reset()
        self.load_datas(filename)
        for _ in range(self.nb_rounds):
            for monkey in self.monkeys:
                monkey.inspect()
        self.solution = self.business_activity()
        print(self)