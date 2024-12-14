#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    return bh.parse_extract_ints_split_by_emptylines(path,fname)

def solution01(show_result=True, fname='Input01.txt'):
    data = parse_input01(fname)
    data = np.transpose(data[0])

    l1 = data[0]
    l2 = data[1]

    l1.sort()
    l2.sort()

    total = 0
    for i in range(len(l1)):
        total += abs(l1[i]-l2[i])

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input01.txt'):
    data = parse_input01(fname)
    data = np.transpose(data[0])

    l1 = data[0]
    freq_table = frequency_table(data[1])

    total = 0

    for item in l1:
        if item in freq_table:
            total+=item*freq_table[item]

    if show_result: print(total) 

    return total


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

