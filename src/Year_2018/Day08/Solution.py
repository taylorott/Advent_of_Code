#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [' '],type_lookup = None, allInt = True, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def build_tree(myGraph,node_list,current_index=0):
    num_children = node_list[current_index]
    num_meta = node_list[current_index+1]

    next_index = current_index+2

    for i in range(num_children):
        myGraph.add_edge(current_index,next_index)
        next_index = build_tree(myGraph,node_list,next_index)

    myGraph.vertex_dict[current_index] = node_list[next_index:(next_index+num_meta)]
    next_index+=num_meta

    return next_index

def compute_value(myGraph,value_dict,current_index=0):
    if current_index in value_dict:
        return value_dict[current_index]

    if len(myGraph.forward_adjacency[current_index])==0:
        value_dict[current_index] = sum(myGraph.vertex_dict[current_index]) 
        return value_dict[current_index]

    total = 0

    forward_list = myGraph.forward_adjacency_list(current_index)
    forward_list.sort()

    for i in myGraph.vertex_dict[current_index]:
        if i-1>=0 and i-1<len(forward_list):
            total+=compute_value(myGraph,value_dict,forward_list[i-1])

    value_dict[current_index] = total
    return value_dict[current_index]


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    node_list = parse_input01(fname)[0][0]

    myGraph = Digraph()

    build_tree(myGraph,node_list)
    
    total = 0
    for vertex in myGraph.vertex_dict:
        total+=sum(myGraph.vertex_dict[vertex])
    print(total)

    value_dict = {}
    root_val = compute_value(myGraph,value_dict)
    print(root_val)


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

