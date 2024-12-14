#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [''],type_lookup = None, allInt = True, allFloat = False)

    return data

dir_list = [(1,0),(0,1),(-1,0),(0,-1)]

regular_crucible = [1,3]
ultra_crucible = [4,10]

def turn_left(dir_in):
    return (dir_in[1],-dir_in[0])
def turn_right(dir_in):
    return (-dir_in[1],dir_in[0])

def add_outgoing_edges(grid_in,myGraph,coord_in,dir_in,crucible_type):
    current_key = (coord_in,dir_in)

    edge_weight = 0

    for i in range(1,crucible_type[-1]+1):
        coord_next = (coord_in[0]+i*dir_in[0],coord_in[1]+i*dir_in[1])

        if 0<=coord_next[0] and coord_next[0]<len(grid_in) and 0<=coord_next[1] and coord_next[1]<len(grid_in[0]):
            edge_weight+=grid_in[coord_next[0]][coord_next[1]]

            if i>=crucible_type[0]:
                dir_left = turn_left(dir_in)
                dir_right = turn_right(dir_in)
                key_left = (coord_next,dir_left)
                key_right = (coord_next,dir_right)
                myGraph.add_edge(current_key,key_left,w=edge_weight)
                myGraph.add_edge(current_key,key_right,w=edge_weight)

def build_graph(grid_in,start_coord,end_coord,crucible_type):
    myGraph = Digraph()

    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            for direction in dir_list:
                add_outgoing_edges(grid_in,myGraph,(i,j),direction,crucible_type)

    for direction in dir_list:
        myGraph.add_edge(start_coord,(start_coord,direction),0)
        myGraph.add_edge((end_coord,direction),end_coord,0)

    return myGraph

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    start_coord, end_coord = (0,0), (len(data)-1,len(data[0])-1)

    myGraph = build_graph(data,start_coord,end_coord,regular_crucible)

    result = myGraph.compute_dist_dijkstra(start_coord,end_coord)['path_length']

    if show_result: print(result)

    return result

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    start_coord, end_coord = (0,0), (len(data)-1,len(data[0])-1)

    myGraph = build_graph(data,start_coord,end_coord,ultra_crucible)

    result = myGraph.compute_dist_dijkstra(start_coord,end_coord)['path_length']

    if show_result: print(result)

    return result
   

if __name__ == '__main__':
    t0 = time.time()
    solution01('Input01.txt')
    # solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

