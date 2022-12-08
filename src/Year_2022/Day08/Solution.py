#!/usr/bin/env python
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph, frequency_table
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False)

    grid_out = []

    for line in data:
        row_out = []
        for item in line:
            row_out.append(int(item))
        grid_out.append(row_out)

    return grid_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    is_visible = []

    for row in data:
        is_visible.append([False]*len(row))

    l1 = len(data)
    l2 = len(data[0])

    for i in range(l1):
        max_height_left = -1
        max_height_right = -1

        for j in range(l2):
            if data[i][j]>max_height_left:
                max_height_left = data[i][j]
                is_visible[i][j]=True
            if data[i][l2-j-1]>max_height_right:
                max_height_right = data[i][l2-j-1]
                is_visible[i][l2-j-1] = True

    for j in range(l2):
        max_height_top = -1
        max_height_bottom = -1

        for i in range(l1):
            if data[i][j]>max_height_top:
                max_height_top = data[i][j]
                is_visible[i][j]=True
            if data[l1-i-1][j]>max_height_bottom:
                max_height_bottom = data[l1-i-1][j]
                is_visible[l1-i-1][j]= True

    count = 0

    for i in range(l1):
        for j in range(l2):
            if is_visible[i][j]:
                count+=1


    print(count)

def compute_tree_score(grid_in,i,j):
    i_top = i-1
    i_bot = i+1
    j_left = j-1
    j_right = j+1

    while i_top>0 and grid_in[i_top][j]<grid_in[i][j]:
        i_top-=1

    while i_bot<len(grid_in)-1 and grid_in[i_bot][j]<grid_in[i][j]:
        i_bot+=1

    while j_left>0 and grid_in[i][j_left]<grid_in[i][j]:
        j_left-=1

    while j_right<len(grid_in[0])-1 and grid_in[i][j_right]<grid_in[i][j]:
        j_right+=1

    return (i-i_top)*(i_bot-i)*(j-j_left)*(j_right-j)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    max_val = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            max_val = max(max_val,compute_tree_score(data,i,j))
    print(max_val)

if __name__ == '__main__':
    solution01()
    solution02()
    

