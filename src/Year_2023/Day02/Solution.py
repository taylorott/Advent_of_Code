#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [':',';'],type_lookup = None, allInt = False, allFloat = False)

    data_out = []
    for i in range(len(data)):
        current_line = data[i]

        game = []
        for j in range(1,len(current_line)):
            item = current_line[j]
            
            item = item.replace(',',' ')
            split_list = item.split(' ')
            reduced_list = []
            for temp in split_list:
                if temp != '':
                    reduced_list.append(temp)
            
            current_dict = {'red':0,'blue':0,'green':0}

            for k in range(len(reduced_list)//2):
                current_dict[reduced_list[2*k+1]]=int(reduced_list[2*k])
            game.append(current_dict)

        data_out.append(game)
            
    return data_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    max_dict = {'red':12,'green':13,'blue':14}

    data = parse_input01(fname)

    total = 0
    for i in range(len(data)):
        game = data[i]
        game_id = i+1

        is_possible = True

        for current_round in game:
            for key in current_round:
                if current_round[key]>max_dict[key]:
                    is_possible = False

        if is_possible:
            total+=game_id
            
    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for i in range(len(data)):
        game = data[i]
        game_id = i+1

        max_dict = {'red':0,'green':0,'blue':0}

        for current_round in game:
            for key in current_round:
                max_dict[key] = max(max_dict[key],current_round[key])
                    
        power = 1

        for key in max_dict:
            power*=max_dict[key]

        total+=power

    print(total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

