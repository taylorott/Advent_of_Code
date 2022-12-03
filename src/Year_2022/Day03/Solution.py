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
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False)

    return data

def char_intersection(str1,str2):
    char_dict1 = {}
    for my_char in str1:
        char_dict1[my_char] = None

    shared_char_dict = {}

    for my_char in str2:
        if my_char in char_dict1:
            shared_char_dict[my_char] = None

    shared_char_list = []

    for key in shared_char_dict.keys():
        shared_char_list.append(key)

    return shared_char_list

def find_common_char_v1(str_in):
    l_str = len(str_in)//2

    str1 = str_in[0:l_str]
    str2 = str_in[l_str:]

    return char_intersection(str1,str2)

def find_common_char_v2(str1,str2,str3):
    shared_char_list = char_intersection(str1,str2)

    str4 = ''
    for my_char in shared_char_list:
        str4+=my_char

    return char_intersection(str3,str4)

def eval_char_score(char_in):
    if ord('a')<=ord(char_in) and ord(char_in)<=ord('z'):
        return 1+ord(char_in)-ord('a')
    else:
        return 27+ord(char_in)-ord('A')

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for item in data:
        shared_char_list = find_common_char_v1(item)

        for shared_char in shared_char_list:
            total+=eval_char_score(shared_char)

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    count = 0
    while count<len(data):
        shared_char_list = find_common_char_v2(data[count],data[count+1],data[count+2])

        for shared_char in shared_char_list:
            total+=eval_char_score(shared_char)

        count+=3

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

