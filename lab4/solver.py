from utils.dimacs import loadCNF
from typing import Union
from copy import deepcopy
from .sat2cnf import sat2cnf
from .CNF import CNF


def solve(cnf: CNF, var: int) -> Union[set[int], bool]:
    cnf.values.add(var)
    if not cnf.propagation(var):
        return False
    if not cnf.clauses:
        return cnf.values

    if cnf.check_if_2_cnf():
        sol = sat2cnf(cnf.dimacs_form())
        if not sol:
            return False
        return sol.union(cnf.values)

    new_var = cnf.get_variable_with_highest_count()
    return solve(deepcopy(cnf), new_var) or solve(cnf, -new_var)


def check_correctness(formula, sol):
    for x in sol:
        assert -x not in sol

    for clause in formula:
        for x in clause:
            if x in sol:
                break
        else:
            raise AssertionError
    print("OK")


def main() -> None:
    filenames = ["lab4/sat_tests/r30_01.dyn.14.sat",
                 "lab4/sat_tests/r30_01.dyn.15.sat",
                 "lab4/sat_tests/r30_01.fast.14.sat",
                 "lab4/sat_tests/r30_01.fast.15.sat",
                 "lab4/sat_tests/r30_01.ins.14.sat",
                 "lab4/sat_tests/r30_01.ins.15.sat"]

    for n, sat_formula in map(loadCNF, filenames):
        cnf = CNF(n, sat_formula)
        if not cnf.initial_simplifications():
            print("UNSAT")
            continue
        if not cnf.clauses:
            sol = cnf.values
            check_correctness(sat_formula, sol)
        else:
            var = cnf.get_random_variable()
            sol = solve(deepcopy(cnf), var) or solve(cnf, -var)
            if sol:
                check_correctness(sat_formula, sol)
            else:
                print("UNSAT")


if __name__ == "__main__":
    main()
