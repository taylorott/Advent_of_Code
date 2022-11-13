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
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[','],allInt=True)

    return data[0]

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    
    data[1]=12
    data[2]=2
    current_index = 0

    while data[current_index]!=99:
        if data[current_index]==1:
            data[data[current_index+3]]=data[data[current_index+2]]+data[data[current_index+1]]
        elif data[current_index]==2:
            data[data[current_index+3]]=data[data[current_index+2]]*data[data[current_index+1]]
        current_index+=4

    print(data[0])


def run_code_with_inputs(x,y,input_list):
    temp_list = list(input_list)
    temp_list[1]=x
    temp_list[2]=y

    current_index = 0
    while current_index<len(temp_list) and temp_list[current_index]!=99:
        if max(temp_list[current_index+1:current_index+4])>=len(temp_list) or min(temp_list[current_index+1:current_index+4])<0:
            return None

        if temp_list[current_index]==1:
            temp_list[temp_list[current_index+3]]=temp_list[temp_list[current_index+2]]+temp_list[temp_list[current_index+1]]
        elif temp_list[current_index]==2:
            temp_list[temp_list[current_index+3]]=temp_list[temp_list[current_index+2]]*temp_list[temp_list[current_index+1]]
        else:
            return None
        current_index+=4
    if current_index<len(temp_list) and temp_list[current_index]==99:
        return temp_list[0]
    else:
        return None


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

   

    x = 0
    while True:
        for y in range(x+1):
            # print(x,y)
            q = run_code_with_inputs(x,y,data)
            # if q is not None:
            #     print(q)
            if q==19690720:
                print(100*x+y)
                return None
        x+=1


if __name__ == '__main__':
    solution01()
    solution02()
    

