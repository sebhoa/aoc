from collections import deque

class Stone:
    
    def __init__(self, number, nb=1):
        self.number = number
        self.nb = nb

    def __repr__(self):
        return f'Stone({self.number}, {self.nb})' 

    def inc(self, n):
        self.nb += n
    
    def transformation(self):        
        # rule 1
        if self.number == '0':
            return ('1',)

        # rule 2
        nb_digits = len(self.number)
        if nb_digits % 2 == 0:
            left = self.number[:nb_digits//2]
            right = str(int(self.number[nb_digits//2:]))
            return (left, right)

        # rule 3
        new_number = str(int(self.number) * 2024)
        return (new_number,)


class Pluto:

    def __init__(self, datas):
        self.stones = {number: Stone(number) for number in datas}

    def __len__(self):
        return sum(stone.nb for stone in self.stones.values())
    
    def transformation(self):
        stone_ids = list(self.stones.keys())
        new_stone_ids = {}
        for stone_id in stone_ids: 
            stone = self.stones.pop(stone_id)
            new_ids = stone.transformation()
            for sid in new_ids:
                new_stone_ids[sid] = new_stone_ids.get(sid, 0) + stone.nb
        for sid in new_stone_ids:
            self.stones[sid] = Stone(sid, new_stone_ids[sid])

class P11(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 11, part)
        self.pluto = None
    
    def load(self, filename):
        with open(filename) as datas:
            self.pluto = Pluto(datas.readline().split())

    def solve(self, filename):
        self.load(filename)
        nb_blinks = [25, 75]
        for _ in range(nb_blinks[self.part]):
            self.pluto.transformation()
        self.solution = len(self.pluto)

def main():
    for part in (0, 1):
        pb = P11(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 