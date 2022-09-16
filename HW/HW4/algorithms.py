# -*- coding: utf-8 -*-
"""
Path Searching Algorithms
Included Below:
    - BFS
    - DFS with step by step with agent
    - Greedy Best-First Search
    - A* Search
All take input of an Agent Class which includes
an environment with 7 randomly generated walls.
It then returns whether or not an exit was found
and how many iterations of the loop it took to find
the exit.
"""

# Imports all external functions used
from functions import makeMove, reverseMove, inMoveable, notVisited
# Adds heap functions to be used with A* and Greedy Best-First Searches
import heapq

"""
- BFS Search Algorithm -
Takes in input of end goal and where the agent starts. Then uses implementation
of BFS to find the goal while counting how many iterations the loop is run.
"""

def BFS(endX: int, endY: int, agent):
    # Grabs the boundaries to know how many nodes there are
    x_boundaries = agent.environment.boundaries[0]
    y_boundaries = agent.environment.boundaries[1]
    # Creates a list that will be used as a queue
    queue = []
    # Grabs the starting position of the agent
    startX = agent.location_x
    startY = agent.location_y
    # Appends to the queue
    queue.append((startX,startY))
    # Flag used to see if exit is found (When Found = False)
    flag = True
    # Sets counter to count iterations of the loop
    iterations = 0
    # Runs through elements in queue until either exit is found or stack is empty
    while (not len(queue) == 0) and flag:
        # Pops the front of the list or the first element in the queue
        currentNode = queue.pop(0)
        # Checks to see if the node popped was already visited through function call
        if notVisited(currentNode, agent):
            # Grabs the current positions
            current_x = currentNode[0]
            current_y = currentNode[1]
            # Sets position to visited status in environment
            agent.environment.visit(current_x, current_y)
            # Checks all connections using adjacency matrix from node 0-99
            for index in range(x_boundaries*y_boundaries):
                # Checks if there is a connection present.
                # If value > 0 there is a connection, if value = 0 there is no connection
                if agent.environment.matrix[current_x+(current_y*x_boundaries)][index] > 0:
                    # Converts node back into cordinates using division and modulous
                    new_x = int(index % x_boundaries)
                    new_y = int(index / x_boundaries)
                    # Checks if the position of the node is the end point 
                    if new_x == endX and new_y == endY:
                        # If so sets flag to false to signify end point reached
                        flag = False
                        break
                    # Checks to see if the connection has not already been visited
                    if notVisited((new_x,new_y),agent):
                        # If it hasn't adds point to queue
                        queue.append((new_x,new_y))
        # Increments the iteration counter
        iterations += 1
    # If it finds the exit simply returns iterations             
    if not flag:
        return(iterations)
    # Otherwise returns -1
    else:
        return(-1)

"""
- DFS Search Algorithm -
Takes in input of end goal and where the agent starts. Then uses implementation
of DFS to find the goal while counting how many iterations the loop is run. However,
this algorigthm also has the agent move and backtrack.
"""

