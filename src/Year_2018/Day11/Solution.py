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

def compute_power(x,y,q):
    rID = x+10
    p = rID*y
    p+=q
    p*=rID

    p//=100
    p%=10
    p-=5

    return p

def total_power3x3(x,y,q):
    total=0
    for i in range(x,x+3):
        for j in range(y,y+3):
            total+=compute_power(i,j,q)
    return total

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)
    # print(data)

    # print(compute_power(122,79,57))
    # print(compute_power(217,196,39))
    # print(compute_power(101,153,71))

    # q = 18
    # q = 42
    q = 7672

    max_val = None
    max_x = None
    max_y = None

    for x in range(1,299):
        for y in range(1,299):
            temp = total_power3x3(x,y,q)
            if max_val is None or temp>max_val:
                max_val = temp
                max_x = x
                max_y = y

    print(str(max_x)+','+str(max_y))

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)

    # q = 18
    # q = 42
    q = 7672

    cum_sum_x = dict()
    cum_sum_y = dict()

    for i in range(1,301):
        cum_sum_x[(0,i)]=0
        cum_sum_y[(i,0)]=0
        for j in range(1,301):
            cum_sum_x[(j,i)]=cum_sum_x[(j-1,i)]+compute_power(j,i,q)
            cum_sum_y[(i,j)]=cum_sum_y[(i,j-1)]+compute_power(i,j,q)

    max_val = compute_power(1,1,q)
    max_key = (1,1,1)

    power_table = dict()
    for x in range(1,301):
        for y in range(1,301):
            power_table[(x,y,1)]=compute_power(x,y,q)

            if power_table[(x,y,1)]>max_val:
                max_val = power_table[(x,y,1)]
                max_key = (x,y,1)

    for n in range(2,301):
        for x in range(1,301-(n-1)):
            for y in range(1,301-(n-1)):
                x_sum = cum_sum_x[(x+n-1,y+n-1)]-cum_sum_x[(x-1,y+n-1)]
                y_sum = cum_sum_y[(x+n-1,y+n-1)]-cum_sum_y[(x+n-1,y-1)]
                overlap = power_table[(x+n-1,y+n-1,1)]
                power_table[(x,y,n)]=power_table[(x,y,n-1)]+x_sum+y_sum-overlap

                if power_table[(x,y,n)]>max_val:
                    max_val = power_table[(x,y,n)]
                    max_key = (x,y,n)

    print(str(max_key[0])+','+str(max_key[1])+','+str(max_key[2]))


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

