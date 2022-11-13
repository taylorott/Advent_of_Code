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

    data = parse_input01(fname)

    total = 0

    for item in data:
        total+=(item//3)-2

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0

    for item in data:
        num_to_add = (item//3)-2

        while num_to_add>0:
            total+=num_to_add
            num_to_add = (num_to_add//3)-2 

    print(total)


if __name__ == '__main__':
    solution01()
    solution02()
    

