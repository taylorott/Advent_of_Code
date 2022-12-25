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

SNAFU_forward_dict = {'2':2,'1':1,'0':0,'-':-1,'=':-2}
SNAFU_reverse_dict = {2:'2',1:'1',0:'0',-1:'-',-2:'='}

def SNAFU_forward(str_in):
    total = 0
    base = 1
    for i in range(len(str_in)-1,-1,-1):
        total+=SNAFU_forward_dict[str_in[i]]*base
        base*=5


    return total

def to_base_five(v_in):
    list_out = [0]

    base = 1
    while base<=v_in:
        base*=5

    while base>1:
        base//=5
        list_out.append(v_in//base)
        v_in%=base

    return list_out

def SNAFU_preprocess(list_in):
    for i in range(len(list_in)-1,0,-1):
        if list_in[i]>=3:
            list_in[i]-=5
            list_in[i-1]+=1

    while list_in[0]==0:
        list_in.pop(0)

def SNAFU_reverse(v_in):
    v_list = to_base_five(v_in)
    SNAFU_preprocess(v_list)

    str_out = ''
    for item in v_list:
        str_out+=SNAFU_reverse_dict[item]

    return str_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for item in data:
        total += SNAFU_forward(item)

    print(SNAFU_reverse(total))


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

