class P6(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 6, part)
        self.buffer = ''
        self.size = 4 if part == 0 else 14
        
    def load_datas(self, filename):
        with open(filename) as datas:
            self.buffer = datas.readline().strip()
        
    def nb_characters(self):
        seen_characters = set()
        start = 0
        nb_consecutive_diff = 0
        for i, char in enumerate(self.buffer):
            if char in seen_characters:
                # Atteindre le premier char à gauche de i
                while self.buffer[start] != char:
                    seen_characters.discard(self.buffer[start])
                    start += 1                    
                # le virer ce premier char...
                start += 1
                
                # et les éventuels suivants toujours à gauche de i
                while start < i and self.buffer[start] == char:
                    start += 1
                
                # on remet à jour le nb de caracteres consécutifs différents
                nb_consecutive_diff = i - start + 1
            else:
                seen_characters.add(char) 
                nb_consecutive_diff += 1
                if nb_consecutive_diff >= self.size:
                    return i + 1
        
    def solve(self, filename):
        self.load_datas(filename)
        self.solution = self.nb_characters()
        