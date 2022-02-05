import random
"""
    hw2.py
    Homework 2
    Name: Ben Goldstone, Michael Norton
    Description: Uses a robot vaccum cleaner to clean a given "environment"
"""


class Environment:
    """
     Class of object environment
    """

    def __init__(self, x_boundary: int, y_boundary: int) -> None:
        """
        __init__ Constructs object of Environment.

        Args:
            x_boundary (int): X boundary of the environment.
            y_boundary (int): Y boundary of the environment.
        """
        self.grid = list()
        self.boundaries = [int(x_boundary), int(y_boundary)]
        self.visited = list()
        # gets new environment
        get_new_environment()

    def get_boundary_x(self) -> int:
        """
        get_boundary_x gets boundary of x-axis.

        Returns:
            int: max position of the X-axis.
        """
        return self.boundaries[0]-1

    def get_boundary_y(self) -> int:
        """
        get_boundary_y Gets the boundary of the y-axis.

        Returns:
            int: max position of the Y-axis.
        """
        return self.boundaries[0]-1

    def get_new_environment(self):
        """
        get_new_environment Develops a new Dirty randomized environment.
        """
        self.grid = [[False for _ in range(self.boundaries[1])]
                     for _ in range(self.boundaries[0])]
        # Generates Dirty locations Dirty = True, Clean = False of 50% of environment
        for _ in range(int(((self.boundaries[0])*(self.boundaries[1]))/2)):
            x = random.randint(0, self.boundaries[0]-1)
            y = random.randint(0, self.boundaries[1]-1)
            if not self.grid[x][y]:
                self.grid[x][y] = True
                self.visited.append((x, y))
            # if location already dirty, find another location to make dirty
            else:
                while((x, y) in self.visited):
                    x = random.randint(0, self.boundaries[0]-1)
                    y = random.randint(0, self.boundaries[1]-1)
                    self.grid[x][y] = True


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
        """
        move_left Moves the agent left.
        """
        self.location_x -= 1

    def move_right(self):
        """
        move_right Moves the agent right.
        """
        self.location_x += 1

    def move_down(self):
        """
        move_down Moves the agent down.
        """
        self.location_y -= 1

    def move_up(self):
        """
        move_up Moves the agent up.
        """
        self.location_y += 1

    def clean(self):
        """
        clean Cleans the spot at which the agent is currently located.
        """
        pos = self.environment.grid[self.location_x][self.location_y]
        if pos:
            pos = not pos


def main():
    env = Environment(10, 10)
    agent = Agent(random.randint(0, len(env.grid)),
                  random.randint(0, len(env.grid[0])), env)


if __name__ == '__main__':
    main()
