class P11(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 11)
        self.f = []        # les fonctions de calcul
        self.div = []      # les diviseur pour le critère de divisibilité
        self.worries = []  # la liste des worry level associé au numéro du singe 
        self.suivants = [] # les numéros des singes où l'item sera transféré
        self.diviseur = None # le diviseur global, 3 ou 1
        self.nb_monkeys = 0  # le nombre de singes
        self.activities = [] # le récap de l'activité de chaque singe
        
    def load_datas(self, part, filename=None):
        if filename is None:
            filename = self.tests[part]
        with open(filename) as datas:
            for pid, monkey_infos in enumerate(datas.read().strip().split('\n\n')):
                _, s_items, ope, div, true, false = monkey_infos.split('\n')
                self.set_fonctions(ope.strip())
                self.set_div(div.strip())
                self.set_worries(s_items.strip(), pid)
                self.set_suivants(true.strip(), false.strip())
                self.activities.append(0)
            self.nb_monkeys = pid+1
        if self.diviseur == 1: 
            for i in range(len(self.worries)):
                w, wid = self.worries[i]
                d = {div: w%div for div in self.div}
                self.worries[i] = [d, wid]

    def set_suivants(self, true, false):
        self.suivants.append((int(false[26:]), int(true[25:])))
    
    def set_div(self, div):
        self.div.append(int(div[19:]))
    
    def set_worries(self, items, pid):
        self.worries.extend([int(e), pid] for e in items[16:].split(', '))
    
    def set_fonctions(self, operation):
        operator = operation[21]
        operand = operation[23:]
        if operand == 'old':
            if operator == '+':
                self.f.append(lambda a: (a + a))
            else:
                self.f.append(lambda a: (a * a))
        else:
            if operator == '+':
                self.f.append(lambda a: (a + int(operand)))
            else:
                self.f.append(lambda a: (a * int(operand)))       
        
    def update_one(self, info):
        lvl, pid = info
        info[0] = self.f[pid](lvl) // 3
        is_divisible = info[0] % self.div[pid] == 0
        info[1] = self.suivants[pid][is_divisible]

    def update_two(self, info):
        d_worry, pid = info
        for k in d_worry:
            d_worry[k] = self.f[pid](d_worry[k]) % k 
        is_divisible = d_worry[self.div[pid]] == 0
        info[1] = self.suivants[pid][is_divisible]
        
    def round(self):
        for pid in range(self.nb_monkeys):
            for i in range(len(self.worries)):
                worry_id = self.worries[i][1]
                if worry_id == pid:
                    self.activities[pid] += 1
                    if self.diviseur == 3:
                        self.update_one(self.worries[i])
                    else:
                        self.update_two(self.worries[i])
                    
                            
    def business_lvl(self):
        self.activities.sort(reverse=True)
        return self.activities[0] * self.activities[1] 
        
    def solve(self, part, filename=None):
        nb_rounds, self.diviseur = (20, 3) if part % 2 == 0 else (10000, 1)
        self.load_datas(part, filename)
        for rnd in range(nb_rounds):
            self.round()
        self.solutions[part] = self.business_lvl()
