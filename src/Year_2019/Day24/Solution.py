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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [','],type_lookup = None, allInt = False, allFloat = False)

    return data

dir_list = [[1,0],[-1,0],[0,1],[0,-1]]

def count_adjacent(grid_in,i,j):
    total = 0
    for direction in dir_list:
        i_temp = i+direction[0]
        j_temp = j+direction[1]

        if 0<=i_temp and i_temp<len(grid_in) and 0<=j_temp and j_temp<len(grid_in[0]) and grid_in[i_temp][j_temp]=='#':
            total+=1

    return total

def update_grid(grid_in):
    new_grid = []

    for i in range(len(grid_in)):
        new_grid.append([None]*len(grid_in[0]))

        for j in range(len(grid_in[0])):
            num_adjacent = count_adjacent(grid_in,i,j)
            if (grid_in[i][j]=='#' and num_adjacent!=1) or (grid_in[i][j]=='.' and (num_adjacent!=1 and num_adjacent!=2)):
                new_grid[i][j]='.'
            else:
                new_grid[i][j]='#'
    return new_grid

def grid_to_str(grid_in):
    str_out = ''

    for line in grid_in:
        for item in line:
            str_out+=item

    return str_out

def eval_score(grid_in):
    total = 0
    a = 1
    for line in grid_in:
        for item in line:
            if item=='#':
                total+=a
            a*=2
    return total

def enumerate_adjacent_tiles(coord_in):
    i = coord_in[0]
    j = coord_in[1]
    k = coord_in[2]

    neighbor_list = []
    for direction in dir_list:
        i_temp = i+direction[0]
        j_temp = j+direction[1]


        if i_temp<0:
            neighbor_list.append((1,2,k-1))
        elif i_temp==5:
            neighbor_list.append((3,2,k-1))
        elif j_temp<0:
            neighbor_list.append((2,1,k-1))
        elif j_temp==5:
            neighbor_list.append((2,3,k-1))
        elif i_temp==2 and j_temp==2:
            if i==1:
                for m in range(5):
                    neighbor_list.append((0,m,k+1))
            elif i==3:
                for m in range(5):
                    neighbor_list.append((4,m,k+1))
            elif j==1:
                for m in range(5):
                    neighbor_list.append((m,0,k+1))
            elif j==3:
                for m in range(5):
                    neighbor_list.append((m,4,k+1))
        else:
            neighbor_list.append((i_temp,j_temp,k))

    if len(neighbor_list)!=4 and len(neighbor_list)!=8:
        print(len(neighbor_list))
    return neighbor_list

def count_adjacent_using_dict(dict_in,key_in):
    neighbor_list = enumerate_adjacent_tiles(key_in)

    total = 0
    for neighbor in neighbor_list:
        if neighbor in dict_in and dict_in[neighbor]=='#':
            total+=1

    return total

def update_dict(dict_in):
    relevant_tiles = {}

    for key in dict_in.keys():
        relevant_tiles[key] = None
        neighbor_list = enumerate_adjacent_tiles(key)

        for neighbor in neighbor_list:
            relevant_tiles[neighbor]=None

    new_dict = {}

    for key in relevant_tiles:
        num_adjacent = count_adjacent_using_dict(dict_in,key)

        condition1 = key in dict_in and dict_in[key]=='#' and num_adjacent==1
        condition2 = (key not in dict_in or dict_in[key]=='.') and (num_adjacent==1 or num_adjacent==2)

        if condition1 or condition2:
            new_dict[key]='#'

    return new_dict

def grid_to_dict(grid_in):
    dict_out = {}
    for i in range(len(grid_in)):
        for j in range(len(grid_in)):
            if (i!=2 or j!=2)  and grid_in[i][j]=='#':
                dict_out[(i,j,0)]='#'
    return dict_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    visited_set={}

    while grid_to_str(data) not in visited_set:
        visited_set[grid_to_str(data)]=None
        data = update_grid(data)

    score = eval_score(data)
    print(score)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    current_dict = grid_to_dict(data)

    for i in range(200):
        current_dict = update_dict(current_dict)

    count = 0

    min_k = np.inf
    max_k =-np.inf
    for key in current_dict.keys():
        min_k = min(min_k,key[2])
        max_k = max(max_k,key[2])
        if current_dict[key]=='#':
            count+=1

    print(count)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

