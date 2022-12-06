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
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False)

    return data[0][0]

def find_first_substring_unique_chars(str_in,substr_len):

    freq_table = frequency_table()
    for i in range(len(str_in)):
        char_in = str_in[i]

        freq_table.add_item(char_in)

        if i>=substr_len:
            char_out = str_in[i-substr_len]
            freq_table.remove_item(char_out)

        if i>=substr_len-1 and freq_table.max_frequency()==1:
            print(i+1)
            break

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    a = 4

    data = parse_input01(fname)
    find_first_substring_unique_chars(data,a)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    a = 14

    data = parse_input01(fname)

    data = parse_input01(fname)
    find_first_substring_unique_chars(data,a)

if __name__ == '__main__':
    solution01()
    solution02()
    

