from typing import Union
from lab1.dimacs import remove_edges


def backtracking(G: list[set], k: int, E: set, vertices: set = None) -> Union[bool, set]:
    if vertices is None:
        vertices = set()

    if not E:
        return vertices
    if k == 0:
        return False

    cur_edge = E.pop()
    for v in cur_edge:
        vertices.add(v)
        removed_edges = remove_edges(G, E, v)

        if vertex_cover := backtracking(G, k - 1, E, vertices):
            return vertex_cover

        vertices.remove(v)
        for edge in removed_edges:
            E.add(edge)

    E.add(cur_edge)
    return False
