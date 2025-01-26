from utils import dimacs
from os import listdir
from os.path import isfile, join
from itertools import combinations
from math import inf
from typing import Generator


def create_subgraph_from_vertices(vertices: set[int], full_graph: list[set[int]]) -> dict[set, set[int]]:
    subgraph = {v: set() for v in vertices}
    for a, b in combinations(vertices, 2):
        if b in full_graph[a]:
            subgraph[a].add(b)
            subgraph[b].add(a)
    return subgraph


class Bag(dimacs.Bag):

    def __init__(self, base_instance: dimacs.Bag, graph: list[set[int]]):
        self.__dict__ = base_instance.__dict__.copy()
        self.bag = set() if not self.bag else self.bag

        self.id_mapping = dict(zip(self.bag, range(len(self.bag))))

        self.full_graph = graph
        self.subgraph = create_subgraph_from_vertices(self.bag, graph)
        self.subgraph_edges = [(a, b) for a, neighbors in self.subgraph.items() for b in neighbors if a < b]

        self.dp = [-1 for _ in range(1 << len(self.bag))]


    def encode_vertices(self, vertices: list[int]) -> int:
        mask = 0
        for v in vertices:
            mask |= 1 << self.id_mapping[v]
        return mask


    def is_vertex_cover(self, vertices: set[int]) -> bool:
        for a, b in self.subgraph_edges:
            if a not in vertices and b not in vertices:
                return False
        return True



def load_graph_and_decompostions(graph_name: str, tree_comp: str) -> tuple[list[set[int]], list[dimacs.Bag]]:
    graph = dimacs.loadGRGraph(f"lab7/graphs/{graph_name}")
    tree_width = dimacs.loadDecomposition(f"lab7/graphs/{tree_comp}")
    return graph, tree_width

def generate_subsets(vertices: set[int]) -> Generator[set[int], None, None]:
    for s in range(len(vertices) + 1):
        for c in combinations(vertices, s):
            yield set(c)
    return


def f(node: Bag, subset: set[int], bags: list[Bag]):
    mask = node.encode_vertices(subset)
    if node.dp[mask] < 0:
        if not node.is_vertex_cover(subset):
            node.dp[mask] = inf
        else:
            dp_value = len(subset)
            for child in node.children:
                child_node = bags[child]

                child_parent_intersect = subset & child_node.bag
                c_p_int_size = len(child_parent_intersect)
                best_value = inf

                for child_subset in generate_subsets(child_node.bag):
                    if (child_subset & node.bag) == child_parent_intersect:
                        best_value = min(best_value, f(child_node, child_subset, bags) - c_p_int_size)

                dp_value += best_value
                if best_value == inf:
                    break
            node.dp[mask] = dp_value

    return node.dp[mask]


def find_min_vertex_cover(graph_name: str, tree_comp: str):
    graph, tree_decomp = load_graph_and_decompostions(graph_name, tree_comp)
    tree_decomp = list(map(lambda x: Bag(x, graph), tree_decomp))

    root = tree_decomp[1]
    ans = inf
    for subset in generate_subsets(root.bag):
        ans = min(ans, f(root, subset, tree_decomp))

    print(f"Minimal vertex cover size: {ans}")


def main():
    files = [f for f in listdir("lab7/graphs") if isfile(join("lab7/graphs", f))]
    graph_names = sorted(filter(lambda name: name.find(".gr") >= 0, files))
    tree_names = sorted(filter(lambda name: name.find(".tw") >= 0, files))

    for graph_name, tree_name in zip(graph_names, tree_names):
        print(graph_name, tree_name)
        if graph_name == "b20.gr" or graph_name == "k330_a.gr":
            continue
        find_min_vertex_cover(graph_name, tree_name)


if __name__ == '__main__':
    main()