#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = bh.parse_char_grid(path,fname)

    return data

delta_list = [-1,0,1]

def is_valid_index(grid,i,j):
    return 0<=i and i<len(grid) and 0<=j and j<len(grid[0])

def is_acessible(grid,i,j):
    if (not is_valid_index(grid,i,j)) or grid[i][j]!='@':
        return False

    count = 0
    for di in delta_list:
        for dj in delta_list:
            i2, j2 = i+di, j+dj

            if is_valid_index(grid,i2,j2) and grid[i2][j2]=='@': 
                count+=1

    return count<=4

def remove_roll_recursive(grid,i,j):
    num_removed = 0
    if is_acessible(grid,i,j):
        grid[i][j] = '.'
        num_removed +=1

        for di in delta_list:
            for dj in delta_list:
                i2, j2 = i+di, j+dj
                
                num_removed+=remove_roll_recursive(grid,i2,j2)

    return num_removed

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0

    for i in range(len(data)):
        for j in range(len(data[0])):
            if is_acessible(data,i,j):
                total+=1

    if show_result:
        print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    
    total = 0

    for i in range(len(data)):
        for j in range(len(data[0])):
            total+=remove_roll_recursive(data,i,j)
            
    if show_result:
        print(total)

    return total   

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

