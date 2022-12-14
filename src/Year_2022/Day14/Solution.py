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
    data = bh.parse_strings(path,fname,delimiters = ['->'],type_lookup = None, allInt = False, allFloat = False)

    for line in data:
        for i in range(len(line)):
            item = line[i]
            pair = item.split(',')        

            line[i] = [int(pair[0]),int(pair[1])]
    return data

def build_state_dict(data):
    dict_out = {}
    for line in data:
        for i in range(len(line)-1):
            start = line[i]
            end = line[i+1]

            x = start[0]
            y = start[1]

            while x!= end[0] or y!=end[1]:
                dict_out[(x,y)]='r'
                x+=np.sign(end[0]-x)
                y+=np.sign(end[1]-y)

            dict_out[(x,y)]='r'
    return dict_out

def drop_sand_particle(state_dict,y_max,include_floor = False):
    x_sand = 500
    y_sand = 0

    can_continue = True

    if include_floor:
        y_max+=1

    while can_continue and y_sand<y_max:
        if (x_sand,y_sand+1) not in state_dict:
            y_sand+=1

        elif (x_sand-1,y_sand+1) not in state_dict:
            x_sand-=1
            y_sand+=1
        elif (x_sand+1,y_sand+1) not in state_dict:
            x_sand+=1
            y_sand+=1
        else:
            can_continue = False
            state_dict[(x_sand,y_sand)]='s'

    if include_floor:
        state_dict[(x_sand,y_sand)]='s'

    return (include_floor and y_sand!=0) or (not include_floor and y_sand!=y_max)


def fill_with_sand(state_dict,include_floor = False):

    y_max = 0

    for key in state_dict.keys():
        y_max = max(y_max,key[1])

    while drop_sand_particle(state_dict,y_max,include_floor=include_floor): continue

    count=0
    for key in state_dict.keys():
        if state_dict[key]=='s':
            count+=1

    print(count)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    state_dict = build_state_dict(data)
    fill_with_sand(state_dict)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    state_dict = build_state_dict(data)
    fill_with_sand(state_dict,True)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

