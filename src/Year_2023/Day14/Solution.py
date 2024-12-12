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
    return bh.parse_char_grid(path,fname)

def eval_score(grid_in):
    score = 0
    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if grid_in[i][j]=='O':
                score+=len(grid_in)-i
    return score       

def slide_north(grid_in):
    for j in range(len(grid_in[0])):
        count1=0
        count2=0
        while count1<len(grid_in):
            while count1<len(grid_in) and grid_in[count1][j]!='.':
                count1+=1

            count2=count1
            while count2<len(grid_in) and grid_in[count2][j]!='#':
                if grid_in[count2][j]=='O':
                    grid_in[count2][j]='.'
                    grid_in[count1][j]='O'
                    count1+=1
                count2+=1

            count1+=1

def execute_cycle(grid_in):
    for i in range(4):
        slide_north(grid_in)
        grid_in = bh.rotate_grid(grid_in,-1)

    return grid_in

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    slide_north(data)
    result = eval_score(data)

    if show_result: print(result)

    return result

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    current_str = str(data)
    current_score = eval_score(data)
    state_dict= {}
    score_lookup = {}
    count = 0

    while current_str not in state_dict:
        state_dict[current_str]=count
        score_lookup[count]=current_score

        data = execute_cycle(data)
        current_str = str(data)
        current_score = eval_score(data)
        count+=1

    offset = state_dict[current_str]
    period = count-offset
    num_cycles = 1000000000-offset
    lookup_index = offset+num_cycles%period

    result = score_lookup[lookup_index]

    if show_result: print(result)

    return result

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

