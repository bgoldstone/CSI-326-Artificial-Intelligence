#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  3 14:36:54 2022

@author: jorgesilveyra
"""


def main():
    graph = dict()
    graphL = list()

    f = open("GraphValues.txt")
    val = f.readline()
    f.close()
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
    dfs(graph)


def dfs(graph):
    stack = list()
    start = 0
    visited = list()
    stack.append(start)
    visited.append(start)
