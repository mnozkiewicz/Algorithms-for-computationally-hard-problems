from lab1.dimacs import remove_edges
from typing import Union


def backtracking_optimized(G: list[set[int]], k: int, E: set, vertices: set, chosen_vertices: set = None) -> Union[bool, set]:
    if chosen_vertices is None:
        chosen_vertices = set()

    if not E:
        return chosen_vertices

    if k == 0:
        return False

    v = vertices.pop()
    neighbors = [u for u in G[v] if u in vertices]

    if not neighbors:
        if vertex_cover := backtracking_optimized(G, k, E, vertices, chosen_vertices):
            return vertex_cover
        vertices.add(v)
        return False

    if len(neighbors) > 1:
        removed_edges = remove_edges(G, E, v)
        chosen_vertices.add(v)

        if vertex_cover := backtracking_optimized(G, k - 1, E, vertices, chosen_vertices):
            return vertex_cover

        chosen_vertices.remove(v)
        for edge in removed_edges:
            E.add(edge)

    vertices.add(v)

    if 1 <= len(neighbors) <= k:
        removed_edges = []
        for u in neighbors:
            removed_edges.append(remove_edges(G, E, u))
            chosen_vertices.add(u)
            vertices.remove(u)

        if vertex_cover := backtracking_optimized(G, k - len(neighbors), E, vertices, chosen_vertices):
            return vertex_cover

        for u in neighbors:
            chosen_vertices.remove(u)
            vertices.add(u)

        for edges in removed_edges:
            for edge in edges:
                E.add(edge)

    return False

