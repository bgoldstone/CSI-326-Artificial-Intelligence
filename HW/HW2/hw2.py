import random


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
        # Sets all indexes to Dirty
        for x in range(self.boundaries[0]):
            self.grid.append(list())
            for y in range(self.boundaries[1]):
                self.grid[x].append(0)
        # Generates Dirty locations Dirty = True, Clean = False
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
        self.og = self.grid[:]

    def setOG(self):
        self.grid = self.og

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

    def clean(self):
        print(self.location_x, self.location_y)
        pos = self.environment.grid[self.location_x][self.location_y]
        if pos:
            pos = not pos
            return 1

        if not pos:
            return 0

    def move(self):
        pos = self.environment.grid[self.location_x][self.location_y]
        randVal = random.randint(1, 4)

        if randVal == 1:
            if self.location_x - 1 >= 0:
                self.move_left()
            else:
                self.move()
        if randVal == 2:
            if self.location_x + 1 <= 9:
                self.move_right()
            else:
                self.move()
        if randVal == 3:
            if (self.location_y - 1 >= 0):
                self.move_up()
            else:
                self.move()
        if randVal == 4:
            if (self.location_y + 1 <= 9):
                self.move_down()
            else:
                self.move()
        print(self.location_x, self.location_y)

    def teleport(self):
        randValX = random.randint(0, 9)
        randValY = random.randint(0, 9)

        self.location_x = randValX
        self.location_y = randValY


def main():

    results = []

    #env = Environment(10, 10)
    for i in range(100):
        cleanCounter = 0

        # create new environment every iteration
        env = Environment(10, 10)

        # create same environment every iteration
        # env.setOG()

        # initialize agent to same location every iteration
        agent = Agent(0, 0, env)

        # initialize agent to new location every iteration
        # agent = Agent(random.randint(0, 9),
        #           random.randint(0, 9), env)

        cleanCounter += agent.clean()

        for j in range(75):
            # move method for experiment 1 to move up and down
            agent.move()
            # move method for experiment 2 to move randomly
            # agent.teleport()
            cleanCounter += agent.clean()
        print(cleanCounter)
        results.append(cleanCounter)

    average = 0

    for x in results:
        average += x
    average = average/len(results)

    print(average)


if __name__ == '__main__':
    main()
