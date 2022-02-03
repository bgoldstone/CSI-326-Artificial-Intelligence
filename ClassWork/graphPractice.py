#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 14:36:54 2022

@author: jorgesilveyra
"""

from sys import maxsize


graph = dict()
graphL = list()

f = open("GraphValues.txt")
val = f.readline()
line1 = val.split()
nodes = int(line1[0])
edges = int(line1[1])

for i in range(nodes):
    graph[i] = list()
    graphL.append(list())

for i in range(edges):
    temp = f.readline().split()
    origin = int(temp[0])
    destination = int(temp[1])
    weight = int(temp[2])
    graph[origin].append((destination, weight))
    graphL[origin].append((destination, weight))


def DFS():
    pass


class Stack:
    stack_object = list()
    max_size: int

    def __init__(self, maxSize: int) -> None:
        self.max_size = maxSize

    def push(self,object):
        if len(self.stack_object) >= self.max_size:
            print("List is full")
            return
        self.stack_object.push(object)

    def pop(self,object):
        self.stack_object.pop(0)

    def peek(self,):
        return self.stack_object[0]
