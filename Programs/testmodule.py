#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 14:49:05 2022

@author: jorgesilveyra
"""
import module

print("I am the tester")
print(__name__)

matrix = [[1,2,3],[4,5,6]]
print(matrix)

mat = list()
for i in range(100):
    if i %2 == 0:
        mat.append(i)

print(mat)
mat2 = [[i] for i in range(100) if i%2 ==0]
print(mat2)
