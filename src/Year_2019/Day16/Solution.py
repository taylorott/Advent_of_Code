#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    data = data[0][0]

    num_list = []

    for q in data:
        num_list.append(int(q))

    return num_list

def compute_element(input_list,n):
    n+=1
    base_pattern = [0]*n + [1]*n + [0]*n + [-1]*n

    total = 0
    for i in range(len(input_list)):
        j = (i+1)%len(base_pattern)
        total+=input_list[i]*base_pattern[j]

    total = int(abs(total))%10

    return total

def update_pattern(input_list):
    new_pattern = []
    for i in range(len(input_list)):
        new_pattern.append(compute_element(input_list,i))
    return new_pattern

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    current_pattern = data

    for i in range(100):
        # print(current_pattern)
        current_pattern = update_pattern(current_pattern)

    q = 0

    for i in range(8):
        q*=10
        q+=current_pattern[i]
    print(q)


def update_pattern2(input_list):
    new_pattern = [0]*len(input_list)

    total = 0

    for i in range(len(input_list)-1,-1,-1):
        total+=input_list[i]
        new_pattern[i]=total%10

    return new_pattern

    
def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'


    data = parse_input01(fname)

    num_to_skip = 0

    for i in range(7):
        num_to_skip*=10
        num_to_skip+=data[i]


    num_remaining = (10**4)*len(data) - num_to_skip


    current_pattern = int(np.floor(num_remaining/len(data)))*data

    current_pattern = data[(len(data)-num_remaining+len(current_pattern)):] +current_pattern

    for i in range(100):
        current_pattern = update_pattern2(current_pattern)

    q = 0

    for i in range(8):
        q*=10
        q+=current_pattern[i]
    print(q)

if __name__ == '__main__':
    solution01()
    solution02()
    

