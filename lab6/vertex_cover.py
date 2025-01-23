from os import listdir
from os.path import isfile, join
from utils import dimacs
import pulp
import multiprocessing

def find_min_vertex_cover(graph_name: str) -> None:
    graph = dimacs.loadGraph(f"lab6/graph/{graph_name}")
    n = len(graph)

    model = pulp.LpProblem("min_vertex_cover", pulp.LpMinimize)
    vertex_vars = [pulp.LpVariable(f"x_{i}", cat="Binary") for i in range(n)]

    model += sum(vertex_vars)

    edges = [(a, b) for a in range(n) for b in graph[a] if a < b]

    for a, b in edges:
        model += vertex_vars[a] + vertex_vars[b] >= 1
    
    model.solve()
    solution = [i for i, x in enumerate(vertex_vars) if x.value() > 0.0]
    dimacs.saveSolution(f"lab6/graph/{graph_name}.sol", set(solution))


def relaxed_vertex_cover(graph_name: str) -> None:
    graph = dimacs.loadGraph(f"lab6/graph/{graph_name}")
    n = len(graph)

    model = pulp.LpProblem("relaxed_vertex_cover", pulp.LpMinimize)
    vertex_vars = [pulp.LpVariable(f"x_{i}", lowBound = 0.0, upBound = 1.0, cat="Continous") for i in range(n)]

    model += sum(vertex_vars)

    edges = [(a, b) for a in range(n) for b in graph[a] if a < b]
    for a, b in edges:
        model += vertex_vars[a] + vertex_vars[b] >= 1
    
    model.solve()
    solution = [i for i, x in enumerate(vertex_vars) if x.value() >= 0.5]
    dimacs.saveSolution(f"lab6/graph/{graph_name}.sol", set(solution))



def main() -> None:
    graph_names = [f for f in listdir("lab6/graph") if isfile(join("lab6/graph", f))]
    graph_names = list(filter(lambda name: name.find(".") < 0, graph_names))

    for graph_name in graph_names:
        print(graph_name)
        
        process = multiprocessing.Process(
            target=relaxed_vertex_cover,
            name="solve",
            args=(graph_name, ),
        )

        process.start()
        process.join(timeout=5)
        process.terminate()

if __name__ == '__main__':
    main()