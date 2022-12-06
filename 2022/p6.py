class P6(Puzzle):

    def __init__(self):
        Puzzle.__init__(self, 6)
        self.buffer = ''
        self.size = 0
        
    def load_datas(self, part, filename):
        if filename is None:
            filename = self.tests[part]
        with open(filename) as datas:
            self.buffer = datas.readline().strip()
        
    def nb_characters(self):
        seen_characters = set()
        start = 0
        nb_consecutive_diff = 0
        for i, char in enumerate(self.buffer):
            if char in seen_characters:
                while self.buffer[start] != char:
                    seen_characters.discard(self.buffer[start])
                    start += 1                    
                start += 1
                while start < i and self.buffer[start] == char:
                    start += 1
                nb_consecutive_diff = i - start + 1
            else:
                seen_characters.add(char) 
                nb_consecutive_diff += 1
                if nb_consecutive_diff >= self.size:
                    return i + 1
        
    def solve(self, part, filename=None):
        self.load_datas(part, filename)
        self.size = (4, 14, 4, 14)[part]
        self.solutions[part] = self.nb_characters()
