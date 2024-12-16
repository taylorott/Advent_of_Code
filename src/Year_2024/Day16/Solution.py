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

up,down ,left, right = (-1,0), (1,0), (0,-1), (0,1)
rotate_dict = {up:[left,right],down:[left,right],left:[up,down],right:[up,down]}

def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def parse_input01(fname):
    data = bh.parse_char_grid(path,fname)

    valid_set, start_tile, end_tile  = set(), None, None

    for i in range(len(data)):
        for j in range(len(data[0])):
            c = data[i][j]
            key = (i,j)
            if c!='#':
                valid_set.add(key)
            if c=='S':
                 start_tile = key   
            if c=='E':
                 end_tile = key   

    return valid_set, start_tile, end_tile

def build_graph(valid_set):
    forwardGraph, reverseGraph = Digraph(), Digraph()

    for coord in valid_set:
        for dir1 in rotate_dict:
            key1, next_coord = (coord,dir1), coord_addition(coord,dir1)

            if next_coord in valid_set:
                key2 = (next_coord,dir1)
                forwardGraph.add_edge(key1,key2,1)
                reverseGraph.add_edge(key2,key1,1)
            for dir2 in rotate_dict[dir1]:
                key2 = (coord,dir2)
                forwardGraph.add_edge(key1,key2,1000)
                reverseGraph.add_edge(key2,key1,1000)

    return forwardGraph, reverseGraph

def solution(show_result=True, fname='Input02.txt'):
    valid_set, start_tile, end_tile = parse_input01(fname)
    forwardGraph, reverseGraph = build_graph(valid_set)

    start_key, min_score, sit_set = (start_tile,right), None, set()

    forward_dist_dict, reverse_dist_dict = forwardGraph.compute_dist_dijkstra(start_key)['dist_dict'], dict()
 
    for end_dir in rotate_dict:
        end_key = (end_tile,end_dir)
        temp_dict = reverseGraph.compute_dist_dijkstra(end_key)['dist_dict']

        if min_score is None or forward_dist_dict[end_key]<min_score: min_score = forward_dist_dict[end_key]

        for mid_key in temp_dict:
            if mid_key in reverse_dist_dict: reverse_dist_dict[mid_key] = min(reverse_dist_dict[mid_key], temp_dict[mid_key])

            else: reverse_dist_dict[mid_key] = temp_dict[mid_key]

    for mid_key in forward_dist_dict:
        if forward_dist_dict[mid_key]+reverse_dist_dict[mid_key]==min_score: sit_set.add(mid_key[0])

    v1, v2 = min_score, len(sit_set)

    if show_result: print(str(v1)+'\n'+str(v2))

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

