#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh

path = currentdir

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

if __name__ == '__main__':
    solution01()
    solution02()
    

