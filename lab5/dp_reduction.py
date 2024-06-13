from utils import dimacs
from itertools import product


def flatten_fun(n):
    return lambda i, j: ((i+j)*(i+j+1) // 2 + i) + n


def reduce_to_sat(graph: list[set[int]], k: int) -> list[list[int]]:
    n = len(graph)

    cover_constraints = []
    for v, u in dimacs.edgeList(graph):
        cover_constraints.append([
            v,
            u
        ])

    flatten = flatten_fun(n)
    edge_case_constraints = []
    for i in range(n + 1):
        edge_case_constraints.append([
            flatten(i, 0)
        ])

    for j in range(1, n + 1):
        edge_case_constraints.append([
            -flatten(0, j)
        ])

    function_constraints = []
    for i, j in product(range(1, n + 1), range(1, n + 1)):
        function_constraints.append([
            -flatten(i - 1, j),
            flatten(i, j)
        ])

        function_constraints.append([
            -flatten(i - 1, j - 1),
            -i,
            flatten(i, j)
        ])

    threshold_constraints = [[
        -flatten(n, k + 1)
    ]]

    cnf = \
        cover_constraints + \
        edge_case_constraints + \
        function_constraints + \
        threshold_constraints

    return cnf
