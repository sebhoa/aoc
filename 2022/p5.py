class P5(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 5)
        self.stacks = []
        self.instructions = []
        
    def aff_stacks(self):
        n = len(max(self.stacks, key=len))
        for i in range(n-1, -1, -1):
            for stack in self.stacks:
                if i >= len(stack):
                    print('   ', end=' ')
                else:
                    print(f'[{stack[i]}]', end=' ')
            print()
        
    def transfert(self, nb_crates, from_stack_id, to_stack_id, model='9000'):
        from_stack = self.stacks[from_stack_id]
        to_stack = self.stacks[to_stack_id]
        temporary_stack = to_stack if model == '9000' else []
        for _ in range(nb_crates):
            temporary_stack.append(from_stack.pop())        
        if model != '9000':
            for _ in range(nb_crates):
                to_stack.append(temporary_stack.pop())
    
    def load_datas(self, part):
        self.instructions = []
        crates = []
        with open(self.tests[part]) as datas:
            # phase crates 
            ligne = datas.readline()
            while ligne and ligne != '\n':
                crates.append(ligne)
                ligne = datas.readline()
            
            # phase instructions
            ligne = datas.readline()
            while ligne:
                str_instr = ligne.strip().replace('move','').replace('from', '').replace('to', '')
                self.instructions.append(tuple(int(e) for e in str_instr.split()))
                ligne = datas.readline()
        
        # now fill stacks
        nb_stacks = len(crates.pop().split())
        self.stacks = [[] for _ in range(nb_stacks)]
        for i in range(len(crates)-1, -1, -1):
            stack_id = 0
            ligne_de_crates = crates[i]
            for k in range(1, len(ligne_de_crates), 4):
                crate = ligne_de_crates[k]
                if crate != ' ':
                    self.stacks[stack_id].append(crate)
                stack_id += 1
                
    def solve(self, part):
        model_of_machine = ('9000', '9001', '9000', '9001')[part]
        self.load_datas(part)
        for (nb_crates, from_num, to_num) in self.instructions:
            self.transfert(nb_crates, from_num-1, to_num-1, model_of_machine)
        msg = ''.join(stack[-1] for stack in self.stacks)
        self.solutions[part] = msg
