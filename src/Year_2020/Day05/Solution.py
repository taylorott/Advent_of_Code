#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import Helpers.basic_helpers as bh

path = '/home/taylorott/Documents/Advent_of_Code/src/Year_2020/Day05'

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = bh.parse_strings(path,fname)

    ID_list = []
    for item in data:
        row_str = item[0:7]

        row_min = 0
        row_max = 127

        row_mid = (row_min+row_max)//2
        for my_char in row_str:
            if my_char == 'F':
                row_mid = (row_min+row_max)//2
                row_max = row_mid
            elif my_char == 'B':
                row_mid = 1+(row_min+row_max)//2
                row_min = row_mid

        col_str = item[7:10]

        col_min = 0
        col_max = 7

        col_mid = (col_min+col_max)//2
        for my_char in col_str:
            if my_char == 'L':
                col_mid = (col_min+col_max)//2
                col_max = col_mid
            elif my_char == 'R':
                col_mid = 1+(col_min+col_max)//2
                col_min = col_mid
        ID = row_mid*8+col_mid
        ID_list.append(ID)
        # print('row: '+str(row_mid)+' col: '+str(col_mid)+' ID: '+str(ID))
    print(max(ID_list))

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = bh.parse_strings(path,fname)

    ID_dict = {}
    for item in data:
        row_str = item[0:7]

        row_min = 0
        row_max = 127

        row_mid = (row_min+row_max)//2
        for my_char in row_str:
            if my_char == 'F':
                row_mid = (row_min+row_max)//2
                row_max = row_mid
            elif my_char == 'B':
                row_mid = 1+(row_min+row_max)//2
                row_min = row_mid

        col_str = item[7:10]

        col_min = 0
        col_max = 7

        col_mid = (col_min+col_max)//2
        for my_char in col_str:
            if my_char == 'L':
                col_mid = (col_min+col_max)//2
                col_max = col_mid
            elif my_char == 'R':
                col_mid = 1+(col_min+col_max)//2
                col_min = col_mid
        ID = row_mid*8+col_mid
        ID_dict[ID] = None

    for i in range(128*8):
        if i not in ID_dict and i-1 in ID_dict and i+1 in ID_dict:
            print(i)




if __name__ == '__main__':
    solution01()
    solution02()
    