def DFS(endX: int, endY: int, agent):
    # Sets boundaries of environment to variables for easier later use
    x_boundaries = agent.environment.boundaries[0]
    y_boundaries = agent.environment.boundaries[1]
    # Creates a list that will act as a stack
    stack = []
    # Sets the starting locations
    startX = agent.location_x
    startY = agent.location_y
    # Adds the starting locations to stack and sets flag for finish to true
    stack.append((startX,startY))
    flag = True
    # Sets counter to count iterations of the loop
    iterations = 0
    # Checks to see that flag status has not changed and that the stack is not empty
    while (not len(stack) == 0) and flag:
        # Pops the top of the stack
        currentNode = stack.pop()
        # Grabs location x and y
        current_x = currentNode[0]
        current_y = currentNode[1]
        # Calls function to see if agent is able to move to the location from
        # where it currently is
        while not inMoveable(current_x,current_y, agent.location_x, agent.location_y):
            # If it is unable to backtrack until agent is able to
            moveIndex = -1
            # Runs until list is empty
            for _ in agent.movehistory:
                # Checks to see if position from back of move history is able to be reversed
                if agent.movehistory[moveIndex][2]:
                    # If so reverses the move and turns it into non-reversible
                    agent.movehistory[moveIndex][2] = False
                    reverseMove(agent, agent.movehistory[moveIndex])
                    break
                # Increments through list backwards
                moveIndex -= 1
        # Moves agent to connection popped
        makeMove(agent, current_x, current_y)
        # Checks to see if the position has not already been visited
        if notVisited(currentNode, agent):
            # Sets new node to visited
            agent.environment.visit(current_x, current_y)
            # Checks all connections to current node
            for index in range(x_boundaries*y_boundaries):
                # If > 0 then there is a connection, if = 0 then there is not
                if agent.environment.matrix[current_x+(current_y*x_boundaries)][index] > 0:
                    # Converts node to cordinates using modulous and division
                    new_x = int(index % x_boundaries)
                    new_y = int(index / x_boundaries)
                    # Checks to see if new position is end goal
                    if new_x == endX and new_y == endY:
                        # If so then then sets flag to appropriate values to escape the loop
                        flag = False
                        makeMove(agent,new_x,new_y)
                        # Does not care about the rest of the connections so it breaks for loop
                        break
                    # Checks to see if node has already been vistited
                    if notVisited((new_x,new_y),agent):
                        # If it hasn't adds node to stack
                        stack.append((new_x,new_y))
        # Increments iterations counter
        iterations += 1
        
    # If it finds the exit simply returns iterations             
    if not flag:
        return(iterations)
    # Otherwise returns -1
    else:
        return(-1)

"""
- Greedy Best-First Search Algorithm -
Takes in input of end goal and where the agent starts. Then uses implementation
of Greedy Best-First Search to find the goal while counting how many 
iterations the loop is run. This algorithm takes advantage of the
heuristic from the grid.
"""    

def GreedyBest_FirstSearch(endX: int, endY: int, agent):
    # Sets boundaries of environment to variables for easier later use
    x_boundaries = agent.environment.boundaries[0]
    y_boundaries = agent.environment.boundaries[1]
    # Creates a list called heap that will use heapq to act as a heap
    heap = []
    # Grabs the starting position
    startX = agent.location_x
    startY = agent.location_y
    # Pushes the value onto the heap
    heapq.heappush(heap, (agent.environment.grid[startX][startY][1],startX,startY))
    # Flag to check when it finishes
    flag = True
    # Sets counter to count iterations of the loop
    iterations = 0
    # Checks to see whether the heap is empty or the it found the exit
    while (not len(heap) == 0) and flag:
        # Pops the value with the lowest heuristic from the heap
        currentNode = heapq.heappop(heap)
        # Grabs its position
        current_x = currentNode[1]
        current_y = currentNode[2]
        # Checks if the node hasn't been visited
        if notVisited((current_x, current_y), agent):
            # Changes the locations status to visited
            agent.environment.visit(current_x, current_y)
            # Checks all connections and if value > 0 there is a connection
            for index in range(x_boundaries*y_boundaries):
                if agent.environment.matrix[current_x+(current_y*x_boundaries)][index] > 0:
                    # Converts Node to Cordinates
                    new_x = int(index % x_boundaries)
                    new_y = int(index / x_boundaries)
                    # Checks if it reached the end points
                    if new_x == endX and new_y == endY:
                        flag = False
                        break
                    # If the position hasn't already been visited adds it to the heap
                    if notVisited((new_x,new_y),agent):
                        heapq.heappush(heap, (agent.environment.grid[new_x][new_y][1],new_x,new_y))
        # Increments the iterations counter to signify one iteration has passed
        iterations += 1

    # If it finds the exit simply returns iterations             
    if not flag:
        return(iterations)
    # Otherwise returns -1
    else:
        return(-1)
    
