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
    data = bh.parse_digit_grid(path,fname)
    return data

adj_list = [(-1,0),(1,0),(0,-1),(0,1)]

def in_bounds(i,j,grid):
    return 0<=i and i<len(grid) and 0<=j and j<len(grid[0])

def compute_score(vertex1,grid,num_path_dict):
    if vertex1 in num_path_dict: 
        return 0, num_path_dict[vertex1]

    i1,j1, total1, total2 = vertex1[0], vertex1[1], 0, 0

    if grid[i1][j1]==9: 
        num_path_dict[vertex1]=1
        return 1, num_path_dict[vertex1]

    for delta in adj_list:
        i2, j2 = i1+delta[0], j1+delta[1]
        vertex2 = (i2,j2)

        if in_bounds(i2,j2,grid) and grid[i2][j2]-grid[i1][j1]==1: 
            temp1, temp2 = compute_score(vertex2,grid,num_path_dict)
            total1, total2 = total1+temp1, total2+temp2

    num_path_dict[vertex1] = total2
    return total1, total2

def solution():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    grid = parse_input01(fname)

    total1, total2 = 0, 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==0: 
                temp1,temp2 =compute_score((i,j),grid,dict())
                total1, total2 = total1+temp1, total2+temp2
    print(total1)
    print(total2)



if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

