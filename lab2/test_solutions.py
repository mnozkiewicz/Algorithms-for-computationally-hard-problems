import sys
from utils.grademe import graphs
from utils import dimacs
import random
from math import exp, inf
import matplotlib.pyplot as plt
from list_set import ListSet


sys.setrecursionlimit(10000)


def calculate_energy(G: list[set], vertices: ListSet):
    both = 0
    one = 0
    for v in range(len(G)):
        for u in G[v]:
            if v in vertices and u in vertices:
                both += 1
            elif v in vertices:
                one += 1
    return -((both // 2) + one)


def f(delta, T):
    return exp(-delta/T)


def annealing(G: list[set], k: int, steps=1000, T0=100, alpha=0.99, target=-inf):
    n = len(G)
    vertices = [True for _ in range(k)] + [False for _ in range(n - k)]
    random.shuffle(vertices)

    chosen = ListSet([i for i, val in enumerate(vertices) if val])
    not_chosen = ListSet([i for i, val in enumerate(vertices) if not val])

    cur_energy = calculate_energy(G, chosen)
    T = T0

    energy_states = [cur_energy]
    temperature = [T0]
    best_energy = cur_energy
    best_set = chosen.copy()

    for i in range(steps):
        first, second = random.choice(chosen), random.choice(not_chosen)

        chosen.remove(first)
        not_chosen.remove(second)
        chosen.add(second)
        not_chosen.add(first)

        next_energy = calculate_energy(G, chosen)

        if next_energy < cur_energy:
            cur_energy = next_energy
        else:
            probability = f(next_energy - cur_energy, T)
            if probability > random.uniform(0, 1):
                cur_energy = next_energy
            else:
                chosen.remove(second)
                not_chosen.remove(first)
                chosen.add(first)
                not_chosen.add(second)

        if cur_energy < best_energy:
            best_energy = cur_energy
            best_set = chosen.copy()

        if cur_energy <= target:
            break
        T *= alpha
        temperature.append(T)
        energy_states.append(cur_energy)

    return best_set, best_energy, energy_states


def simulated_annealing(graph_name: str, G: list[set], E: list[tuple]) -> None:
    vertex_cover = False
    energy_states = []
    m = len(E)
    for i in range(1, len(G)):
        vertex_cover, energy, energy_states = annealing(G, i, target=-m)
        if -energy == m:
            break

    plt.plot(range(len(energy_states)), energy_states)
    plt.show()

    if vertex_cover:
        dimacs.saveSolution(f"graph/{graph_name}.sol", vertex_cover)


def main():
    for graph_name in graphs:
        print(graph_name)
        G = dimacs.loadGraph(f"graph/{graph_name}")
        E = dimacs.edgeList(G)
        simulated_annealing(graph_name, G, E)


if __name__ == "__main__":
    main()
