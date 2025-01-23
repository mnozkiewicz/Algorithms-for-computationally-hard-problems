import sys
import multiprocessing
from copy import deepcopy
from utils.grademe import graphs
from utils import dimacs
from .algorithms import backtracking, backtracking_optimized, brute_force, fast_sol
from .kernel_methods import kernel_solve

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
    dimacs.saveSolution(f"lab1/graph/{graph_name}.sol", vertex_cover)


def main():
    for graph_name in graphs:
        print(graph_name)
        G = dimacs.loadGraph(f"lab1/graph/{graph_name}")
        E = dimacs.edgeList(G)

        process = multiprocessing.Process(
            target=min_vertex_cover,
            name="solve",
            args=(graph_name, G, kernel_solve),
        )

        process.start()
        process.join(timeout=5)
        process.terminate()


if __name__ == "__main__":
    main()
