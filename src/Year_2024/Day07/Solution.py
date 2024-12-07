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
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [':',' '],type_lookup = None, allInt = True, allFloat = False)

    return data

def is_correct(val,subtotal,num_list,i,p2_flag=False):
    if i==len(num_list):
        return val==subtotal

    b1 = is_correct(val,subtotal*num_list[i],num_list,i+1,p2_flag)
    b2 = is_correct(val,subtotal+num_list[i],num_list,i+1,p2_flag)
    b3 = is_correct(val,int(str(subtotal)+str(num_list[i])),num_list,i+1,p2_flag)

    return b1 or b2 or (b3 and p2_flag)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    num_table = parse_input01(fname)
    
    total1, total2 = 0, 0
    for num_list in num_table:
        if is_correct(num_list[0],num_list[1],num_list,2): total1+=num_list[0]
        if is_correct(num_list[0],num_list[1],num_list,2,True): total2+=num_list[0]
    print(total1)
    print(total2)


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

