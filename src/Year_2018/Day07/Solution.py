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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)[0]

    myGraph = Digraph()

    for item in data:
        v1 = item[1]
        v2 = item[7]

        myGraph.add_edge(v1,v2)
        
    vertex_heap = []

    for vertex in myGraph.vertex_set:
        if myGraph.in_degree[vertex]==0:
            hq.heappush(vertex_heap,vertex)

    str_out = ''

    while myGraph.numVertices>0:
        vertex = hq.heappop(vertex_heap)
        str_out+=vertex

        for vertex_next in myGraph.forward_adjacency[vertex]:
            if myGraph.in_degree[vertex_next]==1:
                hq.heappush(vertex_heap,vertex_next)
        myGraph.remove_vertex(vertex)

    print(str_out)



def solution02():
    # fname = 'Input01.txt'
    # time_to_add = 0
    # num_workers = 2

    fname = 'Input02.txt'
    time_to_add = 60
    num_workers = 5

    data = parse_input01(fname)[0]

    myGraph = Digraph()

    for item in data:
        v1 = item[1]
        v2 = item[7]

        myGraph.add_edge(v1,v2)
        
    vertex_heap = []

    for vertex in myGraph.vertex_set:
        myGraph.vertex_dict[vertex] = ord(vertex)-ord('A')+1+time_to_add
        if myGraph.in_degree[vertex]==0:
            hq.heappush(vertex_heap,vertex)

    worker_list = [None]*num_workers

    
    for i in range(len(worker_list)):
        if worker_list[i] is None and len(vertex_heap)>0:
            worker_list[i] = hq.heappop(vertex_heap)
    
    t = 0    
    while myGraph.numVertices>0:
        for i in range(len(worker_list)):
            vertex = worker_list[i]

            if vertex is None:
                continue
                
            myGraph.vertex_dict[vertex]-=1

            if myGraph.vertex_dict[vertex]==0:
                for vertex_next in myGraph.forward_adjacency[vertex]:
                    if myGraph.in_degree[vertex_next]==1:
                        hq.heappush(vertex_heap,vertex_next)
                myGraph.remove_vertex(vertex)
                worker_list[i] = None

        for i in range(len(worker_list)):
            if worker_list[i] is None and len(vertex_heap)>0:
                worker_list[i] = hq.heappop(vertex_heap)
        t+=1

    print(t)

    


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

