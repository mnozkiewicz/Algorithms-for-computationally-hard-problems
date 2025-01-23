
def swap(v: int, u: int) -> tuple[int, int]:
    return (v, u) if v < u else (u, v)


def choose_best(G: list[set[int]], edge_set: set[tuple[int, int]]) -> tuple[int, int]:
    max_degree, best_v, best_u = -1, -1, -1
    for v, u in list(edge_set):
        v, u = swap(v, u)
        if (degree := len(G[v]) + len(G[u])) > max_degree:
            max_degree = degree
            best_v, best_u = v, u
    return best_v, best_u


def solve_two_approx(G: list[set[int]], E: list[tuple[int, int]]) -> set[int]:
    edge_set = set([swap(v, u) for v, u in E])
    vertex_cover = set()
    while edge_set:
        v, u = choose_best(G, edge_set)
        edge_set.remove((v, u))
        for s in G[v]:
            edge_set.discard(swap(v, s))
        for s in G[u]:
            edge_set.discard(swap(u, s))
        vertex_cover.add(v)
        vertex_cover.add(u)

    return vertex_cover
