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
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def update_state(index1,index2,score_list):
    score_sum = score_list[index1]+score_list[index2]
    score_list+=bh.int_to_digit_list(score_sum)

    index1+=1+score_list[index1]
    index1%=len(score_list)

    index2+=1+score_list[index2]
    index2%=len(score_list)

    return index1,index2

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)

    # num_iter = 2018
    num_iter = 598701

    num_extra = 10

    index1, index2, score_list = 0,1, [3,7]

    for i in range(num_iter+num_extra):
        index1,index2 = update_state(index1,index2,score_list)  

    list_out = score_list[num_iter:(num_iter+num_extra)]
    print(bh.digit_list_to_str(list_out))

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)

    # input_val = 92510
    # input_val = 59414
    # input_val = 515891
    input_val = 598701

    target_str = str(input_val)

    index1, index2, score_list = 0,1, [3,7]

    while True:
        i1 = max(len(score_list)-len(target_str),0)
        i2 = len(score_list)
        test_str1 = bh.digit_list_to_str(score_list[i1:i2])

        i3 = max(len(score_list)-len(target_str)-1,0)
        i4 = max(len(score_list)-1,0)
        test_str2 = bh.digit_list_to_str(score_list[i3:i4])

        if test_str1 == target_str:
            print(i1)
            break

        if test_str2 == target_str:
            print(i3)
            break
            
        index1,index2 = update_state(index1,index2,score_list)  

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

