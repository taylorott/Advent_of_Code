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
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    for line in data:
        if len(line)==2:
            line[1] = int(line[1])

    return data


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    x = 1

    strength_list = []
    for line in data:
        command = line[0]

        strength_list.append(x)

        if command=='addx':
            strength_list.append(x)

            x+=line[1]
            
    cycle_list = [20,60,100,140,180,220]

    total=0
    for cycle in cycle_list:
        i = cycle-1
        if i<len(strength_list):
            total+=cycle*strength_list[i]

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    x = 1

    strength_list = []
    for line in data:
        command = line[0]

        strength_list.append(x)

        if command=='addx':
            strength_list.append(x)

            x+=line[1]

    my_mat = []
    for i in range(6):
        my_mat.append(['.']*40)

    for i in range(len(strength_list)):
        row = i//40
        col = i%40
        if abs(strength_list[i]-col)<=1:
            my_mat[row][col]='#'

    for i in range(6):
        str_out = ''
        for j in range(40):
            str_out+=my_mat[i][j]

        print(str_out)

if __name__ == '__main__':
    solution01()
    solution02()
    

