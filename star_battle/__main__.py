from star_battle import solve
from sys import argv
from yaml import safe_load
from z3 import print_matrix

if __name__ == "__main__":
    with open(argv[1]) as f:
        regions = [
            [tuple(int(i) for i in c.split(" ")) for c in r] for r in safe_load(f)
        ]
    solution = solve(regions)
    print_matrix(solution)
