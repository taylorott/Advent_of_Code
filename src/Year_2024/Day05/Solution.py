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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [',','\|'],type_lookup = None, allInt = True, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    order_set = {}
    for order_pair in data[0]:
        a,b = order_pair[0],order_pair[1]

        if a in order_set: order_set[a].add(b)
        else: order_set[a]= {b}
    key=cmp_to_key(lambda x,y: 2*(y in order_set and x in order_set[y])-1)

    total1,total2 = 0, 0
    for list1 in data[1]:
        list2 = sorted(list1, key=key)

        if list1==list2: total1+=list2[len(list2)//2]
        else: total2+=list2[len(list2)//2]
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
    

