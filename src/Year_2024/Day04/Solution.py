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
    return bh.parse_char_grid(path,fname)

def match_xmas1(list_in):
    total = 0
    my_regex = r'XMAS'

    for item in list_in:
        match_list = re.findall(my_regex,item)
        total+=len(match_list)

    return total

def match_xmas2(grid_in,i,j):
    middle    = grid_in[i][j]
    top_left  = grid_in[i-1][j-1]
    top_right = grid_in[i-1][j+1]
    bot_left  = grid_in[i+1][j-1]
    bot_right = grid_in[i+1][j+1]

    test1 = middle=='A' 
    test2 = (top_left=='M' and bot_right=='S') or (top_left=='S' and bot_right=='M')
    test3 = (top_right=='M' and bot_left=='S') or (top_right=='S' and bot_left=='M')


    if test1 and test2 and test3:
        return 1
    return 0

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0
    for i in range(4):
        str_list1 = bh.listlist_to_str_list(data)
        str_list2 = bh.listlist_to_str_list(bh.grid_diagonals_down_left(data))

        total+=match_xmas1(str_list1)
        total+=match_xmas1(str_list2)

        data = bh.rotate_grid(data,1)

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0
    h = len(data)
    w = len(data[0])
    for i in range(1,h-1):
        for j in range(1,w-1):
            total+=match_xmas2(data,i,j)

    if show_result: print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

