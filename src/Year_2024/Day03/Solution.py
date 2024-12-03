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
    data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    # fname = 'Input03.txt'

    data = parse_input01(fname)
    my_regex = r'mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don\'t\(\)'

    total1, total2, is_enabled = 0, 0, True

    for line_str in data: 
        for regex_match in re.finditer(my_regex,line_str):
            if regex_match.group()=='do()': is_enabled = True
            if regex_match.group()=='don\'t()': is_enabled = False
            if regex_match.group()[0:3]=='mul':
                temp = int(regex_match.group(1))*int(regex_match.group(2))
                total1+=temp
                if is_enabled: total2+=temp
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
    

