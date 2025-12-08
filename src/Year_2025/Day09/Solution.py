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
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_extract_ints_split_by_emptylines(path,fname)
    # data = bh.parse_extract_ints(path,fname)

    return data

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)
    print(data)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

