FREE = '.'

class Sector:

    def __init__(self, disk_map, start, size):
        self.disk_map = disk_map
        self.start = start
        self.size = size

    def __str__(self):
        return f'{self.start}: {self.size}'

    def modify(self, size):
        self.start += size
        self.size -= size

class DiskMap:

    def __init__(self, description):
        self.description = description
        self.free_sectors = []
        self.used_sectors = []
        self.disk = []
        self.describe_disk()

    def __str__(self):
        s = "USED: " + ' '.join(str(fs) for fs in self.used_sectors) + '\n'
        s += "FREE: " + ' '.join(str(fs) for fs in self.free_sectors) + '\n'
        s += f'{self.disk}'
        return s
    
    def describe_disk(self):
        infos = self.description
        file_id = 0
        start = 0
        size = int(infos[0])
        self.used_sectors = [Sector(self, start, size)]
        self.disk = [file_id] * size
        for i in range(1, len(infos)):
            start += size
            size = int(infos[i])
            if i%2 == 0:
                file_id += 1            
                self.disk.extend([file_id] * size)
                self.used_sectors.append(Sector(self, start, size))
            else:
                self.disk.extend([FREE] * size)
                self.free_sectors.append(Sector(self, start, size))

    def checksum(self):
        return sum(i * self.disk[i] for i in range(len(self.disk)) if self.disk[i] != FREE)
    
    def first(self, size, with_fragmentation):
        for free_sector in self.free_sectors:
            if free_sector.size >= size or with_fragmentation:
                return free_sector
            
    def compress(self, with_fragmentation):
        for sector_id in range(len(self.used_sectors)-1, -1, -1):
            sector = self.used_sectors[sector_id]
            free_sector = self.first(sector.size, with_fragmentation)
            if free_sector is not None:
                left = free_sector.start
                right = sector.start + sector.size - 1
                while left < right:
                    if self.disk[left] == FREE and self.disk[right] == sector_id:
                        self.disk[left] = sector_id
                        self.disk[right] = FREE
                        left, right = left + 1, right - 1
                    elif self.disk[left] != FREE:
                        left += 1
                    else:
                        right -= 1
                real_size = min(sector.size, free_sector.size)
                free_sector.modify(real_size)


class P9(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 9, part)
        self.disk_map = None
    
    def load(self, filename):
        with open(filename) as datas:
            self.disk_map = DiskMap(datas.readline().strip())

    def solve(self, filename):
        self.load(filename)
        with_fragmentation = self.part == 0
        self.disk_map.compress(with_fragmentation)
        self.solution = self.disk_map.checksum()


def main():
    for part in (0, 1):
        pb = P8(part)
        pb.test()
        print(pb)
        pb.validate()
        print(pb)

if __name__ == "__main__":
    main() 