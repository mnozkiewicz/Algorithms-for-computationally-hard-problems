from utils.grademe import graphs
from utils import dimacs
from .simple_greedy import solve_log_n_approx, solve_remove_random, solve_two_approx
from .annealing import solve_simulated_annealing


def approximate_min_vertex_cover(graph_name: str, G: list[set], E: list[tuple], solver: callable, *args, **kwargs) -> None:
    vertex_cover = solver(G, E, *args, **kwargs)
    dimacs.saveSolution(f"lab2/graph/{graph_name}.sol", vertex_cover)


def main():
    for graph_name in graphs:
        print(graph_name)
        G = dimacs.loadGraph(f"lab2/graph/{graph_name}")
        E = dimacs.edgeList(G)
        approximate_min_vertex_cover(graph_name, G, E, solve_simulated_annealing, show_plot=True)
        # approximate_min_vertex_cover(graph_name, G, E, two_approx)
        # approximate_min_vertex_cover(graph_name, G, E, remove_random, two_approx, show_info=True)


if __name__ == "__main__":
    main()
