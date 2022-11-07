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

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    # num_list = [0,3,6]
    num_list = [0,20,7,16,1,18,15]

    prev_spoke_dict = {}

    for i in range(len(num_list)):
        prev_spoke_dict[num_list[i]]=i+1

    current_num = num_list[-1]
    spoken_before = False
    count = len(num_list)

    next_num = None
    while count<2020:
        count+=1
        if not spoken_before:
            current_num = 0
            next_num = count-prev_spoke_dict[current_num]
            spoken_before = True
        else:
            current_num = next_num

            if current_num in prev_spoke_dict:
                next_num = count-prev_spoke_dict[current_num]
                spoken_before = True
            else:
                next_num = None
                spoken_before = False

        prev_spoke_dict[current_num] = count
    print(current_num)


def solution02():
    # num_list = [0,3,6]
    num_list = [0,20,7,16,1,18,15]

    prev_spoke_dict = {}

    for i in range(len(num_list)):
        prev_spoke_dict[num_list[i]]=i+1

    current_num = num_list[-1]
    spoken_before = False
    count = len(num_list)

    next_num = None
    while count<30000000:
        count+=1
        if not spoken_before:
            current_num = 0
            next_num = count-prev_spoke_dict[current_num]
            spoken_before = True
        else:
            current_num = next_num

            if current_num in prev_spoke_dict:
                next_num = count-prev_spoke_dict[current_num]
                spoken_before = True
            else:
                next_num = None
                num_list.append(current_num)
                spoken_before = False


        prev_spoke_dict[current_num] = count
    print(current_num)


if __name__ == '__main__':
    solution01()
    solution02()
    

