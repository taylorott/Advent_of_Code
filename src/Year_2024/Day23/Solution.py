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
    data = bh.parse_strings(path,fname,delimiters = ['-'],type_lookup = None, allInt = False, allFloat = False)

    myGraph = Graph()
    for item in data:
        myGraph.add_edge(item[0],item[1])

    return myGraph

def find_cliques(key,myGraph,clique_set,shared_set):
    if key in clique_set: return None

    clique_set.add(key)


    for next_vertex in shared_set:
        next_key = tuple(sorted(list(key)+[next_vertex]))
        next_shared_set = shared_set.intersection(myGraph.adjacency_set[next_vertex])

        find_cliques(next_key,myGraph,clique_set,next_shared_set)

def clique_to_str(clique):
    str_out = ''
    for item in clique:
        str_out+=item+','
    return str_out[0:len(str_out)-1]

def solution(show_result=True, fname='Input02.txt'):
    myGraph = parse_input01(fname)

    clique_set, biggest_clique, total = set(), [], 0
    for vertex in myGraph.vertex_set:
        find_cliques(tuple([vertex]),myGraph,clique_set,set(myGraph.adjacency_set[vertex]))


    for clique in clique_set:
        if len(clique)>len(biggest_clique): biggest_clique = clique

        if len(clique)==3:
            for vertex in clique:
                if vertex[0]=='t':
                    total+=1
                    break
            
    str_out = clique_to_str(biggest_clique)

    if show_result: print(str(total)+'\n'+str_out)
    
    return total, str_out

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

