# -*- coding: utf-8 -*-
"""
AI Homework 4
Authors: Kaleb Gearinger and Benjamin Goldstone
Description:
    Various functions that are used in the algorithms file. They do various things
    such as check the status of a square to see if its visited, move the agent, 
    reverse a preious move, and see if something is in moveable range. 
"""

"""
- makeMove -
Takes in the agent and two cordinates and compares them against one another.
It then makes a move accordingly based on the result. To reach this new position.
If the agent is already at the new position has it take no move and just simply
pass through to finish the function. If its not a legal move prints no move to
tell user that something went wrong before calling it that made it try to accomplish
an illegal move.
"""

def makeMove(agent, new_pos_x, new_pos_y):
    # Checks if it needs to move either x or y then moves accordingly
    # All set to True as they are reversible
    if agent.location_x - new_pos_x == 1:
        agent.move_left(True)
    elif agent.location_x - new_pos_x == -1:
        agent.move_right(True)
    elif agent.location_y - new_pos_y == 1:
        agent.move_up(True)
    elif agent.location_y - new_pos_y == -1:
        agent.move_down(True)
    elif agent.location_x - new_pos_x == 0 and agent.location_y - new_pos_y == 0:
        pass
    else:
        print("no move")

"""
- reverseMove -
Takes in the previous move and the agent, and has the agent do a move that will
reverse the previous move. 
"""     
def reverseMove(agent,  prev_move):
    # Grabs the previous move from prev_move
    x = prev_move[0]
    y = prev_move[1]
    # Makes a new move to reverse the move
    # All set to False as they are not reversible
    if x == -1:
        agent.move_right(False)
    elif x == 1:
        agent.move_left(False)
    elif y == -1:
        agent.move_down(False)
    elif y == 1:
        agent.move_up(False)
    
"""
- inMoveable -
Takes in the two cordinates and checks if they can be reached in a legal move.
If not returns false. A legal move in our case qualifies as either +1 or -1
in x only or +1 or -1 in y only. It can not be simulteneous as our agent
does not allow for diagonal movements. There is also one case where it will
let it pass if the object is at the same position.
"""
def inMoveable(x,y,new_x, new_y):
    if x == new_x:
        if y == new_y + 1 or y == new_y - 1:
            return True
        elif y == new_y:
            return True
        else:
            return False
    elif x == new_x + 1 or x == new_x - 1:
        if y == new_y:
            return True
        else:
            return False
    else:
        return False
    
"""
- notVisited -
Takes in a node and an agent and checks to see if the position has been visited.
Returns True if it hasn't, returns False if it has
"""
def notVisited(node, agent):
    tempFlag = True
    # Checks the node position and sees if there is a two there
    if agent.environment.grid[node[0]][node[1]][0] == 2:
        tempFlag = False
    return tempFlag