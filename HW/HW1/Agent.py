import random
"""Agent.py
    Name: Benjamin Goldstone
    Professor: Jorge Silveyra
    Version: 1/21/2022
    """


class Agent:
    """Class of type Agent

    Returns:
        [type]: Nones
    """

    def __init__(self, name: str, age: int, locationX: int, locationY: int) -> None:
        """Constructs Object of type Agent

        Args:
            name (str): name of Agent
            age (int): Age of Agent
            locationX (int): X-Axis location of Agent
            locationY (int): Y-Axis location of Agent
        """
        self.name = name
        self.__age = age
        self.__locationX = locationX
        self.__locationY = locationY

    def setName(self, name: str) -> None:
        """Sets name of Agent

        Args:
            name (str): Name of Agent
        """
        self.name = name

    def getName(self) -> str:
        """Gets Name of Agent

        Returns:
            str: Name of Agent
        """
        return self.name

    def getLocation(self) -> tuple:
        """Gets the X and Y location of Agent

        Returns:
            tuple: x and y location of Agent
        """
        return (self.__locationX, self.__locationY)

    def moveLocationRandom(self) -> None:
        """
        Changes Agent's X and Y location
        """
        self.__locationX = random.randint(-500, 500)
        self.__locationY = random.randint(-500, 500)

    def moveLocationSouth(self) -> None:
        """Moves Agent's location more south(in a negative direction on Y-Axis)
        """
        self.__locationY -= random.randint(0, 20)

    def moveLocationBasedOnAge(self) -> None:
        self.__locationX += self.__age * random.choice([-1, 1])
        self.__locationY += self.__age * random.choice([-1, 1])

    def __str__(self) -> str:
        """Returns String representation of Agent

        Returns:
            str: String representation of Agent
        """
        return f'Agent(name={self.name}, age={self.__age}, locationX={self.__locationX}, locationY={self.__locationY})'


def main():
    """Main Method for Agent Class.

    """
    NAME_CHANGE = ["John", "George"]
    DASHES = '-'*30
    agents = [
        Agent("Ben", random.randint(0, 90), 0, 100),
        Agent("Ben", random.randint(0, 90), 50, 50)
    ]
    for index, agent in enumerate(agents):
        print(f'{DASHES}START AGENT #{index+1}{DASHES}')
        print("Initial agent:", agent)
        agent.setName(NAME_CHANGE[index])
        print(f'Agent name: {agent.getName()}')
        for _ in range(2):
            agent.moveLocationRandom()
            print("Random Location:", agent.getLocation())
            agent.moveLocationSouth()
            print("Move South (y-axis):", agent.getLocation()[1])
            agent.moveLocationBasedOnAge()
            print("Location based on age:", agent.getLocation())
            agent.moveLocationRandom()
        print("Final agent:", agent)
        print(f'{DASHES}END AGENT #{index+1}{DASHES}\n')


# Runs main function on file run
if __name__ == "__main__":
    main()
