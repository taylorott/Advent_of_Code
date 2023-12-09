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
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = True, allFloat = False)

    return np.array(data)

def test_all_zero(array_in):
    return (array_in != 0).sum()==0

def extract_diagonal_list(current_array,target_index):
    list_out = []

    while len(current_array)>0 and not test_all_zero(current_array):
        list_out.append(current_array[target_index])
        current_array = current_array[1:len(current_array)]-current_array[0:(len(current_array)-1)]

    return np.array(list_out)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for row in data:
        diagonal_list = extract_diagonal_list(row,-1)
        total+=diagonal_list.sum()

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for row in data:
        diagonal_list = extract_diagonal_list(row,0)

        temp_val = 0
        for i in range(len(diagonal_list)-1,-1,-1):
            temp_val = diagonal_list[i]-temp_val
        total+=temp_val
    print(total)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

