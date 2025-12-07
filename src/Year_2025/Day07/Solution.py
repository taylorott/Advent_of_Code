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

def update_line(grid,k):
    total = 0

    width = len(grid[0])
    for i in range(width):
        if grid[k][i]=='.':
            test0 = grid[k-1][i] == 'S' or grid[k-1][i] == '|' 
            test1 =  0<i and grid[k][i-1]=='^' and grid[k-1][i-1]=='|'
            test2 =  i<width-1 and grid[k][i+1]=='^' and grid[k-1][i+1]=='|'

            if test0 or test1 or test2:
                grid[k][i]='|'

        if grid[k][i]=='^' and (grid[k-1][i]=='|' or grid[k-1][i]=='S'):
            total+=1

    return total

def update_grid(grid):
    total = 0
    for i in range(1,len(grid)):
        total+=update_line(grid,i)
    return total

def update_timelines(grid,timelines,k):
    total = 0
    width = len(grid[0])

    for i in range(width):
        if grid[k][i]=='|' or grid[k][i]=='S':
            if grid[k+1][i]=='|':
                timelines[k][i]=timelines[k+1][i]
            if grid[k+1][i]=='^':
                if 0<i and grid[k+1][i-1]=='|':
                    timelines[k][i]+=timelines[k+1][i-1]
                if i<width-1 and grid[k+1][i+1]=='|':
                    timelines[k][i]+=timelines[k+1][i+1]
            total+=timelines[k][i]
    return total

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    val1 = update_grid(data)

    h, w = len(data), len(data[0])

    timelines = []
    for i in range(h):
        timelines.append([0]*w)

    for i in range(w):
        if data[-1][i] == '|':
            timelines[-1][i] = 1

    val2 = None
    for i in range(h-2,-1,-1):
        val2 = update_timelines(data,timelines,i)

    if show_result:
        print(val1)
        print(val2)

    return val1, val2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

