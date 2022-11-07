#!/usr/bin/env python
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import Helpers.basic_helpers as bh

path = '/home/taylorott/Documents/Advent_of_Code/src/Year_2020/Day01'

def solution01():
    fname = 'Input01.txt'

    num_list = bh.parse_num_column(path,fname)

    num_dict = {}

    for num in num_list:
        if 2020-num in num_dict:
            result = num*(2020-num)
            print(result)
        num_dict[num] = None 

def solution02():
    fname = 'Input01.txt'

    num_list = bh.parse_num_column(path,fname)

    num_dict = {}

    for i in range(len(num_list)):
        num = num_list[i]

        if num in num_dict:
            num_dict[num].append(i)
        else:
            num_dict[num] = [i]

    for i in range(len(num_list)):
        num1 = num_list[i]
        for j in range(i):
            num2 = num_list[j]

            temp_val = 2020-num1-num2
            if temp_val in num_dict:
                for k in num_dict[temp_val]:
                    if k!=i and k!=j:
                        print(num1*num2*temp_val)
                        return None

if __name__ == '__main__':
    solution01()
    solution02()
    

