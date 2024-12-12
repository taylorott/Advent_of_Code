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
    return bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)


def find_start_digit(item,digit_dict,max_len):
    for i in range(len(item)):
        for j in range(i+1,min(i+max_len+1,len(item)+1)):
            key = item[i:j]
            if key in digit_dict:
                return digit_dict[key]

def find_end_digit(item,digit_dict,max_len):
    for i in range(len(item),-1,-1):
            for j in range(i-1,max(-1,i-max_len-1),-1):
                key = item[j:i]
                if key in digit_dict:
                    return digit_dict[key]

def decode_string(item,digit_dict,max_len):
    d0 = find_start_digit(item,digit_dict,max_len)
    d1 = find_end_digit(item,digit_dict,max_len)

    return d0*10+d1

def decode_list(string_list,digit_dict,max_len):
    total = 0
    for item in string_list:
        total+= decode_string(item,digit_dict,max_len)
    return total
                    

def solution01(show_result=True, fname='Input01.txt'):
    digit_dict = {  '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7,
                    '8':8,
                    '9':9}

    data = parse_input01(fname)
    total = decode_list(data,digit_dict,1)

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input01.txt'):
    digit_dict = {  '0':0,
                    '1':1,
                    '2':2,
                    '3':3,
                    '4':4,
                    '5':5,
                    '6':6,
                    '7':7,
                    '8':8,
                    '9':9,
                    'zero':0,
                    'one':1,
                    'two':2,
                    'three':3,
                    'four':4,
                    'five':5,
                    'six':6,
                    'seven':7,
                    'eight':8,
                    'nine':9}

    data = parse_input01(fname)
    total = decode_list(data,digit_dict,5)
    if show_result: print(total)
    
    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

