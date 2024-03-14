from lab1.dimacs import remove_vertex
from lab1.solutions.fast_backtracking import fast_sol


def degree_one(G: list[set], chosen_vertices: set):
    one = -1
    for v in range(len(G)):
        if len(G[v]) == 1:
            one = v
            break

    if one < 0:
        return False

    u = next(iter(G[one]))
    remove_vertex(G, u)
    chosen_vertices.add(u)
    return True


def degree_k(G: list[set], chosen_vertices: set, k: int):
    deg_k = -1
    for v in range(len(G)):
        if len(G[v]) > k:
            deg_k = v
            break
    if deg_k < 0:
        return False
    remove_vertex(G, deg_k)
    chosen_vertices.add(deg_k)
    return True


def kernelize(G: list[set], k: int):
    chosen_vertices = set()
    while k > 0:
        if degree_one(G, chosen_vertices) or degree_k(G, chosen_vertices, k):
            k -= 1
            continue
        break

    return G, k, chosen_vertices


def kernel_solve(G: list[set[int]], k: int):
    G, k, chosen_vertices = kernelize(G, k)
    if sum(len(neighbors) for neighbors in G) // 2 > k**2:
        return False
    if vertex_cover := fast_sol(G, k, chosen_vertices):
        return vertex_cover
    return False

