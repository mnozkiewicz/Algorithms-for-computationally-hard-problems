from os import listdir
from os.path import isfile, join
from utils import dimacs
import pandas as pd
import pulp
from typing import Optional


def get_metadata() -> pd.Series:
    metadata = pd.read_csv(f"lab6/coloring-test-data/metadata.csv", index_col=0)
    colorings = metadata["X(G)"]
    return colorings

def read_graph(graph_name: str, metadata: pd.Series) -> tuple[list[set[int]], int]:
    graph = dimacs.loadGraph(f"lab6/coloring-test-data/{graph_name}")
    key = graph_name.split(".")[0]
    answer = metadata.get(key, default=-1)
    return graph, answer


def find_graph_coloring(graph: list[set[int]], k: int) -> Optional[dict[int, int]]:
    n = len(graph)

    model = pulp.LpProblem("graph_coloring",)
    vertex_colors = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(k)] for i in range(n)]

    for i in range(n):
        row_sum = sum(vertex_colors[i])
        model += row_sum == 1
    
    edges = [(a, b) for a in range(n) for b in graph[a] if a < b]
    for a, b in edges:
        for j in range(k):
            model += vertex_colors[a][j] + vertex_colors[b][j] <= 1

    solver = pulp.PULP_CBC_CMD(msg=False) 
    status = model.solve(solver)

    if pulp.LpStatus[status] != "Optimal":
        return None

    colors = {}
    for i in range(n):
        for j in range(k):
            if vertex_colors[i][j].value() > 0.0:
                colors[i] = j
                break
    return colors


def find_min_graph_coloring(graph: list[set[int]]) -> Optional[dict[int, int]]:
    n = len(graph)

    model = pulp.LpProblem("graph_coloring", pulp.LpMinimize)
    vertex_colors = [[pulp.LpVariable(f"x_{i}_{j}", cat="Binary") for j in range(n)] for i in range(n)]

    for i in range(n):
        row_sum = sum(vertex_colors[i])
        model += row_sum == 1
    
    edges = [(a, b) for a in range(n) for b in graph[a] if a < b]
    for a, b in edges:
        for j in range(n):
            model += vertex_colors[a][j] + vertex_colors[b][j] <= 1


    color_vars = [pulp.LpVariable(f"y_{i}", cat="Binary") for i in range(n)]
    for i in range(n):
        for j in range(n):
            model += color_vars[i] >= vertex_colors[j][i]

    model += sum(color_vars)

    solver = pulp.PULP_CBC_CMD(msg=False) 
    status = model.solve(solver)

    colors = {}
    for i in range(n):
        for j in range(n):
            if vertex_colors[i][j].value() > 0.0:
                colors[i] = j
    return colors
        


def main() -> None:
    graph_names = [f for f in listdir("lab6/coloring-test-data/") if isfile(join("lab6/coloring-test-data", f))]
    graph_names = list(filter(lambda name: name.find(".sol") < 0, graph_names))
    colorings = get_metadata()

    for i, graph_name in enumerate(graph_names):
        graph, ans = read_graph(graph_name, colorings)
        if ans == -1:
            continue
        print("\n", graph_name, ans)
        color_map = find_min_graph_coloring(graph)
        print(f"Distinct colors: {len(set(color_map.values()))}")

        # color_map = find_graph_coloring(graph, ans)
        # if color_map:
        #     print("Found coloring")
        # else:
        #     print("Coloring was not found")
        
        # color_map = find_graph_coloring(graph, ans - 1)
        # if color_map:
        #     print("Found coloring")
        # else:
        #     print("Coloring was not found")



if __name__ == '__main__':
    main()