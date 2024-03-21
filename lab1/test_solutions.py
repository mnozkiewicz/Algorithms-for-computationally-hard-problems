import sys
import threading
from copy import deepcopy
from utils.grademe import graphs
from utils import dimacs
from solutions.brute import brute_force
from solutions.simple_backtracking import backtracking
from solutions.backtracking import backtracking_optimized
from solutions.fast_backtracking import fast_sol
from kernel_methods.kernelization import kernel_solve

sys.setrecursionlimit(10000)


def min_vertex_cover(graph_name: str, G: list[set], solver: callable, *args) -> None:
    """
    Searches for min_vertex_cover and saves
    the solution to graph directory if one is found
    """
    vertex_cover = False
    for i in range(1, len(G)):
        vertex_cover = solver(deepcopy(G), i, *args)
        if vertex_cover:
            break
    dimacs.saveSolution(f"graph/{graph_name}.sol", vertex_cover)


def main():
    for graph_name in graphs:
        print(graph_name)
        G = dimacs.loadGraph(f"graph/{graph_name}")
        E = dimacs.edgeList(G)

        thread = threading.Thread(
            target=min_vertex_cover,
            name="solve",
            args=(graph_name, G, backtracking_optimized, set(E), set(range(len(G)))),
            daemon=True
        )

        thread.start()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
