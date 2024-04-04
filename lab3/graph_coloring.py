from os import listdir
from os.path import isfile, join
from utils import dimacs
import pycosat


def reduce_to_sat(graph: list[set[int]]):
    pass


if __name__ == '__main__':
    filenames = [f"graphs/{f}" for f in listdir("graphs") if isfile(join("graphs", f))][:2]
    graphs = list(map(dimacs.loadGraph, filenames))
    for graph_name, graph_instance in zip(filenames, graphs):
        print(graph_name.split('/')[-1])
        print(graph_instance)
        reduce_to_sat(graph_instance)

