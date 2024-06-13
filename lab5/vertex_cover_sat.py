import pycosat
from os import listdir
from os.path import isfile, join
from utils import dimacs
from itertools import product
import pycosat


def reduce_to_sat(graph: list[set[int]], k: int) -> list[list[int]]:
    sat = []
    n = len(graph) + 1
    for v, u in dimacs.edgeList(graph):
        sat.append([v, u])

    for i in range(n):
        sat.append([i*n + n])

    for i in range(1, n):
        sat.append([-(i + n)])

    for i, j in product(range(1, n), range(1, n)):
        sat.append([
            -((i-1)*n + j + n),
            i*n + j + n
        ])

        sat.append([
            -((i - 1) * n + j - 1 + n),
            -i,
            i * n + j + n
        ])

    sat.append([
        -((n-1)*n + k + 1 + n)
    ])

    return sat


def main() -> None:
    # filenames = [f"graph/{f}" for f in listdir("graph") if isfile(join("graph", f))]
    filenames = [f"graph/{f}" for f in ["e5", "e10", "e20", "e40"]]
    graphs = list(map(dimacs.loadGraph, filenames))

    for name, graph in zip(filenames, graphs):
        print(name)
        n = len(graph) + 1
        sat = reduce_to_sat(graph, 18)

        sol = pycosat.solve(sat)
        if sol == "UNSAT":
            print("Unsolvable")
        else:
            vertices = list(filter(lambda x: 0 < x < n, sol))
            print(vertices)
        print()


if __name__ == '__main__':
    main()
