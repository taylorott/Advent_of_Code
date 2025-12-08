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
    data = bh.parse_strings(path,fname,delimiters = [','],type_lookup = None, allInt = True, allFloat = False)
    return data

def compute_dist(c1,c2):
    total = 0
    for i in range(3):
        total+=(c1[i]-c2[i])*(c1[i]-c2[i])
    return total

def solution(show_result=True, fname='Input02.txt', num_connections = 1000):

    data = parse_input01(fname)

    n = len(data)
    dist_list_unsorted = []

    for i in range(n):
        for j in range(i+1,n):
            d = compute_dist(data[i],data[j])
            dist_list_unsorted.append([d,i,j])

    dist_list = sorted(dist_list_unsorted, key=lambda item: item[0])

    myUnionFind = UnionFind()

    for i in range(n):
        myUnionFind.add_key(i)

    for i in range(num_connections):
        myUnionFind.union(dist_list[i][1],dist_list[i][2])

    size_list = []

    for leader in myUnionFind.size_dict:
        size_list.append(myUnionFind.get_size(leader))

    size_list.sort(reverse = True)

    prod1 = size_list[0]*size_list[1]*size_list[2]

    k = num_connections-1
    while len(myUnionFind.size_dict)>1:
        k+=1
        myUnionFind.union(dist_list[k][1],dist_list[k][2])

    prod2 = data[dist_list[k][1]][0]*data[dist_list[k][2]][0]
        
    if show_result:    
        print(prod1)
        print(prod2)

    return prod1, prod2


if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

