from os import listdir
from os.path import isfile, join
from utils import dimacs
from collections import defaultdict
from itertools import combinations
import pycosat


def reduce_to_sat(size: int, sets: list[list[int]]):
    elem_sets: dict[int, list[int]] = defaultdict(lambda: [])
    for i, set3 in enumerate(sets):
        for elem in set3:
            elem_sets[elem].append(i + 1)

    cnf = list(elem_sets.values())
    for a, b in combinations(range(len(sets)), 2):
        if set(sets[a]).intersection(set(sets[b])):
            cnf.append([-(a + 1), -(b + 1)])

    return cnf


if __name__ == '__main__':
    filenames = [f"lab3/x3c/{f}" for f in listdir("lab3/x3c") if isfile(join("lab3/x3c", f))]
    x3c_instances = list(map(dimacs.loadX3C, filenames))

    for name, x3c in zip(filenames, x3c_instances):
        print(name.split("/")[-1])
        sat = reduce_to_sat(*x3c)
        sol = pycosat.solve(sat)
        if sol == "UNSAT":
            print("Unsolvable")
        else:
            print("Solvable")
            chosen_sets = [i for i in sol if i > 0]
            print(chosen_sets)
        print()


