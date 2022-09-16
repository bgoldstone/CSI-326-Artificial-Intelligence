# -*- coding: utf-8 -*-
"""
AI Homework 4
Authors: Kaleb Gearinger and Benjamin Goldstone
Description:
    The Agent class is a a class of a common roomba. This class is able
    to move up, down, left, or right and able to keep track of its movements
    using its move history. It always knows its location at all times in the
    environment.
"""

class Agent:

    def __init__(self, location_x: int, location_y: int, environment):
        """
        __init__ Constructs object of an Agent.

        Args:
            location_x (int): x location of Agent.
            location_y (int): y location of Agent.
            environment (Environment): takes in an environment.
        """
        self.location_x = location_x
        self.location_y = location_y
        self.environment = environment
        self.movehistory = []
    
    # Movement Functions take in boolean to tell if it has already been reversed
    # All moves append to move history to be used to backtrack
    def move_left(self, isReversible):
        self.location_x -= 1
        self.movehistory.append([-1,0,isReversible])
        
    def move_right(self, isReversible):
        self.location_x += 1
        self.movehistory.append([1,0,isReversible])
        
    def move_down(self, isReversible):
        self.location_y += 1
        self.movehistory.append([0,1,isReversible])
        
    def move_up(self, isReversible):
        self.location_y -= 1
        self.movehistory.append([0,-1,isReversible])