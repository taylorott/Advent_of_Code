#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = ['-',','],type_lookup = None, allInt = True, allFloat = False)

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    count = 0

    for item in data:
        c1 = item[0]<=item[2] and item[1]>=item[3]
        c2 = item[0]>=item[2] and item[1]<=item[3]
        if c1 or c2:
            count+=1

    print(count)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    count = 0

    for item in data:
        c1 = item[1]<item[2]
        c2 = item[0]>item[3]
        if not(c1 or c2):
            count+=1

    print(count)

if __name__ == '__main__':
    solution01()
    solution02()
    

