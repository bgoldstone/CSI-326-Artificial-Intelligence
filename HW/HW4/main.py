# -*- coding: utf-8 -*-
"""
AI Homework 4
Authors: Kaleb Gearinger and Benjamin Goldstone
Description:
    Tests the different algorithms and sees which ones find the exit and
    how many iterations it takes on average to complete the search. Every
    iteration has the same heuristics and weights assigned however, the positions
    of the walls are different from iteration to iteration.
"""

# Import all our defined algorithms
from algorithms import DFS, BFS, GreedyBest_FirstSearch, A_Star
# Imports to allow use of deepcopy function
import copy
# Imports the Environment and Agent classes
from Environment import Environment as e
from Agent import Agent as a

def main():

    # Creates an environment with no walls of size 10x10
    env = e(10, 10)
    
    # Creates the blank lists for the results to be stored
    bfs = []
    dfs = []
    gbfs = []
    astar = []
    
    # Loops 100 times
    for _ in range(100):
        
        # Creates a copy of the initial enironment with same weights and heuristics
        testEnv = copy.deepcopy(env)
        # Adds walls to the environment
        testEnv.create_wall()
        # Inputs that into the agent with an intial position of (0,0)
        testAgent = a(0, 0, testEnv)
        # Copies the Agent 3 times to create 4 
        testAgent2 = copy.deepcopy(testAgent)
        testAgent3 = copy.deepcopy(testAgent)
        testAgent4 = copy.deepcopy(testAgent)
        
        # Add below code if you want to print out the trial number and the environment of every trial
        """
        txt = ("Trial: {trialnum: d}")
        print(txt.format(trialnum = i))
        testEnv.print_without_heurisics()
        print()
        """
        
        # Asks all algorithms to find the exit at 9,9 (returns -1 if exit not found)
        bfsvalue = BFS(9,9,testAgent)
        dfsvalue = DFS(9,9,testAgent2)
        gbfsvalue = GreedyBest_FirstSearch(9,9,testAgent3)
        astarvalue = A_Star(9,9,testAgent4)
        
        # Appends them to a total data list only if its not -1
        if bfsvalue != -1:
            bfs.append(bfsvalue)
        if dfsvalue != -1:
            dfs.append(dfsvalue)
        if gbfsvalue != -1:
            gbfs.append(gbfsvalue)
        if astarvalue != -1:
            astar.append(astarvalue)
    
    # Formats the output to print how many times it succeeded
    #  and the average number of steps
    print()
    print("-BFS---------------------------------")
    print("BFS found the exit: ", end = '')
    print(len(bfs), end = '')
    print("/100 times")
    print("BFS had an average score: ", end = '')
    print(sum(bfs)/len(bfs))
    
    print()
    print("-DFS---------------------------------")
    print("DFS found the exit: ", end = '')
    print(len(dfs), end = '')
    print("/100 times")
    print("DFS had an average score: ", end = '')
    print(sum(dfs)/len(dfs))
    
    print()
    print("-Greedy Best-First Search------------")
    print("Greedy Best-First Search found the exit: ", end = '')
    print(len(gbfs), end = '')
    print("/100 times")
    print("Greedy Best-First Search had an average score: ", end = '')
    print(sum(gbfs)/len(gbfs))
    
    print()
    print("-A*----------------------------------")
    print("A* found the exit: ", end = '')
    print(len(astar), end = '')
    print("/100 times")
    print("A* had an average score: ", end = '')
    print(sum(astar)/len(astar))


if __name__ == '__main__':
    main()