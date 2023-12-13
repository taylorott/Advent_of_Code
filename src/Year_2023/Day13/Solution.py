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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [''],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def generate_row_strings(mat_in):
    row_list = []
    for i in range(len(mat_in)):
        temp_str = ''
        for j in range(len(mat_in[0])):
            temp_str+=mat_in[i][j]
        row_list.append(temp_str)
    return row_list

def generate_col_strings(mat_in):
    col_list = []
    for j in range(len(mat_in[0])):
        temp_str = ''
        for i in range(len(mat_in)):
            temp_str+=mat_in[i][j]
        col_list.append(temp_str)
    return col_list

def compare_strings(str1,str2):
    total = 0
    for i in range(len(str1)):
        if str1[i]!=str2[i]:
            total+=1
    return total

def find_mirror(str_list,target_diff_val=0):
    for i in range(len(str_list)-1):
        count1 = i
        count2 = i+1
        total_diff = 0
        while 0<=count1 and count2<len(str_list) and total_diff<=target_diff_val:
            total_diff+=compare_strings(str_list[count1],str_list[count2])
            count1-=1
            count2+=1
        if total_diff==target_diff_val:
            return i+1
    return None

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total  = 0
    for item in data:
        row_list = generate_row_strings(item)
        col_list = generate_col_strings(item)

        vertical_line_mirror = find_mirror(col_list)
        horizontal_line_mirror = find_mirror(row_list)

        if vertical_line_mirror is not None:
            total += vertical_line_mirror
        if horizontal_line_mirror is not None:
            total += 100*horizontal_line_mirror
    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total  = 0
    for item in data:
        row_list = generate_row_strings(item)
        col_list = generate_col_strings(item)

        vertical_line_mirror = find_mirror(col_list,1)
        horizontal_line_mirror = find_mirror(row_list,1)

        if vertical_line_mirror is not None:
            total += vertical_line_mirror
        if horizontal_line_mirror is not None:
            total += 100*horizontal_line_mirror
    print(total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

