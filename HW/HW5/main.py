"""
    main.py runs graph coloring problem constraint satisfaction problem.
    Date: 3/20/2022
    Authors: Ben Goldstone and Kaleb Gearinger
    Professor: Jorge Silveyra
"""

import random
import sys
import time
from copy import deepcopy

from backtracking import simple_backtrack_recurse
from gcp import GraphColoringProblem
from csp_improvements import find_most_constrained_variable


def is_solution(solution):
    if None in solution.values():
        print("No Solution")
    else:
        print(solution)


def main():
    """
    main Main Runner for Graph Coloring Problem.
    """
    for i in range(1):
        print(f'\n\nTrial #{i+1}\n\n')
        sys.setrecursionlimit(10**9)
        gcp = GraphColoringProblem()
        gcp2 = deepcopy(gcp)
        gcp3 = deepcopy(gcp)
        gcp4 = deepcopy(gcp)
        gcp5 = deepcopy(gcp)
        gcp6 = deepcopy(gcp)
        gcp7 = deepcopy(gcp)
        gcp8 = deepcopy(gcp)
        gcp9 = deepcopy(gcp)
        gcp10 = deepcopy(gcp)
        gcp11 = deepcopy(gcp)
        gcp12 = deepcopy(gcp)
        gcp13 = deepcopy(gcp)
        gcp14 = deepcopy(gcp)
        gcp15 = deepcopy(gcp)
        gcp16 = deepcopy(gcp)
        print(gcp.constraints)
        print()
        color_assignments = {variable: None for variable in gcp.variables}
        print("-------------------------------------------------------")
        print("No additions")
        print("-------------------------------------------------------")
        solution, iterations = simple_backtrack_recurse(
            gcp, deepcopy(color_assignments), False, False, False, False)
        is_solution(solution)
        print(iterations)
        print("-------------------------------------------------------")
        print("One improvement")
        print("-------------------------------------------------------")
        print("Just Most Constrained Variable")
        solution, iterations = simple_backtrack_recurse(
            gcp2, deepcopy(color_assignments), True, False, False, False)
        is_solution(solution)
        print(iterations)
        print("Just Most Constraining Variable")
        solution, iterations = simple_backtrack_recurse(
            gcp3, deepcopy(color_assignments), False, True, False, False)
        is_solution(solution)
        print(iterations)
        print("Just Least Constraining Value")
        solution, iterations = simple_backtrack_recurse(
            gcp4, deepcopy(color_assignments), False, False, True, False)
        is_solution(solution)
        print(iterations)
        print("Just Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp5, deepcopy(color_assignments), False, False, False, True)
        is_solution(solution)
        print(iterations)
        print("-------------------------------------------------------")
        print("Two improvements")
        print("-------------------------------------------------------")
        print("Most Constrained Variable and Most Constraining Variable")
        solution, iterations = simple_backtrack_recurse(
            gcp6, deepcopy(color_assignments), True, True, False, False)
        is_solution(solution)
        print(iterations)
        print("Most Constrained Variable and Least Constraining Value")
        solution, iterations = simple_backtrack_recurse(
            gcp7, deepcopy(color_assignments), True, False, True, False)
        is_solution(solution)
        print(iterations)
        print("Most Constrained Variable and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp8, deepcopy(color_assignments), True, False, False, True)
        is_solution(solution)
        print(iterations)
        print("Most Constraining Variable and Least Constraining Value")
        solution, iterations = simple_backtrack_recurse(
            gcp9, deepcopy(color_assignments), False, True, True, False)
        is_solution(solution)
        print(iterations)
        print("Most Constraining Variable and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp10, deepcopy(color_assignments), False, True, False, True)
        is_solution(solution)
        print(iterations)
        print("Least Constraining Value and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp11, deepcopy(color_assignments), False, False, True, True)
        is_solution(solution)
        print(iterations)
        print("-------------------------------------------------------")
        print("Three improvements")
        print("-------------------------------------------------------")
        print("Most Constrained Variable, Most Constraining Variable, and Least Constraining Value")
        solution, iterations = simple_backtrack_recurse(
            gcp12, deepcopy(color_assignments), True, True, True, False)
        is_solution(solution)
        print(iterations)
        print("Most Constrained Variable, Most Constraining Variable, and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp13, deepcopy(color_assignments), True, True, False, True)
        is_solution(solution)
        print(iterations)
        print("Most Constrained Variable, Least Constraining Value, and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp14, deepcopy(color_assignments), True, False, True, True)
        is_solution(solution)
        print(iterations)
        print("Most Constraining Variable, Least Constraining Value, and Forward Checking")
        solution, iterations = simple_backtrack_recurse(
            gcp15, deepcopy(color_assignments), False, True, True, True)
        is_solution(solution)
        print(iterations)
        print("-------------------------------------------------------")
        print("All improvements")
        print("-------------------------------------------------------")
        solution, iterations = simple_backtrack_recurse(
            gcp16, deepcopy(color_assignments), True, True, True, True)
        is_solution(solution)
        print(iterations)


if __name__ == "__main__":
    main()
