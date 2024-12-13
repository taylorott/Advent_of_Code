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
    return bh.parse_split_by_emptylines(path,fname,delimiters = [' ',':','\+','=',','],type_lookup = None, allInt = False, allFloat = False)

def test_block(block, p2_flag=False):
    a, c = int(block[0][3]), int(block[0][5])
    b, d = int(block[1][3]), int(block[1][5])
     
    e, f = int(block[2][2]), int(block[2][4])

    if p2_flag:
        e+=10000000000000
        f+=10000000000000

    M = np.array([[a,b],[c,d]])
    Y = np.array([e,f])
    X = np.linalg.solve(M,Y)

    q1, q2 = round(X[0]), round(X[1])

    if q1*a+q2*b == e and q1*c+q2*d == f: return 3*q1+q2

    return 0

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total1 = 0
    total2 = 0
    for block in data:
        total1+=test_block(block)
        total2+=test_block(block, True)
  
    if show_result:
        print(total1)
        print(total2)
    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

