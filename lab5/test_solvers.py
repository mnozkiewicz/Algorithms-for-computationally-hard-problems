from os import listdir
from os.path import isfile, join
from utils import dimacs
import multiprocessing
import pycosat
from dp_reduction import reduce_to_sat
from sorter_net import sorter_net


def find_min_vertex_cover(graph_name: str, sat_reducer: callable) -> None:
    graph = dimacs.loadGraph(f"graph/{graph_name}")
    n = len(graph)
    solution = []
    for i in range(1, n + 1):
        sat = sat_reducer(graph, i)
        sol = pycosat.solve(sat)
        if sol == "UNSAT":
            continue
        solution = list(filter(lambda x: 0 < x < n, sol))
        break

    dimacs.saveSolution(f"graph/{graph_name}.sol", set(solution))


def main() -> None:
    graph_names = [f for f in listdir("graph") if isfile(join("graph", f))]
    graph_names = list(filter(lambda name: name.find(".") < 0, graph_names))

    for graph_name in graph_names:
        print(graph_name)

        process = multiprocessing.Process(
            target=find_min_vertex_cover,
            name="solve",
            args=(graph_name, sorter_net),
        )

        process.start()
        process.join(timeout=5)
        process.terminate()


if __name__ == '__main__':
    main()
