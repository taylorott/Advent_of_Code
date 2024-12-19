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

    data = bh.parse_split_by_emptylines(path,fname,delimiters = [' ',','],type_lookup = None, allInt = False, allFloat = False)
    pattern_set = set()

    for item in data[0][0]:
        pattern_set.add(item)

    return pattern_set, data[1]

def check_pattern_recursive(pattern,myset,mytable=None,current_index=0):
    if mytable is None: mytable = dict()

    if current_index in mytable: return mytable[current_index]

    if current_index == len(pattern): return 1

    mytable[current_index]  = 0

    for item in myset:
        if len(item)+current_index<=len(pattern) and pattern[current_index: (current_index+len(item))]==item:
            mytable[current_index] += check_pattern_recursive(pattern,myset,mytable,current_index+len(item))

    return mytable[current_index]  

def solution(show_result=True, fname='Input02.txt'):
    myset, pattern_list = parse_input01(fname)

    total1, total2 = 0, 0
    for item in pattern_list:
        temp = check_pattern_recursive(item[0],myset,dict()) 
        total1, total2= total1+(temp>0), total2+temp

    if show_result: print(str(total1)+'\n'+str(total2))
    
    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

