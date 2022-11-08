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
    # num_list = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    tile_list = []
    tile_ids = []
    for full_tile in data:
        tile_num = int(full_tile[0].split(' ')[1][0:-1])
        tile_map = full_tile[1:]
        tile_ids.append(tile_num)
        tile_list.append(tile_map)
    return tile_list,tile_ids

def extract_border_codes(tile):
    top_str = tile[0]
    bot_str = tile[-1]
    left_str = ''
    right_str = ''

    for tile_str in tile:
        left_str+=tile_str[0]
        right_str+=tile_str[-1]

    return {top_str:1,bot_str:3,left_str:2,right_str:0}



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    tile_list,tile_ids = parse_input01(fname)


    border_dict_fwd = {}
    border_dict_rev = {}
    border_label_dict = {}

    for i in range(len(tile_list)):
        str_dict = extract_border_codes(tile_list[i])

        border_dict_fwd[tile_ids[i]] = str_dict

        for key in str_dict.keys():
            if key not in border_dict_rev:
                border_dict_rev[key] = {}
                border_label_dict[key] = []
            if key[::-1] not in border_dict_rev:
                border_dict_rev[key[::-1]] = {}
                border_label_dict[key[::-1]] = []

            border_dict_rev[key][tile_ids[i]]=None
            border_dict_rev[key[::-1]][tile_ids[i]]=None

            border_label_dict[key].append([tile_ids[i],str_dict[key],1])

    # print(border_dict_fwd)
    # print(border_dict_rev)
    prod = 1
    for i in range(len(tile_list)):
        count = 0
        # print(border_dict_fwd[tile_ids[i]])
        for key in border_dict_fwd[tile_ids[i]]:
            # print(key)
            # print(border_dict_rev[key].keys())
            if len(border_dict_rev[key].keys())==1:
                count+=1
        if count==2:
            # print(tile_ids[i])
            prod*=tile_ids[i]

    print(prod)

            
    

    # print(tile_list[0])

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # parse_input01(fname)

if __name__ == '__main__':
    solution01()
    solution02()
    

