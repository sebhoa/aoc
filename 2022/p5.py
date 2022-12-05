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
        with open(self.tests[part]) as datas:
            datas_crates, datas_instructions = [s.split('\n') for s in datas.read().split('\n\n')]
            
            nb_stacks = len(datas_crates.pop().split())
            self.stacks = [[] for _ in range(nb_stacks)]
            for i in range(len(datas_crates)-1, -1, -1):
                stack_id = 0
                crates = datas_crates[i]
                for k in range(1, len(crates), 4):
                    if crates[k] != ' ':
                        self.stacks[stack_id].append(crates[k])
                    stack_id += 1
            
            self.instructions = []
            datas_instructions.pop()
            for instr in datas_instructions:
                str_instr = instr.strip().replace('move','').replace('from', '').replace('to', '')
                self.instructions.append(tuple(int(e) for e in str_instr.split()))
                
    def solve(self, part):
        model_of_machine = ('9000', '9001', '9000', '9001')[part]
        self.load_datas(part)
        for (nb_crates, from_num, to_num) in self.instructions:
            self.transfert(nb_crates, from_num-1, to_num-1, model_of_machine)
        msg = ''.join(stack[-1] for stack in self.stacks)
        self.solutions[part] = msg
