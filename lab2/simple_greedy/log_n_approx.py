from queue import PriorityQueue


def solve_log_n_approx(G: list[set[int]], E: list[tuple[int, int]]) -> set[int]:
    n = len(G)
    vertex_cover = set()
    pq = PriorityQueue()
    degree_count = 0
    for i in range(n):
        degree_count += len(G[i])
        pq.put((-len(G[i]), i))

    while not pq.empty() and degree_count > 0:
        degree, v = pq.get()
        if -degree == len(G[v]) and v not in vertex_cover:
            for u in list(G[v]):
                G[u].remove(v)
                G[v].remove(u)
                degree_count -= 2
                pq.put((-len(G[u]), u))
            vertex_cover.add(v)

    return vertex_cover
