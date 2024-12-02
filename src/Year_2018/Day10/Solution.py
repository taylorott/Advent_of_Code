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
    data = bh.parse_strings(path,fname,delimiters = [' ',',','<','>','=','position','velocity'],type_lookup = None, allInt = True, allFloat = False)

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    coords = parse_input01(fname)

    num_coords = len(coords)

    coords = np.array(np.transpose(coords))

    index_min = np.argmin(coords[1])
    index_max = np.argmax(coords[1])
    
    min_y = coords[1][index_min]
    vy_minus = coords[3][index_min]

    max_y = coords[1][index_max]
    vy_plus = coords[3][index_max]

    delta_desired = max(0,(max_y-min_y-100))
    delta_t = delta_desired//(vy_minus-vy_plus)

    coords[0]+=coords[2]*delta_t
    coords[1]+=coords[3]*delta_t

    while max(coords[1]+coords[3])-min(coords[1]+coords[3])<max(coords[1])-min(coords[1]):
        delta_t+=1        
        coords[0]+=coords[2]
        coords[1]+=coords[3]

    min_x = min(coords[0])
    max_x = max(coords[0])
    min_y = min(coords[1])
    max_y = max(coords[1])

    char_matrix = []

    for i in range(max_y-min_y+1):
        char_matrix.append(['.']*(max_x-min_x+1))

    for i in range(num_coords):
        x = coords[0][i]-min_x
        y = coords[1][i]-min_y

        char_matrix[y][x]='#'

    bh.print_char_matrix(char_matrix)
    print(delta_t)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