"""
- A* Searching -
This algorithm uses heuristics and actual cost to find the shortest path. It is input
the position of the goal and the agent.

"""
def A_Star(endX: int, endY: int, agent):
    # Boundaries of the environment for later use
    x_boundaries = agent.environment.boundaries[0]
    y_boundaries = agent.environment.boundaries[1]
    # Creates a list called heap
    heap = []
    # Grabs the starting position
    startX = agent.location_x
    startY = agent.location_y
    # Uses heapq to heap push the data into the heap like structure
    heapq.heappush(heap, (agent.environment.grid[startX][startY][1],startX,startY,0))
    # Keeps a flag to tell if the goal is found
    flag = True
    # For counting iterations
    iterations = 0
    # Runs until goal is found or no more elements in heap
    while (not len(heap) == 0) and flag:
        # Grabs the node in the heap
        currentNode = heapq.heappop(heap)
        # Grabs the current position from the node
        current_x = currentNode[1]
        current_y = currentNode[2]
        # Checks to see if the node was already visited if so doesn't need to check again as it already
        # found the shortest path to that point based on the algorithm
        if notVisited((current_x,current_y), agent):
            # Checks if popped is the final position as it will be the shortest path when popped
            if current_x == endX and current_y == endY:
                flag = False
            # If not continues looping normally
            else:
                # If the path was already the shortest adds it to visited
                agent.environment.visit(current_x,current_y)
                # Checks for all positions
                for index in range(x_boundaries*y_boundaries):
                    # Makes a copy of the weight currently used to get there
                    totalWeightOfPath = currentNode[3]
                    # Checks if there is a connections (0 = no connection : 0 > connection)
                    if agent.environment.matrix[current_x+(current_y*x_boundaries)][index] > 0:
                        # Grabs weight of connection, new_x, new_y and heuristic
                        weight = agent.environment.matrix[current_x+(current_y*x_boundaries)][index]
                        new_x = int(index % x_boundaries)
                        new_y = int(index / x_boundaries)
                        heuristic = agent.environment.grid[new_x][new_y][1]
                        # Adds to find total path to get to new connection
                        newTotalWeightOfPath = totalWeightOfPath + weight
                        # Calculates A* value
                        a_star_value = float(heuristic + newTotalWeightOfPath)
                        # Checks if heap is empty
                        if len(heap) == 0:
                            # If it is just simply pushes value onto heap
                            heapq.heappush(heap, (a_star_value,new_x,new_y,newTotalWeightOfPath))
                        # If not has to run some checks
                        else:
                            # Arbitrary counter
                            i = 0
                            # Checks to see if object is in heap already
                            while i < len(heap):
                                inheap = heap.pop(i)
                                notInHeap = True
                                # Checks to see if there is already a shorter path in the heap
                                if (new_x == inheap[1] and new_y == inheap[2]):
                                    if  a_star_value < inheap[0]:
                                        # If the path found is shorter adds it to the heap and breaks the loop
                                        heapq.heappush(heap, (a_star_value,new_x,new_y,newTotalWeightOfPath))
                                        notInHeap = False
                                        break
                                    else:
                                        # If the path is not shorter just puts the object back
                                        heapq.heappush(heap, inheap)
                                # If the cordinates don't match just puts it back
                                else:
                                    heapq.heappush(heap, inheap)
                                # Increments the counter
                                i += 1
                            # If the object is not in the heap at all just simply adds it
                            if notInHeap:
                                heapq.heappush(heap, (a_star_value,new_x,new_y,newTotalWeightOfPath))
        
        # Counts the iterations it has to run to complete the search                
        iterations += 1
    
    # If it finds the exit simply returns iterations             
    if not flag:
        return(iterations)
    # Otherwise returns -1
    else:
        return(-1)