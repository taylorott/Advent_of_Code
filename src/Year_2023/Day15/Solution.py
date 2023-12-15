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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [' ',','],type_lookup = None, allInt = False, allFloat = False)

    return data

def run_hash(str_in):
    current_val = 0
    for my_char in str_in:
        current_val+=ord(my_char)
        current_val*=17
        current_val%=256
    return current_val

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    # print(data)
    total = 0

    for item in data:
        for my_str in item:
            total+=run_hash(my_str)
    print(total)

def parse_string(str_in):

    count=0
    while str_in[count]!='-' and str_in[count]!='=':
        count+=1

    label = str_in[:count]
    box_num = run_hash(label)
    command = str_in[count]
    focal_length = None

    if str_in[count]=='=':
        focal_length = int(str_in[count+1:])

    return label,box_num,command,focal_length

def execute_command(box_list,str_in):
    label,box_num,command,focal_length = parse_string(str_in)

    current_box = box_list[box_num]
    if command=='-':
        count=0
        while count<len(current_box) and current_box[count][0]!=label:
            count+=1
        if count<len(current_box):
            current_box.pop(count)
    elif command=='=':
        count=0
        while count<len(current_box) and current_box[count][0]!=label:
            count+=1
        if count<len(current_box):
            current_box[count][1]=focal_length
        else:
            current_box.append([label,focal_length])

def eval_box_score(box_list):
    total = 0
    for i in range(len(box_list)):
        current_box = box_list[i]
        for j in range(len(current_box)):
            total+=(i+1)*(j+1)*current_box[j][1]
    return total

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    box_list = []
    for i in range(256):
        box_list.append([])
    

    for item in data:
        for my_str in item:
            execute_command(box_list,my_str)

    score_out = eval_box_score(box_list)
    print(score_out)
    

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

