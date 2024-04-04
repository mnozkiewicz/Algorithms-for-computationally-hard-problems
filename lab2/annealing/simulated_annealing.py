import random
from math import exp, inf
import matplotlib.pyplot as plt
from lab2.annealing.list_set import ListSet


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


def annealing(G: list[set], k: int, steps=100, T0=100, alpha=0.95, target=-inf):
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


def simulated_annealing(G: list[set], E: list[tuple], show_plot=False) -> set[int]:
    vertex_cover = False
    energy_states = []
    m = len(E)
    for i in range(1, len(G)):
        vertex_cover, energy, energy_states = annealing(G, i, target=-m)
        if -energy == m:
            break

    if show_plot:
        plt.plot(list(range(len(energy_states))), energy_states)
        plt.show()

    return set(vertex_cover)
