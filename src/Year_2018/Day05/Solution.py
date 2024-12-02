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
    data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def shorten_polymer(str_in,char_remove_index = None):
    if char_remove_index is not None:
        char_remove_lower = chr(ord('a')+char_remove_index)
        char_remove_upper = chr(ord('A')+char_remove_index)

        str_in = str_in.replace(char_remove_lower,'')
        str_in = str_in.replace(char_remove_upper,'')


    match_diff = abs(ord('A')-ord('a'))

    list_out = []

    for item in str_in:
        if len(list_out)==0:
            list_out.append(item)
            continue

        char_diff = abs(ord(list_out[-1])-ord(item))
        if char_diff==match_diff:
            list_out.pop(-1)
        else:
            list_out.append(item)    

    return len(list_out)    

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)[0]
    
    print(shorten_polymer(data))

    
    min_val = None

    for i in range(26):
        temp_val = shorten_polymer(data,i)
        if min_val is None or temp_val<min_val:
            min_val = temp_val

    print(min_val)

    



def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

