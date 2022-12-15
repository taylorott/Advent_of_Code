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

    data = parse_input01(fname)

    two_count = 0
    three_count = 0

    for item in data:
        my_freq_table = bh.build_freq_table(item)

        has_two = False
        has_three = False

        for key in my_freq_table.keys():
            has_two = has_two or my_freq_table[key]==2
            has_three = has_three or my_freq_table[key]==3

        if has_two:
            two_count+=1
        if has_three:
            three_count+=1

    print(two_count*three_count)

def compare_strings(str1,str2):
    total = 0

    str_out = ''
    for i in range(len(str1)):
        if str1[i]!=str2[i]:
            total+=1
        else:
            str_out+=str1[i]

    return total==1,str_out

def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    for i in range(len(data)):
        for j in range(i):
            result,str_out = compare_strings(data[i],data[j])
    
            if result:
                print(str_out)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

