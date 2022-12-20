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
    
    data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    
    state_list = deque(data)
    has_moved_list = deque([False]*len(data))

    move_count = 0
    l = len(data)

    while move_count<l:
        while has_moved_list[0]:
            state_list.append(state_list.popleft())
            has_moved_list.append(has_moved_list.popleft())

        new_pos = state_list[0]%(l-1)

        temp = state_list.popleft()
        state_list.insert(new_pos,temp)

        dummy = has_moved_list.popleft()
        has_moved_list.insert(new_pos,True)

        move_count+=1

    state_list = list(state_list)

    zero_index = None
    for i in range(l):
        if state_list[i]==0:
            zero_index=i

    index1 = (1000+zero_index)%l
    index2 = (2000+zero_index)%l
    index3 = (3000+zero_index)%l

    print(state_list[index1]+state_list[index2]+state_list[index3])

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    l = len(data)

    decryption_key = 811589153

    for i in range(l):
        data[i]*=decryption_key

    state_list = deque(data)
    move_order_list = deque()
    for i in range(l): 
        move_order_list.append(i)

    
    for i in range(10):
        move_count = 0
        while move_count<l:
            while move_count!=move_order_list[0]:
                state_list.append(state_list.popleft())
                move_order_list.append(move_order_list.popleft())

            new_pos = state_list[0]%(l-1)

            temp = state_list.popleft()
            state_list.insert(new_pos,temp)

            temp = move_order_list.popleft()
            move_order_list.insert(new_pos,temp)

            move_count+=1

    state_list = list(state_list)

    zero_index = None
    for i in range(l):
        if state_list[i]==0:
            zero_index=i

    index1 = (1000+zero_index)%l
    index2 = (2000+zero_index)%l
    index3 = (3000+zero_index)%l

    print(state_list[index1]+state_list[index2]+state_list[index3])


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

