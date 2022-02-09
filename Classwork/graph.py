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
    def __init__(self, filename: str):
        """
        __init__ Initializes graph object.

        Args:
            filename (str): File of graph to import.
        """
        # graph = {origin:[(destination,weight)]}
        self.graph = dict()
        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        with open(filename) as f:
            val = f.readline()
            line1 = val.split()
            self.nodes = int(line1[0])
            self.edges = int(line1[1])

            for i in range(self.nodes):
                self.graph[i] = list()

            for i in range(self.edges):
                edge = f.readline().split()
                origin, destination, weight = int(
                    edge[0]), int(edge[1]), int(edge[2])
                self.graph[origin].append((destination, weight))

    def bfs(self, start: int):
        """
        bfs Does a Breath First Search of the Graph.

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
            for path in self.graph.get(i):
                if not seen[path[0]]:
                    queue.enqueue(path[0])
                    seen[path[0]] = True
            visited.append(i)
        print("Visited:", visited)

    def dfs(self, start: int):
        """
        dfs Does a Depth First Search of the Graph.

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
            for path in self.graph.get(i):
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
        for node in self.graph.items():
            output.append(str(node))

        return "\nGraph:\n\t(Start,[(Destination,Weight),...]\n\n\t" + "\n\t".join(output)

    def __len__(self) -> int:
        return len(self.graph.keys())


def main():
    graph = Graph('GraphExample.txt')
    graph.bfs(0)
    print(graph)


if __name__ == '__main__':
    main()
