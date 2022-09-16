# -*- coding: utf-8 -*-
"""
AI Homework 4
Authors: Kaleb Gearinger and Benjamin Goldstone
Description:
    Creates a grid like environment of specified size for which it creates
    connections. It has functions to print and return various different things
    and is able to keep track of the status of a square by simply having a number
    0-3 that all mean something different. 0 = empty, 1 = wall, 2 = visited, and
    3 = exit.
"""

# Imports random to be used in rng for weights attributed to squares
import random
import math

class Environment:

    def __init__(self, x_boundary: int, y_boundary: int, is_random_weight=True) -> None:
        """
        __init__ Constructs object of Environment.

        Args:
            x_boundary (int): X boundary of the environment.
            y_boundary (int): Y boundary of the environment.
        """
        self.grid = list()
        # zero matrix
        self.boundaries = [int(x_boundary), int(y_boundary)]
        self.matrix = [[0 for _ in range(self.boundaries[0]*self.boundaries[1])]
                       for _ in range(self.boundaries[0]*self.boundaries[1])]
        self.visited = list()
        # Sets all indexes to empty cell
        for x in range(self.boundaries[0]):
            self.grid.append(list())
            for y in range(self.boundaries[1]):
                if is_random_weight:
                    #                   (status, heuristics)
                    self.grid[x].append([0, math.sqrt(
                        ((self.boundaries[0]-1-x)**2)+((self.boundaries[1]-1-y)**2))])

        # sets boundary to exit
        self.grid[self.boundaries[0]-1][self.boundaries[1]-1] = (3, 0)


        # Matrix range(100)
        for x in range(int(self.boundaries[0]*self.boundaries[1])):
            # if left
            if x % self.boundaries[0] != 0:
                if self.matrix[x][x-1] == 0:
                    self.matrix[x][x-1] = random.randint(1, 20)
                    self.matrix[x-1][x] = random.randint(1, 20)

            # if right
            if x % self.boundaries[0] != self.boundaries[0]-1:
                if self.matrix[x][x+1] == 0:
                    self.matrix[x][x+1] = random.randint(1, 20)
                    self.matrix[x+1][x] = random.randint(1, 20)

            # if up
            if x - self.boundaries[0] >= 0:
                if self.matrix[x][x-self.boundaries[0]] == 0:
                    self.matrix[x][x-self.boundaries[0]] = random.randint(1, 20)
                    self.matrix[x-self.boundaries[0]][x] = random.randint(1, 20)

            # if down
            if x + self.boundaries[0] < int(self.boundaries[0]*self.boundaries[1]):
                if self.matrix[x][x+self.boundaries[0]] == 0:
                    self.matrix[x][x+self.boundaries[0]] = random.randint(1, 20)
                    self.matrix[x+self.boundaries[0]][x] = random.randint(1, 20)

    # Checks if wall is at location x,y
    def is_wall(self, x, y):
        return self.grid[int(x)][int(y)] == 1
    
        # Generates Wall locations
    def create_wall(self):
        for _ in range(7):
            while True:
                x = random.randint(0, self.boundaries[0]-1)
                y = random.randint(0, self.boundaries[1]-1)
                #checks if this random node is not a wall, entrance, or exit.
                if not ((x == self.boundaries[0]-1 and y == self.boundaries[1]-1) or (x == 0 and y == 0) or self.grid[x][y] == 1):
                    self.grid[x][y] = 1
                    
                    # Removes Connections to/from Walls
                    for index in range(self.boundaries[0]*self.boundaries[1]):
                        self.matrix[x+(y*self.boundaries[0])][index] = 0
                        self.matrix[index][x+(y*self.boundaries[0])] = 0
                    break
      
    # Function to change status of square on grid to visited
    def visit(self, x, y):
        self.grid[x][y][0] = 2
    
    """
    Returns the total number of vistited tiles and takes in the arguement
    of a boolean that holds whether or not the exit was reached to tell the
    function whether or not to add one additional value to the number of
    tiles visited
    """
    def returnNumOfVisited(self, boolean):
        numOfVisited = 0
        # Iterates through all tiles and checks the status
        for x in range(self.boundaries[0]):
            for y in range(self.boundaries[1]):
                if self.grid[x][y] != 1:
                    if self.grid[x][y][0] == 2:
                        numOfVisited += 1
        if not boolean:
            numOfVisited += 1
        return(numOfVisited)
    
    # Prints the grid without heurisitic value for clear visual of grid
    def print_without_heurisics(self):
        # Creates new value to temporarily hold the it called map
        Map = list()
        # Iterates through grid
        for y in range(self.boundaries[1]):
            templist = []
            for x in range(self.boundaries[0]):
                # If the value at the grid is 1,2,3 there is no heuristic
                # value assigned anymore
                if self.grid[x][y] == 1:
                    templist.append(1)
                elif self.grid[x][y] == 3:
                    templist.append(3)
                elif self.grid[x][y] == 2:
                    templist.append(2)
                # Otherwise add only the 0 to the grid and not the heuristic
                else:
                    templist.append(self.grid[x][y][0])
            # Appends the rows into the 2d list
            Map.append(templist)
        # Formats the map into a grid format and prints
        print(*Map, sep = "\n")

    # Prints the adjacency matrix
    def printAdjacencyMatrix(self):
        print(*self.matrix, sep = "\n")