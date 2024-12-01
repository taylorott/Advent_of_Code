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
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = ['-',' ',':','\[','\]'],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def compare_function(x,y):
    code1 = int(x[1])*(10**6)+int(x[2])*(10**4)+int(x[3])*(10**2)+int(x[4])
    code2 = int(y[1])*(10**6)+int(y[2])*(10**4)+int(y[3])*(10**2)+int(y[4])
    
    if code1>code2:
        return 1
    if code1<code2:
        return -1
    if code1==code2:
        return 0

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)[0]
    data = sorted(data, key=cmp_to_key(compare_function))

    guard_table = dict()
    current_guard = None

    is_awake = True
    sleep_start = None

    for item in data:
        time_min = int(item[4])

        code = item[5]

        if code=='Guard':
            current_guard = int(item[6][1:])

            if current_guard not in guard_table:
                guard_table[current_guard] = [0]*60

            is_awake = True

        if code=='falls' and is_awake:
            is_awake = False
            sleep_start = time_min

        if code=='wakes' and not is_awake:
            is_awake = True

            for i in range(sleep_start,time_min):
                guard_table[current_guard][i]+=1

            sleep_start = None
        

    max_time_total = 0
    result1 = None

    max_time_minute = 0
    result2 = None

    for guard in guard_table:
        total_time_slept = np.sum(guard_table[guard])
        max_minute = np.argmax(guard_table[guard])
        largest_minute =  guard_table[guard][max_minute]

        if total_time_slept>max_time_total:
            max_time_total = total_time_slept
            result1 = max_minute*guard

        if largest_minute>max_time_minute:
            max_time_minute = largest_minute
            result2 = max_minute*guard


    print(result1)
    print(result2)


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

