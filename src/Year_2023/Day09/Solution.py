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
    return np.array(bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = True, allFloat = False))

def test_all_zero(array_in):
    return (array_in != 0).sum()==0

def compute_val(current_array):
    total = 0
    while len(current_array)>0 and not test_all_zero(current_array):
        total+=current_array[-1]
        current_array = current_array[1:len(current_array)]-current_array[0:(len(current_array)-1)]
    return total

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0
    for row in data:
        total+=compute_val(row)

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0
    for row in data:
        total+=compute_val(np.flip(row))

    if show_result: print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))