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
    # data = bh.parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False)

    return data[0][0]

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    a = 4

    data = parse_input01(fname)

    freq_table = {}
    for i in range(len(data)):
        char_in = data[i]

        if char_in in freq_table:
            freq_table[char_in]+=1
        else:
            freq_table[char_in]=1

        if i>=a:
            char_out = data[i-a]
            freq_table[char_out]-=1

        more_than_two = False

        for key in freq_table.keys():
            if freq_table[key]>1:
                more_than_two = True

        if i>=a-1 and (not more_than_two):
            print(i+1)
            break

    # print(data)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    a = 14

    data = parse_input01(fname)

    freq_table = {}
    for i in range(len(data)):
        char_in = data[i]

        if char_in in freq_table:
            freq_table[char_in]+=1
        else:
            freq_table[char_in]=1

        if i>=a:
            char_out = data[i-a]
            freq_table[char_out]-=1

        more_than_two = False

        for key in freq_table.keys():
            # print(key)
            if freq_table[key]>1:
                more_than_two = True

        if i>=a-1 and (not more_than_two):
            print(i+1)
            break

if __name__ == '__main__':
    solution01()
    solution02()
    

