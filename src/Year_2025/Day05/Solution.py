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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = ['-'],type_lookup = None, allInt = True, allFloat = False)

    return data

def check_fresh(fresh_ranges,val):   
    for item in fresh_ranges:
        if item[0]<=val and val<=item[1]:
            return True

    return False

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    fresh_ranges = data[0]

    total = 0
    for val in data[1]:
        if check_fresh(fresh_ranges,val[0]):
            total+=1

    if show_result:
        print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    fresh_ranges = sorted(data[0], key=lambda x: x[0])

    min_val, max_val = fresh_ranges[0][0], fresh_ranges[0][1]
    total = 0

    for item in fresh_ranges:
        if item[0]<=max_val:
            max_val = max(item[1],max_val)
        else:
            total+= (max_val-min_val)+1            
            min_val, max_val= item[0], item[1]

    total+= (max_val-min_val)+1

    if show_result:
        print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

