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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = ['initial state: ',' => '],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    current_state = dict()
    for i in range(len(data[0][0][0])):
        current_state[i]=data[0][0][0][i]

    update_dict = dict()
    for rule in data[1]:
        update_dict[rule[0]]=rule[1]


    return current_state, update_dict

def update_plants(current_state,update_dict):
    next_state = dict()

    max_index = None
    min_index = None

    for i in current_state:
        if max_index is None: max_index = i
        if min_index is None: min_index = i
        max_index = max(i,max_index)
        min_index = min(i,min_index)

    table = 0
    for i in range(min_index-2,max_index+3):
        key = ''

        for j in range(5):
            if i+j-2 in current_state:
                key+=current_state[i+j-2]
            else:
                key+='.'
        if key in update_dict and update_dict[key]=='#': next_state[i]='#'

    return next_state

def memoize_state(state_dict):
    min_index = None
    index_list = []
    for i in state_dict:
        index_list.append(i)
        if min_index is None:min_index = i
        min_index = min(i,min_index)

    for i in range(len(index_list)):
        index_list[i]-=min_index
    
    index_list.sort()

    return tuple(index_list),min_index

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    current_state, update_dict = parse_input01(fname)

    for i in range(20):
        current_state =update_plants(current_state,update_dict)

    total = 0
    for key in current_state:
        total+=key
    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    current_state, update_dict = parse_input01(fname)

    memo_dict = dict()
    state_table = dict()
    count = 0
    while True:
        key,min_index = memoize_state(current_state)

        if key in memo_dict:
            break
        memo_dict[key]=[min_index,count]
        state_table[count]=[key,min_index]

        count+=1
        current_state =update_plants(current_state,update_dict)

    x1 = memo_dict[key][0]
    t1 = memo_dict[key][1]
    x2 = min_index
    t2 = count

    tf = 50000000000

    num_iter = (tf-t1)//(t2-t1)
    t_rem = (tf-t1)%(t2-t1)

    final_state = state_table[t1+t_rem][0]
    xa = state_table[t1+t_rem][1]

    xf = num_iter*(x2-x1)+xa

    print(sum(final_state)+len(final_state)*xf)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

