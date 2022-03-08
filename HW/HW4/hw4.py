import random
import math


class Environment:
    """
     Class of object environment
    """

    def __init__(self, x_boundary: int, y_boundary: int, is_random_weight=True) -> None:
        """
        __init__ Constructs object of Environment.

        Args:
            x_boundary (int): X boundary of the environment.
            y_boundary (int): Y boundary of the environment.
        """
        self.grid = list()
        self.boundaries = [int(x_boundary), int(y_boundary)]
        self.visited = list()
        # Sets all indexes to empty cell
        for x in range(self.boundaries[0]):
            self.grid.append(list())
            for y in range(self.boundaries[1]):
                if is_random_weight:
                    #                   (status,weight,heuristics)
                    self.grid[x].append(0, random.randint(0, 20), math.sqrt(
                        (self.boundaries[0]-1-x)**2)+((self.boundaries[1]-1-y)**2))

        # sets boundary to exit
        self.grid[self.x_boundary][self.y_boundary] = 3

        # Generates Wall locations
        for _ in range(int((self.boundaries[0])*(self.boundaries[1]))):
            while True:
                if self.grid[x][y] != 3 and (x, y) != (0, 0):
                    x = random.randint(0, self.boundaries[0]-1)
                    y = random.randint(0, self.boundaries[1]-1)
                    self.grid[x][y] = 1
                    break


class Agent:
    """
     Class of an Agent
    """

    def __init__(self, location_x: int, location_y: int, environment: Environment):
        """
        __init__ Constructs object of an Agent.

        Args:
            location_x (int): x location of Agent.
            location_y (int): y location of Agent.
            environment (Environment): takes in an environment.
        """
        self.location_x = location_x
        self.location_y = location_y
        self.environment = environment

    def move_left(self):
        self.location_x -= 1

    def move_right(self):
        self.location_x += 1

    def move_down(self):
        self.location_y += 1

    def move_up(self):
        self.location_y -= 1

    def move(self):
        randVal = random.randint(1, 4)

        if randVal == 1:
            if self.location_x - 1 >= 0:
                # if not wall
                if self.environment.grid[self.location_x - 1][self.location_y] != 1:
                    self.move_left()
            else:
                self.move()
        if randVal == 2:
            if self.location_x + 1 < self.environment.boundaries[0]:
                # if not wall
                if self.environment.grid[self.location_x + 1][self.location_y] != 1:
                    self.move_right()
            else:
                self.move()
        if randVal == 3:
            if (self.location_y - 1 >= 0):
                # if not wall
                if self.environment.grid[self.location_x][self.location_y - 1] != 1:
                    self.move_up()
            else:
                self.move()
        if randVal == 4:
            if self.location_y + 1 < self.environment.boundaries[1]:
                # if not wall
                if self.environment.grid[self.location_x][self.location_y + 1] != 1:
                    self.move_down()
            else:
                self.move()
        print(self.location_x, self.location_y)

    def clean(self):
        pos = self.environment.grid[self.location_x][self.location_y]
        if pos == 0:
            pos = 2

        if not pos:
            pass


def main():

    results = []

    env = Environment(10, 10)
    agent = Agent(0, 0, env)


if __name__ == '__main__':
    main()
