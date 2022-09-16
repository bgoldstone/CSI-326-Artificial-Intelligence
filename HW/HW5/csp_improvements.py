"""
    csp_improvements.py contains CSP improvements for the graph coloring Problem
    Date: 3/20/2022
    Authors: Ben Goldstone and Kaleb Gearinger
    Professor: Jorge Silveyra
"""


from typing import List, Dict
from gcp import GraphColoringProblem
from copy import deepcopy


def find_most_constrained_variable(gcp: GraphColoringProblem, color_assignments: Dict, variable=None) -> List:
    """
    find_most_constrained_variable Finds the most constrained variable(s).

    Args:
        gcp (GraphColoringProblem): Graph Coloring Problem object.
        color_assignments (Dict): current color_assignments dictionary.
        variable (_type_, optional): any variables already selected, if any. Defaults to None.

    Returns:
        List: returns a list of values that are the most constrained variables.
    """
    # gets a list of variables without color.
    non_colored_variables = [
        non_colored_variable for non_colored_variable in gcp.variables if color_assignments[non_colored_variable] is None]
    # dictionary to store number of colors per variable.
    mcv = {}
    # sets the variables to the total number of colors.
    for non_colored_variable in non_colored_variables:
        mcv[non_colored_variable] = len(gcp.domains)
    # gets the number of colors per variable and sets them.
    for var in non_colored_variables:
        list_of_colors = gcp.domains[:]
        for constraint in gcp.get_constraints(var):
            if color_assignments[constraint] in list_of_colors:
                list_of_colors.remove(color_assignments[constraint])
        # sets number of color possibilities.
        mcv[var] = len(list_of_colors)
    # gets the one with the smallest number of color possibilities.
    min_val = min(mcv.values())
    most_constrained = []
    for var in mcv:
        if mcv[var] == min_val:
            most_constrained.append(var)
    # returns list of most constrained variable(s).
    return(most_constrained)


def find_most_constraining_variable(gcp: GraphColoringProblem, color_assignments: Dict, variable=None) -> List:
    """
    find_most_constraining_variable Finds the most constraining variable(s).

    Args:
        gcp (GraphColoringProblem): Graph Coloring Problem object.
        color_assignments (Dict): current color_assignments dictionary.
        variable (_type_, optional): any variables already selected, if any. Defaults to None.

    Returns:
        List: returns a list of values that are the most constraining variables.
    """
    # if variables are already selected, use those, otherwise find variables without color.
    if variable is None:
        variable = [
            non_colored_variable for non_colored_variable in gcp.variables if color_assignments[non_colored_variable] is None]
    # most constraining variable dictionary to store counts.
    mcv = {}
    # sets the count to the number of colors.
    for non_colored_variable in variable:
        mcv[non_colored_variable] = len(gcp.domains)
    # for each variable.
    for var in variable:
        # set count to number of constraints the variable has.
        count = len(gcp.get_constraints(var))
        # for each constraint, if there is a color assignment, subtract one.
        for constraint in gcp.get_constraints(var):
            if not color_assignments[constraint] is None:
                count -= 1
        # store count
        mcv[var] = count
    # gets the most constraining variable max number.
    max_val = max(mcv.values())
    most_constraining = []
    # gets most constraining variable(S).
    for var in mcv:
        if mcv[var] == max_val:
            most_constraining.append(var)
    # returns most constraining variable(s).
    return(most_constraining)


def find_least_constraining_value(gcp: GraphColoringProblem, color_assignments: Dict, variable=None) -> List:
    """
    find_least_constraining_value Finds the least constraining value(s).

    Args:
        gcp (GraphColoringProblem): Graph Coloring Problem object.
        color_assignments (Dict): current color_assignments dictionary.
        variable (_type_, optional): any variables already selected, if any. Defaults to None.

    Returns:
        List: returns a list of variables that meet the least constraining value(s).
    """
    least_constraining_variable_count = {}
    # if variables not passed through
    if variable is None:
        variable = [
            uncolored_variable for uncolored_variable in color_assignments if color_assignments[uncolored_variable] is None]
    # goes through all variables that are uncolored or passed through
    for var in variable:
        list_of_colors = gcp.domains[:]
        # checks each constraint
        for constraint in gcp.get_constraints(var):
            # if there is a color assigned and is in list of colors, remove it.
            if not (color_assignments[constraint] is None) and color_assignments[constraint] in list_of_colors:
                list_of_colors.remove(color_assignments[constraint])
        least_constraining_variable_count[var] = len(list_of_colors)
    # finds minimum counts
    lcv_minimum_count = min(
        least_constraining_variable_count.values())
    # returns values that match least constraining variable count minimum
    return [var for var in least_constraining_variable_count if least_constraining_variable_count[var] == lcv_minimum_count]


# def find_forward_checking(gcp: GraphColoringProblem, color_assignments: Dict, variable) -> Dict:
#     """
#     find_forward_checking Runs forward checking algorithm and returns a dictionary of variables with possible colors.

#     Args:
#        gcp (GraphColoringProblem): Graph Coloring Problem object.
#         color_assignments (Dict): current color_assignments dictionary.
#         variable (_type_, optional): any variables already selected, if any. Defaults to None.
#     Returns:
#         Dict: returns dictionary of variables mapped to possible color possibilities for variables that have not been assigned.
#     """
#     # all colors
#     colors = [color for color in gcp.domains]
#     # color possibilities for uncolored variables
#     color_possibilities = {}
#     # if variable is none, add variables.
#     if variable is None:
#         variable = [
#             non_colored_variable for non_colored_variable in color_assignments if color_assignments[non_colored_variable] is None]
#     # Maps all colors to each variable.
#     for var in variable:
#         color_possibilities[var] = colors
#     # list of colored variables.
#     colored_variables = [
#         var for var in color_assignments if color_assignments[var] is not None]
#     for var in variable:
#         # If variable is not colored variables, get colors for variables.
#         if var not in colored_variables:
#             constraints = gcp.get_constraints(var)
#             # for each constraint of the variable check if color and in color possibilities.
#             for constraint in constraints:
#                 if color_assignments[constraint] is not None and color_assignments[constraint] in color_possibilities[constraint]:
#                     # if color in color_possibilities, remove that color.
#                     color_possibilities[constraint].remove(
#                         color_assignments[constraint])
#     return color_possibilities

def find_forward_checking(gcp: GraphColoringProblem, variable: str, color: str) -> bool:
    """
    find_forward_checking Runs forward checking algorithm and returns a dictionary of variables with possible colors.

    Args:
       gcp (GraphColoringProblem): Graph Coloring Problem object.
        color_assignments (Dict): current color_assignments dictionary.
        variable (str): any variables already selected, if any. Defaults to None.
        color(str): current color
    Returns:
        bool: returns True if the move is not legal.
    """
    temp_color_choices = deepcopy(gcp.color_choices)
    connections = gcp.get_constraints(variable)
    # for each connection, check if color in color_choices.
    for connection in connections:
        if color in gcp.color_choices[connection]:
            # Remove the color from the dictionary
            gcp.color_choices[connection].remove(color)
        if len(gcp.color_choices[connection]) == 0:
            gcp.color_choices = temp_color_choices
            return True
    return False
