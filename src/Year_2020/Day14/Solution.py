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

def read_mask01(mask_in):
    on_num = 0
    off_num = (1<<36)-1
    for i in range(36):
        if mask_in[i]=='0':
            off_num-=1<<(35-i)
        elif mask_in[i]=='1':
            on_num+=1<<(35-i)
    return on_num,off_num

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[' = ',r'\[',r'\]','mask','mem'])

    on_num,off_num = 0,0
    index_list = []
    memory_dict = {}

    for line in data:
        if len(line)==1:
            on_num,off_num = read_mask01(line[0])

        else:
            key = int(line[0])
            val = int(line[1])
            val = (val|on_num)&off_num
            if key not in memory_dict:
                index_list.append(key)
            memory_dict[key]=val

    total = 0
    for key in index_list:
        total+=memory_dict[key]

    print(total)

def read_mask02(mask_in):
    on_num = 0
    off_num = (1<<36)-1

    item_list = np.array([0])
    for i in range(36):
        if mask_in[i]=='X':
            item_list = np.array(item_list.tolist() + (item_list+(1<<(35-i)) ).tolist())
            off_num-=1<<(35-i)
        elif mask_in[i]=='1':
            on_num+=1<<(35-i)
    
    return on_num,off_num,item_list


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    # fname = 'Input03.txt'

    data = bh.parse_strings(path,fname,[' = ',r'\[',r'\]','mask','mem'])

    on_num,off_num = 0,0
    index_list = []
    memory_dict = {}

    on_num,off_num = 0,0
    for line in data:
        if len(line)==1:
            on_num,off_num,add_list = read_mask02(line[0])
        else:
            key = int(line[0])
            val = int(line[1])
            key = (key|on_num)&off_num
            key_list = key+add_list

            for index in key_list:
                if int(index) not in memory_dict:
                    index_list.append(int(index))
                memory_dict[int(index)]=val

    total = 0
    for key in index_list:
        total+=memory_dict[key]

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

