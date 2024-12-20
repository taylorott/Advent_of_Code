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

direction_list = [(-1,0), (1,0), (0,-1), (0,1)]

def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def parse_input01(fname):
    data = bh.parse_char_grid(path,fname)

    valid_set, start_tile, end_tile  = set(), None, None

    for i in range(len(data)):
        for j in range(len(data[0])):
            c = data[i][j]
            coord = (i,j)
            if c!='#': valid_set.add(coord)
            if c=='S': start_tile = coord   
            if c=='E': end_tile = coord   
    return valid_set, start_tile, end_tile

def build_graph(valid_set):
    gridGraph = Graph()

    for coord in valid_set:
        for direction in direction_list:
            next_coord = coord_addition(coord,direction)

            if next_coord in valid_set: 
                gridGraph.add_edge(coord,next_coord)
    return gridGraph

def compute_num_cheats(valid_set, forward_dist_dict, reverse_dist_dict, regular_dist, cheat_time, time_saved):
    count = 0

    for coord in valid_set:
        for i in range(-cheat_time,cheat_time+1):
            for j in range(-(cheat_time-abs(i)),(cheat_time-abs(i))+1):
                next_coord = coord_addition(coord,(i,j))
                if next_coord in valid_set:
                    d1, d2 =  forward_dist_dict[coord], reverse_dist_dict[next_coord]
                    if d1+d2+abs(i)+abs(j)+time_saved<=regular_dist and abs(i)+abs(j)<=cheat_time: count+=1
    return count

def solution(show_result=True, fname='Input02.txt'):
    valid_set, start_tile, end_tile = parse_input01(fname)

    gridGraph = build_graph(valid_set)

    forward_dist_dict  = gridGraph.compute_dist_BFS(start_tile)['dist_dict']
    reverse_dist_dict  = gridGraph.compute_dist_BFS(end_tile)['dist_dict']

    regular_dist = forward_dist_dict[end_tile]

    time_saved = 100

    v1 = compute_num_cheats(valid_set, forward_dist_dict, reverse_dist_dict, regular_dist, 2, time_saved)
    v2 = compute_num_cheats(valid_set, forward_dist_dict, reverse_dist_dict, regular_dist, 20, time_saved)

    if show_result: print(str(v1)+'\n'+str(v2))

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

