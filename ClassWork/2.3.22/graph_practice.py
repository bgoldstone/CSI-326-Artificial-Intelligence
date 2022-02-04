"""
graph_practice.py
A module that contains the class and functions of Graph, Stack, and Queue.
Author: Ben Goldstone
Date: 2/3/2022
Original Author: Jorge Silveyra
"""
import os
from typing import TypeVar
T = TypeVar('T')


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
        q = Queue()
        visited = list()
        q.enqueue(start)
        seen[start] = True
        while q.size() > 0:
            i = q.dequeue()
            for path in self.graph.get(i):
                if not seen[path[0]]:
                    q.enqueue(path[0])
                    seen[path[0]] = True
            visited.append(i)
        print("Visited:", visited)


class Queue:
    """
     Python Queue.
    """

    def __init__(self) -> None:
        """
        __init__ Initializes python queue.
        """
        self.queue = []

    def enqueue(self, object: T) -> None:
        """
        enqueue Insert item into queue.

        Args:
            object (T): Item to insert into queue.
        """
        self.queue.insert(0, object)

    def dequeue(self) -> T:
        """
        dequeue Removes item from queue.

        Returns:
            T: Item removed from queue.
        """
        return self.queue.pop()

    def size(self) -> int:
        return len(self.queue)


class Stack:
    """
     Python Stack
    """
    stack_object = list()
    max_size: int

    def __init__(self, max_size: int) -> None:
        """
        __init__ Initializes stack object.

        Args:
            max_size (int): [description]
        """
        self.max_size = max_size

    def push(self, object: T):
        """
        push Adds item to stack.

        Args:
            object (T): Item to add to stack.
        """
        if len(self.stack_object) >= self.max_size:
            print("List is full")
            return
        self.stack_object.push(object)

    def pop(self) -> T:
        """
        pop Removes item from stack.

        Returns:
            T: item removed from stack.
        """
        return self.stack_object.pop(0)

    def peek(self) -> T:
        """
        peek Returns Last item in Stack (next item to pop).

        Returns:
            T: Item
        """
        return self.stack_object[0]

    def isEmpty(self) -> bool:
        """
        isEmpty Returns true if stack is empty.

        Returns:
            bool: is stack empty.
        """
        return len(self.stack_object) == 0


def main():
    graph = Graph('GraphExample.txt')
    graph.bfs(0)


if __name__ == '__main__':
    main()
