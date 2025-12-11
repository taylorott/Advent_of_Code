#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList, UnionFind
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = bh.parse_strings(path,fname,delimiters = [' ',':'],type_lookup = None, allInt = False, allFloat = False)

    myDigraph = Digraph()

    for row in data:
        for i in range(1,len(row)):
            myDigraph.add_edge(row[0],row[i])

    return myDigraph

def assign_ordering(myDigraph,vertex,vertex_ordering = None, visited_set = None, is_start = True):
    if visited_set is None:
        visited_set = set()

    if vertex_ordering is None:
        vertex_ordering = []

    if vertex in visited_set:
        return vertex_ordering

    for next_vertex in myDigraph.forward_adjacency[vertex]:
        assign_ordering(myDigraph,next_vertex,vertex_ordering,visited_set, False)

    vertex_ordering.append(vertex)
    visited_set.add(vertex)

    if is_start:
        vertex_ordering.reverse()

    return vertex_ordering

def compute_paths(v1,v2,myDigraph,vertex_ordering):
    path_dict = {v1: 1}

    for vertex in vertex_ordering:
        if vertex not in path_dict:
            path_dict[vertex] = 0

        for prev_vertex in myDigraph.reverse_adjacency[vertex]:
            if prev_vertex in path_dict:
                path_dict[vertex]+=path_dict[prev_vertex]

    if v2 in path_dict:
        return path_dict[v2]

    return 0

def solution01(show_result=True, fname='Input02.txt'):
    myDigraph = parse_input01(fname)

    vertex_ordering = assign_ordering(myDigraph,'you')

    res = compute_paths('you','out',myDigraph,vertex_ordering)

    if show_result:
        print(res)

    return res

def solution02(show_result=True, fname='Input02.txt'):
    myDigraph = parse_input01(fname)

    vertex_ordering = assign_ordering(myDigraph,'svr')

    route_lists = [['svr','fft','dac','out'],
                   ['svr','dac','fft','out']]

    total = 0

    for route in route_lists:
        temp = 1

        for i in range(len(route)-1):
            temp*=compute_paths(route[i],route[i+1],myDigraph,vertex_ordering)   

        total+=temp

    if show_result:
        print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

