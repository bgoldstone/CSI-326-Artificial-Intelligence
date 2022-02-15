"""
HW3.py
A module that contains the class and functions of Graph.
Author: Ben Goldstone
Date: 2/15/2022
Original Author: Jorge Silveyra
"""
import time
from typing import Union
import os
from data_structures import Queue, Stack

# heapq


class Graph:
    def __init__(self, filename: str) -> None:
        """
        __init__ Initializes graph object.

        Args:
            filename (str): File of graph to import.
        """
        # graph formatting: {origin:[(destination,weight)]}
        self.__graph = dict()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        file = open(filename)
        for index, line in enumerate(file):
            if(index == 0):
                line1 = line.split()
                self.vertices = int(line1[0])
                for i in range(self.vertices):
                    self.__graph[i] = list()
            else:
                edge = line.split()
                weight = 0
                if len(edge) == 3:
                    weight = int(edge[2])
                self.__graph[int(edge[0])].append((int(edge[1]), weight))
        file.close()

    """
    Helper methods:
        add_connections()
        remove_connections()
        get_connections()
        add_node()
        remove_node()
        node_exists()
    """

    def add_connections(self, origin: int, destination: int, weight: int) -> None:
        """
        add_connections Adds connection to existing node.

        Args:
            origin (int): origin node or from node.
            destination (int): destination or to node.
            weight (int): weight or cost to path of nodes.
        """
        if destination > len(self.__graph) - 1:
            print("Invalid destination! Node will not be added!")
            return

        if not self.node_exists(origin):
            self.add_node(origin)
        self.__graph[origin].append((destination, weight))

    def remove_connections(self, origin: int, destination: int, weight: int) -> bool:
        """
        remove_connections Removes connections from existing nodes.

        Args:
            origin (int): original or start node.
            destination (int): destination or end node.
            weight (int): weight or distance of node.

        Returns:
            bool: True if successfully removed.
        """
        pair = (destination, weight)
        if self.node_exists(origin) and pair in self.__graph.get(origin):
            self.__graph.get(origin).pop(pair)

    def get_connections(self, origin=-1) -> list:
        """
        get_connections Gets connections for a given origin.

        Args:
            origin (int): start, or origin node.

        Returns:
             list: if origin is specified: 
                                    None if the origin does not exist, else returns list of destinations and weights of origin. 
                                else: All connections will be returned.
        """

        if origin == -1:
            return_list = []
            for node_number in range(len(self.__graph)):
                verticy = self.__graph[node_number]
                for edge in verticy:
                    destination, weight = edge
                    return_list.append((node_number, destination, weight))
        else:
            return_list = []
            for edge in self.__graph.get(origin, None):
                destination, weight = edge
                return_list.append(
                    f'Origin: {origin}, Destination: {destination}, Weight: {weight}')

        return return_list

    def add_node(self, node_number: int) -> bool:
        """
        add_node Adds an additional node to the dictionary.

        Args:
            node_number (int): Number of node to add.

        Returns:
            bool: true if node is successfully added.
        """
        if self.node_exists(node_number):
            return False
        self.__graph[node_number] = list()
        return True

    def remove_node(self, node_number: int) -> bool:
        """
        remove_node Removes a node from the dictionary.

        Args:
            node_number (int): Number of node to remove.

        Returns:
            bool: true if node is successfully removed.
        """
        if self.node_exists(node_number):
            self.__graph.pop(node_number)
            return True
        return False

    def node_exists(self, node_number: int) -> bool:
        """
        node_exists Checks if node exists.

        Args:
            node_number (int): node number.

        Returns:
            bool: True if node exists.
        """
        return True if self.__graph.get(node_number) else False

    """
    Search Algorithms:
        breath_first_search()
        depth_first_Search()
    """

    def breath_first_search(self, start: int) -> None:
        """
        breath_first_search Does a Breath First Search of the Graph.

        Args:
            start (int): Graph Node to start at.
        """
        seen = [False for _ in range(self.vertices)]
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
        seen = [False for _ in range(self.vertices)]
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
        output = list()
        for node in self.__graph.items():
            output.append(str(node))

        return "\nGraph:\n\t(Start,[(Destination,Weight),...]\n\n\t" + "\n\t".join(output)

    def __len__(self) -> int:
        """
        __len__ Length of Graph

        Returns:
            int: number of nodes
        """
        return len(self.__graph.keys())


def main() -> None:
    graph = Graph('GraphExample.txt')
    choice = 0
    prompt = """
Input a choice:
    1. Vertices connected to
    2. Print Graph
    3. Add Connection
    4. Store to File
    5. Exit
    6. Print BFS
    7. Print DFS
    
    input: """
    while(choice != 5):
        choice = int(input(prompt))
        print()
        if choice == 1:
            vertices_connected_to(graph)
        elif choice == 2:
            print(graph)
        elif choice == 3:
            add_connection(graph)
        elif choice == 4:
            store_to_file(graph)
        elif choice == 5:
            print("Goodbye!")
        elif choice == 6:
            bfs(graph)
        elif choice == 7:
            dfs(graph)

        else:
            print("Invalid input!")
        time.sleep(1)


def vertices_connected_to(graph: Graph):
    origin = int(input("Please enter a verticy to get: "))
    print("\n".join(graph.get_connections(origin)))

def bfs(graph: Graph):
    start_node = int(input("Enter a start node for BFS: "))
    graph.breath_first_search(start_node)

def dfs(graph: Graph):
    start_node = int(input("Enter a start node for DFS: "))
    graph.depth_first_search(start_node)

def add_connection(graph: Graph):
    origin = int(input("Please enter an origin node: "))
    destination = int(input("Please enter a destination node: "))
    weight = int(input("Please enter the weight of the connection: ") or 0)
    graph.add_connections(origin, destination, weight)


def store_to_file(graph: Graph):
    filename = str(input("Enter a filename to save to: "))
    connections = graph.get_connections()
    output = open(filename, "w")
    output.write(f'{graph.vertices}\n')
    for connection in connections:
        output.write(f'{connection[0]} {connection[1]} {connection[2]}\n')
    output.close()


if __name__ == '__main__':
    main()
