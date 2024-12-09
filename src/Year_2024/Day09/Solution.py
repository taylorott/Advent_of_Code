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
    data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data[0]

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    val_list = []

    data = parse_input01(fname)
    
    for i in range(len(data)):
        if i%2==0:
            val_list+=[i//2]*data[i]
        else:
            val_list+=[None]*data[i]

    index1 = 0
    index2 = len(val_list)-1
    while index1<index2:
        while val_list[index1] is not None: index1+=1

        while val_list[index2] is None: index2-=1

        if index1<index2:
            val_list[index1]=val_list[index2]
            val_list[index2]=None

    print(compute_score(val_list))

def compute_score(val_list):
    total = 0
    for i in range(len(val_list)): 
        if val_list[i] is not None: 
            total+=i*val_list[i]
    return total

def move_file_block(block_list,index1):
    index2 = 0
    while index2<index1:
        if block_list[index2][0]>block_list[index1][0] and block_list[index2][1] is None:
            block_list[index2][0]-=block_list[index1][0]
            swap_val = list(block_list[index1])
            block_list[index1][1] = None
            block_list.insert(index2,swap_val)
            return True
        elif block_list[index2][0]==block_list[index1][0] and block_list[index2][1] is None:
            block_list[index2][1]=block_list[index1][1]
            block_list[index1][1]=None
            return False
        index2+=1
    return False

def solution02a():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)

    block_list = []

    for i in range(len(data)):
        if data[i]!=0:
            if i%2==0: block_list.append([data[i],i//2])
            else: block_list.append([data[i],None])

    index1 = len(block_list)-1

    while index1>=0:
        if block_list[index1][1] is not None and move_file_block(block_list,index1): index1+=1
        index1-=1

    val_list = []
    for item in block_list: val_list+=[item[1]]*item[0]

    print(compute_score(val_list))



def solution02b():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    data = parse_input01(fname)

    empty_block_table = []

    for i in range(10): empty_block_table.append([])

    occupied_block_list = []
    block_index = 0
    for i in range(len(data)):
        if data[i]!=0:
            if i%2==0: 
                occupied_block_list.append([block_index, data[i], i//2])
            else: 
                hq.heappush(empty_block_table[data[i]], block_index)
            block_index+=data[i]

    total = 0
    while len(occupied_block_list)>0:
        item = occupied_block_list.pop(-1)

        block_index, block_size, block_id = item[0], item[1], item[2]

        swap_index, swap_size = block_index, None

        for i in range(block_size,10):
            if len(empty_block_table[i])>0 and (swap_index is None or  empty_block_table[i][0]<swap_index):
                swap_index = empty_block_table[i][0]
                swap_size = i

        if swap_size is not None:
            hq.heappop(empty_block_table[swap_size])
            block_index = swap_index
    
            if swap_size > block_size:
                remaining_size = swap_size-block_size
                hq.heappush(empty_block_table[remaining_size],swap_index+block_size)

        total+= (block_id*block_size*(2*block_index+block_size-1))//2
    print(total)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02b()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

