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
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = bh.parse_strings(path,fname,delimiters = [',','\(','\)',' ','='],type_lookup = None, allInt = False, allFloat = False)

    return data[0][0], data[2:len(data)]

def build_move_dict(edge_list):
    move_dict = {}

    for item in edge_list:
        move_dict[item[0]]={'L':item[1],'R':item[2]}

    return move_dict

def solution01(show_result=True, fname='Input02.txt'):
    move_string, edge_list = parse_input01(fname)

    move_dict = build_move_dict(edge_list)

    current_node = 'AAA'
    count = 0
    while current_node!='ZZZ':
        move_char = move_string[count%len(move_string)]
        current_node = move_dict[current_node][move_char]
        count+=1

    if show_result: print(count)

    return count

def solution02(show_result=True, fname='Input02.txt'):
    move_string, edge_list = parse_input01(fname)

    move_dict = build_move_dict(edge_list)

    num_vertices = len(move_dict)
    sequence_len = len(move_string)

    state_list = []
    for item in move_dict:
        if item[-1]=='A':
            state_list.append(item)

    start_state_list = list(state_list)

    period_dict = {}

    max_period = num_vertices*sequence_len+1
    for i in range(max_period):
        move_char = move_string[i%sequence_len]
        for j in range(len(state_list)):
            state_list[j] = move_dict[state_list[j]][move_char]
            if state_list[j][-1]=='Z' and start_state_list[j] not in period_dict:
                period_dict[start_state_list[j]] = i+1

    total = 1

    for start_state in start_state_list:
        total = lcm(total,period_dict[start_state])

    if show_result: print(total)
    
    return total
                

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

