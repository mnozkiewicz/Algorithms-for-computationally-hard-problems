from typing import Union
from utils.dimacs import remove_vertex, restore_vertex


def fast_sol(G: list[set[int]], k: int, chosen_vertices: set = None) -> Union[bool, set]:
    if chosen_vertices is None:
        chosen_vertices = set()

    degree_one = -1
    v = 0
    for u in range(len(G)):
        if len(G[u]) > len(G[v]):
            v = u
        if len(G[u]) == 1:
            degree_one = u

    if len(G[v]) == 0:
        return chosen_vertices

    if k <= 0:
        return False

    if degree_one >= 0:
        v = next(iter(G[degree_one]))

    removed_edges = remove_vertex(G, v)
    chosen_vertices.add(v)
    if vertex_cover := fast_sol(G, k - 1, chosen_vertices):
        return vertex_cover
    restore_vertex(G, v, removed_edges)
    chosen_vertices.remove(v)

    if degree_one == -1 and len(G[v]) <= k:
        neighbors = list(G[v])
        removed_edges = []
        for u in neighbors:
            removed_edges.append(remove_vertex(G, u))
            chosen_vertices.add(u)

        if vertex_cover := fast_sol(G, k - len(neighbors), chosen_vertices):
            return vertex_cover

        for u, edges in zip(neighbors, removed_edges):
            restore_vertex(G, u, edges)
            chosen_vertices.remove(u)

    return False
