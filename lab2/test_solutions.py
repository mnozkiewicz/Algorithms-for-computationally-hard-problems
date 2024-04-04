from utils.grademe import graphs
from utils import dimacs
from simple_greedy.log_n_approx import log_n_approx
from simple_greedy.two_approx import two_approx
from simple_greedy.remove_random import remove_random
from annealing.simulated_annealing import simulated_annealing


def approximate_min_vertex_cover(graph_name: str, G: list[set], E: list[tuple], solver: callable, *args, **kwargs) -> None:
    vertex_cover = solver(G, E, *args, **kwargs)
    dimacs.saveSolution(f"graph/{graph_name}.sol", vertex_cover)


def main():
    for graph_name in graphs:
        print(graph_name)
        G = dimacs.loadGraph(f"graph/{graph_name}")
        E = dimacs.edgeList(G)
        approximate_min_vertex_cover(graph_name, G, E, simulated_annealing, show_plot=True)
        # approximate_min_vertex_cover(graph_name, G, E, two_approx)
        # approximate_min_vertex_cover(graph_name, G, E, remove_random, two_approx, show_info=True)


if __name__ == "__main__":
    main()
