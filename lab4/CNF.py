from collections import defaultdict, deque
from typing import Union
import random


class CNF:
    def __init__(self, n: int, formula: list[list[int]]) -> None:
        self.n = n
        self.clauses = dict(zip(range(len(formula)), formula))
        self.var_to_clause = self._create_graph()
        self.values = set()

    def initial_simplifications(self) -> bool:
        queue = deque()
        for clause in self.clauses.values():
            if len(clause) == 1:
                x = clause[0]
                if -x in self.values:
                    return False
                self.values.add(x)
                queue.append(x)

        for key in self.var_to_clause.keys():
            if -key not in self.var_to_clause or len(self.var_to_clause[-key]) == 0:
                self.values.add(key)
                queue.append(key)

        return self.propagation(queue)

    def _create_graph(self) -> dict[int, set[int]]:
        graph = defaultdict(lambda: set())
        for idx, clause in self.clauses.items():
            for var in clause:
                graph[var].add(idx)
        return graph

    def get_random_variable(self) -> int:
        clause = random.choice(list(self.clauses.keys()))
        var = random.choice(self.clauses[clause])
        return var

    def _get_variable_count(self) -> dict[int, int]:
        counter = defaultdict(lambda: 0)
        for clause in self.clauses.values():
            for x in clause:
                counter[abs(x)] += 1
        return counter

    def get_variable_with_highest_count(self) -> int:
        counter = self._get_variable_count()
        best_var = 0
        best_count = -1
        for key, count in counter.items():
            if count > best_count:
                best_var = key
                best_count = count
        return best_var

    def _remove_satisfied_clauses(self, var: int, queue: deque) -> bool:
        for clause_idx in list(self.var_to_clause[var]):
            for x in self.clauses[clause_idx]:
                self.var_to_clause[x].remove(clause_idx)
                if not self.var_to_clause[x] and x not in self.values:
                    self.values.add(-x)
                    queue.append(-x)
            self.clauses.pop(clause_idx)

        return True

    def _remove_var_from_clauses(self, var: int, queue: deque) -> bool:
        for clause_idx in list(self.var_to_clause[var]):
            self.var_to_clause[var].remove(clause_idx)
            self.clauses[clause_idx] = list(
                filter(lambda x: x != var, self.clauses[clause_idx])
            )
            clause = self.clauses[clause_idx]
            if not clause:
                return False
            if len(clause) == 1:
                x = clause[0]
                if -x in self.values:
                    return False
                if x not in self.values:
                    self.values.add(x)
                    queue.append(x)
        return True

    def propagation(self, var: Union[deque[int], int]) -> bool:
        if isinstance(var, int):
            queue = deque([var])
        else:
            queue = var
        while queue:
            var = queue.popleft()
            if var in self.var_to_clause:
                self._remove_satisfied_clauses(var, queue)
            if var in self.var_to_clause:
                if not self._remove_var_from_clauses(-var, queue):
                    return False
        return True

    def check_if_2_cnf(self) -> bool:
        for clause in self.clauses.values():
            if len(clause) > 2:
                return False
        return True

    def dimacs_form(self):
        return [clause for clause in self.clauses.values()]
