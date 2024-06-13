from utils import dimacs
from copy import deepcopy
from abc import ABC, abstractmethod
import pycosat

class SorterNet(ABC):
    def __init__(self, n):
        self._n = n
        self._lines = list(range(n + 1))
        self._last_var = n + 1
        self._formulas = []

    def cmp(self, i, j):
        assert i < j, "line i should be above line j"

        last_i, last_j = self._lines[i], self._lines[j]
        new_i, new_j = self._last_var, self._last_var + 1

        self._lines[i] = self._last_var
        self._lines[j] = self._last_var + 1
        self._last_var += 2

        self._formulas.extend([
            [-last_i, -last_j, new_i],
            [-last_i, new_j],
            [-last_j, new_j]
        ])

    def get_threshold_constraint(self, k) -> list[int]:
        assert len(self._lines) >= k, "k should be less than number of lines"
        return [-self._lines[-k - 1]]

    def get_sort_cnf(self):
        self._sort()
        return deepcopy(self._formulas)

    @abstractmethod
    def _sort(self):
        pass


class InsertSortNet(SorterNet):
    def __init__(self, n):
        super().__init__(n)

    def _sort(self):
        for j in range(2, self._n + 1):
            for i in range(1, j):
                self.cmp(i, j)


def power_of_2(n):
    k = 1
    while k < n:
        k *= 2
    return k


class MergeSortNet(SorterNet):
    def __init__(self, n):
        super().__init__(power_of_2(n))

    def _sort(self):
        self._merge_sort(1, self._n)

    def _merge_sort(self, left, right):
        if left + 1 == right:
            self.cmp(left, right)
        elif left < right:
            middle = (left + right) // 2
            self._merge_sort(left, middle)
            self._merge_sort(middle + 1, right)
            self._merge(left, middle, right)

    def _merge(self, left, middle, right):
        for i in range(left, middle + 1):
            self.cmp(i, right + left - i)

        if left < middle:
            self._bitonic_sort(left, middle)
            self._bitonic_sort(middle + 1, right)

    def _bitonic_sort(self, left, right):
        if left + 1 >= right:
            self.cmp(left, right)
            return

        middle = (left + right) // 2
        for i in range(left, middle + 1):
            self.cmp(i, middle - left + i + 1)

        self._bitonic_sort(left, middle)
        self._bitonic_sort(middle + 1, right)


def sorter_net(graph: list[set[int]], k: int) -> list[list[int]]:
    n = len(graph)
    cover_constraints = []
    for v, u in dimacs.edgeList(graph):
        cover_constraints.append([
            v,
            u
        ])

    net = MergeSortNet(n)
    cnf = \
        cover_constraints + \
        net.get_sort_cnf() + \
        [net.get_threshold_constraint(k)]

    return cnf


def main() -> None:
    graph_names = ["graph/e5"]

    for graph_name in graph_names:
        g = dimacs.loadGraph(graph_name)
        print(sorter_net(g, 2))


if __name__ == "__main__":
    main()
