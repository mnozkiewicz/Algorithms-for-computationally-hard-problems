import utils.dimacs as dimacs
from itertools import combinations


def brute_force(G: list[set], k: int, E: list[tuple]):
    V = len(G)
    for vertex_set in combinations(range(V), k):
        vertex_set = set(vertex_set)
        if dimacs.isVC(E, vertex_set):
            return vertex_set
    return False
