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

path = currentdir

def parse_input01(fname):
    data = None

    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    current_pos = None
    target_pos = None
    for i in range(len(data)):
        for j in range(len(data[0])):
            if 'a'<=data[i][j] and data[i][j]<='z':
                data[i][j] = ord(data[i][j])-ord('a')

            elif data[i][j]=='S':
                current_pos = (i,j)
                data[i][j] = 0
            elif data[i][j]=='E':
                target_pos = (i,j)
                data[i][j] = 25

    return data, current_pos, target_pos

def adjacency_criteria(grid_in,current_vert,neighbor_vert):
    i = current_vert[0]
    j = current_vert[1]

    i_temp = neighbor_vert[0]
    j_temp = neighbor_vert[1]

    return grid_in[i][j]+1>=grid_in[i_temp][j_temp]

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data, starting_vert, target_vert = parse_input01(fname)
    myGraph = Digraph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria)

    dist_out = myGraph.compute_dist_BFS(starting_vert,target_vert)
    print(dist_out)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data, dummy, target_vert = parse_input01(fname)
    myGraph = Digraph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria)

    min_dist = None

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]==0:
                starting_vert = (i,j)

                dist_out = myGraph.compute_dist_BFS(starting_vert,target_vert)

                if min_dist is None:
                    min_dist = dist_out
                elif dist_out is not None:
                    min_dist = min(min_dist,dist_out)
    print(min_dist)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

