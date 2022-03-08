#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 25 12:52:53 2022

@author: jorgesilveyra
"""

print(__name__)
def fun1(a):
    x = a + a
    print(x)
if __name__ == '__main__':
    import sys
    
    #fun1(int(sys.argv[2]))
    print(sys.argv[0])
    print(__name__)
