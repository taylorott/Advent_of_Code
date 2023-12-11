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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def is_row_empty(grid_in,row_num):
    for i in range(len(grid_in[row_num])):
        if grid_in[row_num][i]=='#':
            return False
    return True

def is_col_empty(grid_in,col_num):
    for i in range(len(grid_in)):
        if grid_in[i][col_num]=='#':
            return False
    return True 

def get_empty_rows_and_cols(grid_in):
    row_list = []
    col_list = []

    for i in range(len(grid_in)):
        if is_row_empty(grid_in,i):
            row_list.append(i)

    for i in range(len(grid_in[0])):
        if is_col_empty(grid_in,i):
            col_list.append(i)

    return row_list,col_list

def find_galaxies(grid_in):
    galaxy_list = []
    for i in range(len(grid_in)):
        for j in range(len(grid_in[i])):
            if grid_in[i][j]=='#':
                galaxy_list.append((i,j))
    return galaxy_list

def manhattan_distance(coord1,coord2):
    return abs(coord1[0]-coord2[0])+abs(coord1[1]-coord2[1])

#returns True is b is strictly inbetweeen a and c, false otherwise
def is_inbetween(a,b,c):
    return (a<b and b<c) or (a>b and b>c)

def galaxy_dist(coord1,coord2,row_list,col_list,multiplier):
    base_dist = manhattan_distance(coord1,coord2)

    for row_num in row_list:
        if is_inbetween(coord1[0],row_num,coord2[0]):
            base_dist+=multiplier-1

    for col_num in col_list:
        if is_inbetween(coord1[1],col_num,coord2[1]):
            base_dist+=multiplier-1

    return base_dist

def get_pairwise_distances(grid_in,multiplier):
    row_list,col_list = get_empty_rows_and_cols(grid_in)

    galaxy_list = find_galaxies(grid_in)

    total=0
    for i in range(len(galaxy_list)):
        for j in range(i+1,len(galaxy_list)):
            total+=galaxy_dist(galaxy_list[i],galaxy_list[j],row_list,col_list,multiplier)
    return total

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
   
    print(get_pairwise_distances(data,2))

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    print(get_pairwise_distances(data,1000000))

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))