#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import Helpers.basic_helpers as bh

path = '/home/taylorott/Documents/Advent_of_Code/src/Year_2020/Day02'

def solution01():
    fname = 'Input01.txt'

    type_lookup = {0:'int',1:'int'}
    data = bh.parse_strings(path,fname,[' ','-',':'],type_lookup=type_lookup)

    num_valid = 0

    for item in data:
        freq_table = bh.build_char_freq_table(item[3])

        char_freq = 0

        if item[2] in freq_table:
            char_freq = freq_table[item[2]]

        if item[0]<=char_freq and char_freq<=item[1]:
            num_valid+=1

    print(num_valid)

def solution02():
    fname = 'Input01.txt'

    type_lookup = {0:'int',1:'int'}
    data = bh.parse_strings(path,fname,[' ','-',':'],type_lookup=type_lookup)

    num_valid = 0

    for item in data:
        index0 = item[0]-1
        index1 = item[1]-1
        my_char = item[2]
        my_string = item[3]

        if ((my_string[index0]==my_char and my_string[index1]!=my_char) or
            (my_string[index0]!=my_char and my_string[index1]==my_char)):

            num_valid+=1

    print(num_valid)


if __name__ == '__main__':
    solution01()
    solution02()
    

