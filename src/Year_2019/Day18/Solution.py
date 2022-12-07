#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    return data

direction_dict = [(1,0),(0,1),(-1,0),(0,-1)]

def build_graph(grid_in):
    l1 = len(grid_in)
    l2 = len(grid_in[0])

    myGraph = Digraph()

    for i in range(l1):
        for j in range(l2):
            if grid_in[i][j]!='#':
                myGraph.set_vertex_val((i,j),grid_in[i][j])

                for k in range(4):
                    i_adj = i + direction_dict[k][0]
                    j_adj = j + direction_dict[k][1]

                    if 0<=i_adj and i_adj<l1 and 0<=j_adj and j_adj<l2 and grid_in[i_adj][j_adj]!='#':
                        myGraph.add_edge((i,j),(i_adj,j_adj))

    return myGraph

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)[0]

    myGraph = build_graph(data)

    # for vertex in myGraph.vertex_list:
    #     print(vertex)
    #     print(myGraph.vertex_dict[vertex])
    #     print(myGraph.forward_adjacency[vertex])
    #     print(' ')


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)

if __name__ == '__main__':
    solution01()
    solution02()
    

