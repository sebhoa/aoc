import sys

EOF = ''


# Part One

def solve(filename='input01.txt'):
    """Une version où on traite les données une à une (enfin 2 par 2)
    sans tout charger... on avance un peu comme dans la version itérative
    de fibonacci"""
    with open(filename, 'r', encoding='utf-8') as entree:
        solution = 0
        ligne = entree.readline()
        b = int(ligne.strip())
        while ligne != EOF:
            a = b
            b = int(ligne.strip())
            if b > a:
                solution += 1
            ligne = entree.readline()
        return solution


# Part Two

def solve_two(filename='input01.txt'):
    with open(filename, 'r', encoding='utf-8') as entree:
        three_lines = tuple(entree.readline() for _ in range(3))
        x, y, z = tuple(int(e) for e in three_lines)
        third = three_lines[-1]
        solution = -1 if z > x else 0 # astuce pour le cas de départ :)
        while third != EOF:
            a, b, c = x, y, z
            x, y, z = b, c, int(third)
            if z > a:  # x+y+z > a+b+c mais x, y c'est pareil que b, c 
                solution += 1
            third = entree.readline()
        return solution


def main():
    fct = [solve, solve_two][int(sys.argv[1])]
    if len(sys.argv) > 2:
        rep = fct(sys.argv[2])
    else:
        rep = fct()
    print(rep)

if __name__ == '__main__':
    main()
