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

up, down, left, right = (-1,0), (1,0), (0,-1), (0,1)
traversal_dict = {up:[left,right],down:[left,right],left:[up,down],right:[up,down]}

def in_bounds(i,j,grid):
    return 0<=i and i<len(grid) and 0<=j and j<len(grid[0])

def parse_input01(fname):
    return bh.parse_char_grid(path,fname)

def dfs_region(i,j,c,grid, area_set, boundary_set):
    if (i,j) in area_set: return

    area_set.add((i,j))
    grid[i][j] = None

    for delta in traversal_dict:
        i_adj,j_adj = i+delta[0], j+delta[1]
        if in_bounds(i_adj,j_adj,grid) and grid[i_adj][j_adj]==c:
            dfs_region(i_adj,j_adj,c,grid,area_set, boundary_set)
        elif (i_adj,j_adj) not in area_set:
            boundary_set.add((i_adj,j_adj,delta))

def compute_boundary_score(boundary_set):
    total, visited_set = 0, set()

    for coord in boundary_set:
        if coord not in visited_set:
            total, bdry_normal=total+1, coord[2]

            for delta in traversal_dict[bdry_normal]:
                a = 1
                while (coord[0]+a*delta[0],coord[1]+a*delta[1],bdry_normal) in boundary_set:
                    visited_set.add((coord[0]+a*delta[0],coord[1]+a*delta[1],bdry_normal))
                    a+=1
    return total

def solution(show_result=True, fname='Input02.txt'):
    grid = parse_input01(fname)

    total1, total2 = 0, 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] is not None:
                area_set, boundary_set = set(), set()
                dfs_region(i,j, grid[i][j], grid,area_set, boundary_set)
                boundary_score = compute_boundary_score(boundary_set)
                total1+=len(area_set)*len(boundary_set)
                total2+=len(area_set)*boundary_score

    if show_result:
        print(total1)
        print(total2)

    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))