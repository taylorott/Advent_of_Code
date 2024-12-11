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
    grid = bh.parse_char_grid(path,fname)

    l, w = len(grid), len(grid[0])

    pos_dict = dict()

    for i in range(l):
        for j in range(w):
            c = grid[i][j]
            if c!='.':
                if c not in pos_dict: pos_dict[c] = []
                pos_dict[c].append((i,j))

    return pos_dict, l, w

def compute_antinodes1(pos1,pos2,l,w,node_set):
    i1, j1, i2, j2 = pos1[0], pos1[1], pos2[0], pos2[1]

    di, dj = i2-i1, j2-j1

    node1 = (i1-di,j1-dj)
    if is_in_bounds(node1,l,w): node_set.add(node1)

    node2 = (i2+di,j2+dj)
    if is_in_bounds(node2,l,w): node_set.add(node2)

def compute_antinodes2(pos1,pos2,l,w,node_set):
    i1, j1, i2, j2 = pos1[0], pos1[1], pos2[0], pos2[1]

    di, dj = i2-i1, j2-j1

    di, dj=di//gcd(di,dj), dj//gcd(di,dj)
    
    i, j = i1, j1
    while is_in_bounds((i,j),l,w):
        node_set.add((i,j))
        i, j =i+di, j+dj

    i, j = i1, j1
    while is_in_bounds((i,j),l,w):
        node_set.add((i,j))
        i, j =i-di, j-dj

def is_in_bounds(pos,l,w): 
    return 0<=pos[0] and pos[0]<l and 0<=pos[1] and pos[1]<w

def solution(show_result=True, fname='Input02.txt'):
    pos_dict, l, w = parse_input01(fname)

    node_set1, node_set2 = set(), set()
    for key in pos_dict:
        coord_list = pos_dict[key]
        for i in range(len(coord_list)):
            for j in range(i+1,len(coord_list)):
                compute_antinodes1(coord_list[i],coord_list[j],l,w,node_set1)
                compute_antinodes2(coord_list[i],coord_list[j],l,w,node_set2)
       
    v1, v2 = len(node_set1), len(node_set2)
    if show_result:
        print(v1)
        print(v2)

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

