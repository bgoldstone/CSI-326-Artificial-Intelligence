import random


class Agent:
    """Class of type Agent

    Returns:
        [type]: Nones
    """    
    name: str
    __age: int
    __locationX: int
    __locationY: int

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

    def moveLocationRandom(self) -> None:
        """
        Changes Agent's X and Y location
        """
        self.__locationX = random.randint(0, 100)
        self.__locationY = random.randint(0, 100)

    def moveLocationSouth(self) -> None:
        """Moves Agent's location more south(in a negative direction on Y-Axis)
        """
        self.__locationX -= 10

    def moveLocationBasedOnAge(self) -> None:
        self.__locationX += self.__age
        self.__locationY += self.__age

    def __str__(self) -> str:
        """Returns String representation of Agent

        Returns:
            str: String representation of Agent
        """
        return f'Agent(name={self.name}, age={self.__age}, locationX={self.__locationX}, locationY={self.__locationY})'


def main():
    """Main Method for Agent Class.
    """
    agent = Agent("Ben", 20, 50, 50)
    print(agent)
    agent.setName("John")
    print(f'Agent name: {agent.getName()}')
    agent.moveLocationRandom()
    print(agent)
    agent.moveLocationSouth()
    print(agent)
    agent.moveLocationBasedOnAge()
    print(agent)


# Runs Main Method
if __name__ == "__main__":
    main()
