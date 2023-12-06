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
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    return data

def count_ways_to_win_slow(t,d):
    total = 0

    for i in range(t+1):
        if i*(t-i)>d:
            total+=1

    return total

def count_ways_to_win_fast(t,d):
    #(t-n)*n > d  
    #n^2-t*n+d <0

    a = min(int(np.floor((t+np.sqrt(t**2-4*d))/2.0)),d)
    b = max(0,int(np.ceil((t-np.sqrt(t**2-4*d))/2.0)))

    if a**2-t*a+d==0:
        a-=1
    if b**2-t*b+d==0:
        b+=1

    return max(a-b+1,0)

def count_ways_to_win(t,d):
    return count_ways_to_win_fast(t,d)
    # return count_ways_to_win_slow(t,d)    

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    time_list = []
    distance_list = []

    for i in range(1,len(data[0])):
        time_list.append(int(data[0][i]))

    for i in range(1,len(data[1])):
        distance_list.append(int(data[1][i]))

    total=1
    for i in range(len(time_list)):
        total*=count_ways_to_win(time_list[i],distance_list[i])
    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    str1 = ''
    str2 = ''

    for i in range(1,len(data[0])):
        str1+=data[0][i]

    for i in range(1,len(data[1])):
        str2+=data[1][i]

    t = int(str1)
    d = int(str2)

    print(count_ways_to_win(t,d))

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

