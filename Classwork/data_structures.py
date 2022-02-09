"""
    Date: 2/8/2022
    Data Structures Implementations
"""
from typing import TypeVar

T = TypeVar('T')


class Queue:
    """
    Queue Implementation of a Queue.
    """

    def __init__(self) -> None:
        """
        __init__ Initializes python queue.
        """
        self.__queue = []

    def enqueue(self, object: T) -> None:
        """
        enqueue Insert item into queue.

        Args:
            object (T): Item to insert into queue.
        """
        self.__queue.insert(0, object)

    def dequeue(self) -> T:
        """
        dequeue Removes item from queue.

        Returns:
            T: Item removed from queue.
        """
        return self.__queue.pop()

    def __len__(self) -> int:
        """
        __len__ Length of queue using len() function.

        Returns:
            int: Length of queue.
        """
        return len(self.__queue)


class Stack:
    """
    Stack Implementation of a Stack
    """
    max_size: int

    def __init__(self, max_size: int) -> None:
        """
        __init__ Initializes stack object.

        Args:
            max_size (int): [description]
        """
        self.max_size = max_size
        self.__stack = []

    def push(self, object: T):
        """
        push Adds item to stack.

        Args:
            object (T): Item to add to stack.
        """
        if len(self.__stack) >= self.max_size:
            print("List is full")
            return
        self.__stack.push(object)

    def pop(self) -> T:
        """
        pop Removes item from stack.

        Returns:
            T: item removed from stack.
        """
        return self.__stack.pop(0)

    def peek(self) -> T:
        """
        peek Returns Last item in Stack (next item to pop).

        Returns:
            T: Item
        """
        return self.__stack[0]

    def isEmpty(self) -> bool:
        """
        isEmpty Returns true if stack is empty.

        Returns:
            bool: is stack empty.
        """
        return len(self.__stack) == 0

    def __len__(self):
        """
        __len__ returns length of stack.
        Returns: length of the stack.
        """
        return len(self.__stack)
