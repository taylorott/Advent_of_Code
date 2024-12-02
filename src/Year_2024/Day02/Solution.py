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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = True, allFloat = False)

    return data
    
def check_safety(list_in):
    change_is_bounded = True

    does_increase = False
    does_decrease = False

    for i in range(len(list_in)-1):
        diff_val = list_in[i+1]-list_in[i]
        
        change_is_bounded&=(abs(diff_val)>=1 and abs(diff_val)<=3)
        does_increase|= diff_val>0
        does_decrease|= diff_val<0

    return change_is_bounded and not(does_increase and does_decrease)

def check_loose_safety(list_in):
    if check_safety(list_in):
        return True

    for i in range(len(list_in)):
        temp_list = list_in[0:i]+list_in[i+1:len(list_in)]
        if check_safety(temp_list):
            return True

    return False

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    total = 0
    for item in data:
        if check_safety(item):
            total+=1
    print(total)

    total = 0
    for item in data:
        if check_loose_safety(item):
            total+=1
    print(total)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

