#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))
path = currentdir

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

up, down, left, right = (-1,0), (1,0), (0,-1), (0,1)
rotate_dict = {up:[left,right],down:[left,right],left:[up,down],right:[up,down]}

def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def parse_input01(fname):
    data = bh.parse_char_grid(path,fname)

    valid_set, start_tile, end_tile  = set(), None, None

    for i in range(len(data)):
        for j in range(len(data[0])):
            c = data[i][j]
            key = (i,j)
            if c!='#': valid_set.add(key)
            if c=='S': start_tile = key   
            if c=='E': end_tile = key   

    return valid_set, start_tile, end_tile

def build_graph(valid_set, end_tile):
    gridGraph = Digraph()

    for coord in valid_set:
        for dir1 in rotate_dict:
            key1, next_coord = (coord,dir1), coord_addition(coord,dir1)
            if next_coord in valid_set: gridGraph.add_edge(key1,(next_coord,dir1),1)

            for dir2 in rotate_dict[dir1]: gridGraph.add_edge(key1,(coord,dir2),1000)    

    for dir_end in rotate_dict:
        gridGraph.add_edge((end_tile,dir_end),end_tile,0)

    return gridGraph

def solution(show_result=True, fname='Input02.txt'):
    valid_set, start_tile, end_tile = parse_input01(fname)
    gridGraph = build_graph(valid_set, end_tile)

    start_key, sit_set = (start_tile,right), set()

    forward_dist_dict  = gridGraph.compute_dist_dijkstra(start_key)['dist_dict']
    reverse_dist_dict  = gridGraph.compute_dist_dijkstra(end_tile, reverse=True)['dist_dict']

    min_score = forward_dist_dict[end_tile]

    for mid_key in forward_dist_dict:
        if mid_key!=end_tile and forward_dist_dict[mid_key]+reverse_dist_dict[mid_key]==min_score: sit_set.add(mid_key[0])

    v1, v2 = min_score, len(sit_set)

    if show_result: print(str(v1)+'\n'+str(v2))

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

