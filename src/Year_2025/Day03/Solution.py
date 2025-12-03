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

    data = bh.parse_digit_grid(path,fname)
    
    return data


def max_digit_left(row,min_index,max_index):
    
    index_out, digit_out = max_index, row[max_index]

    for k in range(max_index-1,min_index-1,-1):
        if row[k]>=digit_out:
            index_out, digit_out = k, row[k]

    return index_out, digit_out

def get_joltage(row,k):
    min_index, max_index, joltage= 0, len(row)-k, 0
    
    for power in range(k-1,-1,-1):
        index_out, digit_out = max_digit_left(row,min_index,max_index)
        joltage += digit_out*(10**power)
        
        min_index = index_out+1
        max_index+=1

    return joltage

def solution(show_result=True, fname='Input02.txt'):
    
    data = parse_input01(fname)

    total1, total2 = 0, 0

    for row in data:
        total1+= get_joltage(row,2)
        total2+= get_joltage(row,12)
        
    if show_result:
        print(total1)
        print(total2)

    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

