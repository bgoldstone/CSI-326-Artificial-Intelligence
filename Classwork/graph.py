"""
graph_practice.py
A module that contains the class and functions of Graph, Stack, and Queue.
Author: Ben Goldstone
Date: 2/3/2022
Original Author: Jorge Silveyra
"""
import os
from data_structures import Queue, Stack

# import heapq


class Graph:
    def __init__(self, filename: str) -> None:
        """
        __init__ Initializes graph object.

        Args:
            filename (str): File of graph to import.
        """
        # graph = {origin:[(destination,weight)]}
        self.__graph = dict()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        with open(filename) as f:
            val = f.readline()
            line1 = val.split()
            self.nodes = int(line1[0])
            self.edges = int(line1[1])

            for i in range(self.nodes):
                self.__graph[i] = list()

            for i in range(self.edges):
                edge = f.readline().split()
                origin, destination, weight = int(
                    edge[0]), int(edge[1]), int(edge[2])
                self.__graph[origin].append((destination, weight))

    def add_connection(self, origin: int, destination: int, weight: int) -> None:
        """
        add_connection Adds connection to existing node.

        Args:
            origin (int): origin node or from node.
            destination (int): destination or to node.
            weight (int): weight or cost to path of nodes.
        """
        self.__graph[origin].append((destination, weight))

    def get_connections(self, origin: int) -> dict:
        """
        get_connections Gets connections for a given origin.

        Args:
            origin (int): start, or origin node.

        Returns:
            dict: sequence of nodes that  the origin node goes to.
        """
        return self.__graph[origin]

    def add_node(self, node_number: int) -> bool:
        """
        add_node Adds an additional node to the dictionary.

        Args:
            node_number (int): Number of node to add.

        Returns:
            bool: true if node is successfully added.
        """
        if self.__graph.get(node_number):
            return False
        self.__graph[node_number] = []
        return True

    def remove_node(self, node_number: int) -> bool:
        """
        remove_node Removes a node from the dictionary.

        Args:
            node_number (int): Number of node to remove.

        Returns:
            bool: true if node is successfully removed.
        """
        if self.__graph.get(node_number):
            self.__graph.pop(node_number)
            return True
        return False

    def breath_first_search(self, start: int) -> None:
        """
        breath_first_search Does a Breath First Search of the Graph.

        Args:
            start (int): Graph Node to start at.
        """
        seen = [False for _ in range(self.nodes)]
        queue = Queue()
        visited = list()
        queue.enqueue(start)
        seen[start] = True
        while len(queue) > 0:
            i = queue.dequeue()
            for path in self.__graph.get(i):
                if not seen[path[0]]:
                    queue.enqueue(path[0])
                    seen[path[0]] = True
            visited.append(i)
        print("Visited:", visited)

    def depth_first_search(self, start: int) -> None:
        """
        depth_first_search Does a Depth First Search of the Graph.

        Args:
            start (int): Graph Node to start at.
        """
        seen = [False for _ in range(self.nodes)]
        stack = Stack()
        visited = list()
        stack.push(start)
        seen[start] = True
        while len(stack) > 0:
            i = stack.pop()
            for path in self.__graph.get(i):
                if not seen[path[0]]:
                    stack.push(path[0])
                    seen[path[0]] = True
            visited.append(i)
        print("Visited:", visited)

    def __str__(self) -> str:
        """
        __str__ Returns string represention of graph.

        Returns:
            str: String representation of graph.
        """
        output = []
        for node in self.__graph.items():
            output.append(str(node))

        return "\nGraph:\n\t(Start,[(Destination,Weight),...]\n\n\t" + "\n\t".join(output)

    def __len__(self) -> int:
        return len(self.__graph.keys())


def main() -> None:
    graph = Graph('GraphExample.txt')
    graph.breath_first_search(0)
    print(graph)


if __name__ == '__main__':
    main()
