from os import listdir
from os.path import isfile, join
from utils import dimacs
from itertools import combinations
import pycosat
from enum import Enum


class Res(Enum):
    UNSOL = 0
    SOL = 1
    INCORRECT = 2


def reduce_to_sat(graph: list[set[int]], k: int):
    n = len(graph)
    cnf = []
    for i in range(1, n + 1):
        v = (i-1)*k
        cnf.append([v + j for j in range(1, k + 1)])
        for a, b in combinations(range(1, k + 1), 2):
            cnf.append([-(v + a), -(v + b)])

    for a, b in dimacs.edgeList(graph):
        for j in range(1, k + 1):
            cnf.append([-((a - 1)*k + j), -((b - 1)*k + j)])

    return cnf


def decode_vertex_color(value: int, k: int):
    value -= 1
    return (value // k) + 1, (value % k) + 1


def check_coloring(graph: list[set[int]], coloring: list[int], k: int):
    mapping = {}
    for val in coloring:
        if val > 0:
            vertex, color = decode_vertex_color(val, k)
            if vertex in mapping:
                return False
            mapping[vertex] = color

    for vertex in range(1, len(graph) + 1):
        if vertex not in mapping:
            return False

    for a, b in dimacs.edgeList(graph):
        if mapping[a] == mapping[b]:
            return False

    return True


def graph_coloring(graph: list[set[int]], k: int):
    formula = reduce_to_sat(graph, k)
    sol = pycosat.solve(formula)
    if sol == "UNSAT":
        return Res.UNSOL
    else:
        if not check_coloring(graph, sol, k):
            return Res.INCORRECT
        else:
            return Res.SOL


if __name__ == '__main__':
    filenames = [f"lab3/graphs/{f}" for f in listdir("lab3/graphs") if isfile(join("lab3/graphs", f))]
    graphs = map(dimacs.loadGraph, filenames)
    for graph_name, graph_instance in zip(filenames, graphs):
        if len(dimacs.edgeList(graph_instance)) > 200:
            continue
        print(graph_name.split('/')[-1])
        right = 3
        left = 3
        checked = set()
        while True:
            res = graph_coloring(graph_instance, right)
            checked.add(right)
            match res:
                case Res.INCORRECT:
                    print("Found solution but is incorrect")
                    exit(0)
                case Res.SOL:
                    print(f"{right} colors is OK")
                    right -= 1
                    break
                case Res.UNSOL:
                    print(f"{right} colors is not enough")
                    left = right + 1
                    right = min(right * 2, len(graph_instance))

        while left <= right:
            s = (left + right) // 2
            if s in checked:
                print(f"{s} colors is not enough")
                left = s + 1
                continue

            res = graph_coloring(graph_instance, s)
            match res:
                case Res.INCORRECT:
                    print("Found solution but is incorrect")
                    exit(0)
                case Res.SOL:
                    print(f"{s} colors is OK")
                    right = s - 1
                case Res.UNSOL:
                    print(f"{s} colors is not enough")
                    left = s + 1
        print("--------------------")
