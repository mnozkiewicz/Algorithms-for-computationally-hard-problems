import pycosat
import matplotlib.pyplot as plt
from random import randrange, choice


def generate_random_cnf(k: int, n: int, m: int):
    value = [-1, 1]
    cnf = [[randrange(1, n + 1)*choice(value) for _ in range(k)] for _ in range(m)]
    return cnf


if __name__ == '__main__':
    k_value = 3
    n_value = 10
    T = 100
    a = 1
    a_values = []
    true_count = []
    while a <= 10.0:
        count = 0
        for _ in range(T):
            k_cnf = generate_random_cnf(k_value, n_value, int(a*n_value))
            sol = pycosat.solve(k_cnf)
            if sol != "UNSAT":
                count += 1
        a_values.append(a)
        true_count.append(count / T)
        a += 0.1

    plt.plot(a_values, true_count)
    plt.show()
