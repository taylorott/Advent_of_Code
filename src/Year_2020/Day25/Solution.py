#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd

path = currentdir

def parse_input01(fname):
    data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    pub_keys = parse_input01(fname)

    sub_num = 7
    mod_num = 20201227

    key1 = pub_keys[0]
    key2 = pub_keys[1]

    v = 1
    count=0

    while v!=key1:
        v*=sub_num
        v%=mod_num
        count+=1

    loop1 = count

    v = 1
    count=0

    while v!=key2:
        v*=sub_num
        v%=mod_num
        count+=1

    loop2 = count

    v = 1
    for i in range(loop2):
        v*=key1
        v%=mod_num

    print(v)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # parse_input01(fname)

if __name__ == '__main__':
    solution01()
    solution02()
    

