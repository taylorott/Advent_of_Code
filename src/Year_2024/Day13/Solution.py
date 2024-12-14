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
    return bh.parse_extract_ints_split_by_emptylines(path,fname)

def test_block(T, p2_flag=False):
    a,c,b,d,e,f=T[0][0],T[0][1],T[1][0],T[1][1],T[2][0],T[2][1]

    if p2_flag: e,f=e+10000000000000, f+10000000000000   
    
    q1, q2 = (d*e-b*f)//(a*d-b*c), (-c*e+a*f)//(a*d-b*c)
    
    return (q1*a+q2*b == e and q1*c+q2*d == f) * (3*q1+q2)

def solution(show_result=True, fname='Input02.txt'):
    data, total1, total2 = parse_input01(fname), 0, 0
    
    for block in data: total1, total2=total1+test_block(block), total2+test_block(block, True)
    
    if show_result: print(str(total1)+'\n'+str(total2))      
    
    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

