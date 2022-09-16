"""
    backtracking.py Implements backtracking algorithms
    Date: 3/20/2022
    Authors: Ben Goldstone and Kaleb Gearinger
    Professor: Jorge Silveyra
"""

import random
from typing import Dict, Union
import time

from gcp import GraphColoringProblem
from csp_improvements import find_most_constrained_variable, find_most_constraining_variable, find_least_constraining_value, find_forward_checking


def simple_backtrack_recurse(gcp: GraphColoringProblem, color_assignments: Dict, most_constrained_variable=False, most_constraining_variable=False, least_constraining_value=False, forward_checking=False, previous_variable=None, iterations=0) -> tuple:
    """
    simple_backtrack_recurse runs the recursion

    Args:
        gcp(GraphColoringProblem): Graph Coloring Problem instance to pass in
        color_assignments(Dict): current color_assignments dictionary.
        most_constrained_variable(bool, optional): Flag if Most Constrained Variable is active. Defaults to False.
        most_constraining_variable(bool, optional): Flag if Most Constraining Variable is active. Defaults to False.
        least_constraining_value(bool, optional): Flag if Least Constraining Value is active. Defaults to False.
        forward_checking(bool, optional): Flag if Forward Checking is active. Defaults to False.
        previous_variable(str,optional): Gets last variable changed before this recursion. Defaults to None.

    Returns:
        Dict: Returns a dictionary of color assignments or None if solution could not be found.
    """

    # if all colors assigned, return color_assignments.
    if not None in color_assignments.values():
        iterations += 1
        return color_assignments, iterations

    # assigns colors to each variable.
    if None in color_assignments.values():
        # checks if most constrained variable.
        if most_constrained_variable:
            variable = find_most_constrained_variable(gcp, color_assignments)
            # checks if more than one constrained variable.
            if len(variable) > 1 and isinstance(variable, list):
                # if most constraining variable is active.
                if most_constraining_variable:
                    variable = find_most_constraining_variable(
                        gcp, color_assignments, variable)
                    # if most constraining variable has more than one and least constraining variable is selected.
                    if len(variable) > 1 and isinstance(variable, list) and least_constraining_value:
                        variable = find_least_constraining_value(
                            gcp, color_assignments, variable)
                # if not most constraining variable and more than one constrained variable, check least constraining value.
                elif least_constraining_value:
                    variable = find_least_constraining_value(
                        gcp, color_assignments, variable)

        # check most constraining variable.
        elif most_constraining_variable:
            variable = find_most_constraining_variable(gcp, color_assignments)
            # if more than one and least constraining value is active.
            if len(variable) > 1 and isinstance(variable, list) and least_constraining_value:
                variable = find_least_constraining_value(
                    gcp, color_assignments, variable)

        # check least constraining value.
        elif least_constraining_value:
            variable = find_least_constraining_value(gcp, color_assignments)

        # if nothing is active, choose a variable that has not been picked.
        else:
            variable = [
                variable for variable in gcp.variables if color_assignments[variable] is None]

        # Choose from list of variables until one works
        for variable in variable:
            # checks forward_checking given the selected variables.

            # if variable does not have color assignment.
            if color_assignments[variable] is None:
                # checks constraint of that color and assigns color.
                for color in gcp.domains:
                    iterations += 1
                    if gcp.is_legal(variable, color, color_assignments):
                        color_assignments[variable] = color
                        # if forward checking is enabled.
                        if forward_checking:
                            backtracking_required = find_forward_checking(
                                gcp, variable, color)
                            print(backtracking_required)
                            if backtracking_required:
                                color_assignments[variable] = None
                                return color_assignments, iterations
                        color_assignments, iterations = simple_backtrack_recurse(
                            gcp, color_assignments, most_constrained_variable, most_constraining_variable, least_constraining_value, forward_checking, variable, iterations)
                # Checks if loop was broken because color chosen has solved the problem
                if not None in color_assignments.values():
                    return color_assignments, iterations

                # If not resets color assignment for variable back to None
                color_assignments[variable] = None
                # if color assignment is still None, backtrack.
                if color_assignments[variable] is None and not (previous_variable is None):
                    # moves a variable back to make sure it does not get stuck and calls recursion.
                    color_assignments[previous_variable] = None
                    return color_assignments, iterations
        return color_assignments, iterations
    # if done return color_assignments
    return color_assignments, iterations
