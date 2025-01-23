from random import shuffle
from copy import deepcopy


def solve_remove_random(G: list[set[int]], E: list[tuple[int, int]], solver: callable, show_info: bool = False) -> set[int]:
    G_copy = deepcopy(G)
    vertex_cover = solver(G, E)
    vertices = list(vertex_cover)
    shuffle(vertices)
    removed_vertices = 0
    for v in vertices:
        for s in G_copy[v]:
            if s not in vertex_cover:
                break
        else:
            vertex_cover.remove(v)
            removed_vertices += 1

    if show_info:
        print(f"Removed {removed_vertices} vertices")

    return vertex_cover
