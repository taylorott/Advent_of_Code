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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = ['#','@',',',':','x',' '],type_lookup = None, allInt = True, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)[0]
    
    my_table = frequency_table()

    for item in data:
        x0 = item[1]
        y0 = item[2]
        dx = item[3]
        dy = item[4]

        for x in range(x0,x0+dx):
            for y in range(y0,y0+dy):
                coord_tuple = (x,y)
                my_table.add_item(coord_tuple)


    total = 0

    for item in my_table.keys():
        if my_table[item]>=2:
            total+=1

    print(total)

    #part 2
    for item in data:
        x0 = item[1]
        y0 = item[2]
        dx = item[3]
        dy = item[4]

        is_good = True

        for x in range(x0,x0+dx):
            for y in range(y0,y0+dy):
                coord_tuple = (x,y)
                
                is_good &= my_table[coord_tuple]==1

        if is_good:
            print(item[0])
            break

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)[0]
    
 



if __name__ == '__main__':
    t0 = time.time()
    solution01()
    # solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

