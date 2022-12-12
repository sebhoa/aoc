from puzzle import Puzzle

TOTAL_SIZE = 70000000
MIN_SIZE = 30000000
SEUIL = 100000

class P7(Puzzle):

    def __init__(self, part):
        Puzzle.__init__(self, 7, part)
        self.file_system = {}
        self.path = []
        self.directory_size = {}
        
    def current_path(self):
        return '/'.join(self.path).replace('//', '/')
    
    def create_path(self, parent, child):
        return f'{parent}/{child}'.replace('//', '/')
    
    def parse_cmd(self, cmd):
        if cmd.startswith('cd'):
            _, directory = cmd.split()            
            if directory == '/':
                self.path = ['/']
                if '/' not in self.file_system:
                    self.file_system['/'] = {}
            elif directory == '..':
                self.path.pop()
            else:
                self.path.append(directory)
                name = self.current_path() 
                if name not in self.file_system:
                    self.file_system[name] = {}
    
    def parse_ls(self, cmd):
        parent_name = self.current_path()
        
        # cas d'un répertoire
        if cmd.startswith('dir'):
            _, directory = cmd.split()
            child_name = self.create_path(parent_name, directory) 
            if child_name not in self.file_system[parent_name]:
                self.file_system[parent_name][child_name] = {}
        
        # cas d'un fichier
        else:
            size, filename = cmd.split()
            child_name = self.create_path(parent_name, filename) 
            self.file_system[parent_name][child_name] = int(size)
            
    
    def load_datas(self, filename):
        """Met à jour le file_system ie le listing des repertoires et leur contenu"""
        with open(filename) as datas:
            for cmd in datas:
                if cmd.startswith('$'):
                    self.parse_cmd(cmd[2:])
                else:
                    self.parse_ls(cmd)
                    
    def size_of(self, directory, content):
        """Calcule la taille de tous les répertoires"""
        if directory not in self.directory_size:
            self.directory_size[directory] = 0
            for file in content:
                if self.is_directory(file):
                    self.directory_size[directory] += self.size_of(file, self.file_system[file])
                else:
                    self.directory_size[directory] += content[file]
        return self.directory_size[directory]
    
    def is_directory(self, ressource):
        return ressource in self.file_system
    
    def sum_small_sizes(self):
        return sum(size for size in self.directory_size.values() if size <= SEUIL)
    
    def the_smallest_to_delete(self):
        total_used = self.directory_size['/']
        smallest_size = total_used
        for size in self.directory_size.values():
            if TOTAL_SIZE - total_used + size >= MIN_SIZE and size < smallest_size:
                smallest_size = size
        return smallest_size
    
    def reset(self):
        self.file_system = {}
        self.path = []
        self.directory_size = {}
    
    def solve(self, filename):
        self.reset()
        self.load_datas(filename)
        self.size_of('/', self.file_system['/'])
        self.solution = self.sum_small_sizes() if self.part == 0 else self.the_smallest_to_delete()
        print(self)

p7one = P7(0)
p7one.validate()
p7two = P7(1)
p7two.validate()