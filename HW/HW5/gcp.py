"""
    gcp.py contains the GraphColoringProblem object.
    Date: 3/20/2022
    Authors: Ben Goldstone and Kaleb Gearinger
    Professor: Jorge Silveyra
"""

import random
from typing import List, Dict


class GraphColoringProblem:
    """
     class for the Graph coloring problem
    """

    def __init__(self) -> None:
        """
        __init__ Constructor for the GraphColoringProblem class.
        """
        self.variables = ["WA", "NT", "Q", "NSW", "V", "SA", "T"]
        self.domains = ["red", "green", "blue"]
        self.constraints = {}
        random.shuffle(self.variables)
        # puts list in dictionary
        for variable in self.variables:
            self.constraints[variable] = []

        for variable in self.variables:
            for connection in self.variables:
                if (random.random() < .3) and not (connection in self.constraints[variable]) and connection != variable:
                    self.constraints[variable].append(connection)
                    self.constraints[connection].append(variable)
        self.color_choices = {}
        for variable in self.variables:
            self.color_choices[variable] = self.domains[:]

    def get_constraints(self, variable: str) -> List:
        """
        get_constraints Gets the constraints for a given variable.

        Args:
            variable (str): Variable that you would like the constraints for.

        Returns:
            List: list of the constraints for the given variable.
        """
        return self.constraints[variable]

    def is_legal(self, variable: str, color: str, color_assignments: Dict) -> bool:
        """
        is_legal Checks if the color is a legal move.

        Args:
            variable (str): variable to check.
            color (str): color to check against constraints.
            color_assignments (Dict): existing color assignments.

        Returns:
            bool: true if move is legal.
        """

        # if no constraints, do any move.
        if len(self.get_constraints(variable)) == 0:
            return True
        return len([constraint for constraint in self.get_constraints(variable) if color_assignments[constraint] == color]) == 0
