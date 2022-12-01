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


    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    max_cal = 0
    for cal_list in data:
        total = 0
        for item in cal_list:
            total+=int(item)
        max_cal = max(max_cal,total)

    print(max_cal)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    cal_total_list = []
    for cal_list in data:
        total = 0
        for item in cal_list:
            total+=int(item)
        cal_total_list.append(total)

    cal_total_list.sort(reverse=True)
    print(sum(cal_total_list[:3]))

if __name__ == '__main__':
    solution01()
    solution02()
    

