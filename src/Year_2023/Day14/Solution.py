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
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def print_grid(grid_in):
    for row in grid_in:
        row_str = ''
        for grid_char in row:
            row_str+=grid_char
        print(row_str)

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

def slide_south(grid_in):
    for j in range(len(grid_in[0])):
        count1=len(grid_in)-1
        count2=len(grid_in)-1
        while count1>=0:
            while count1>=0 and grid_in[count1][j]!='.':
                count1-=1

            count2=count1
            while count2>=0 and grid_in[count2][j]!='#':
                if grid_in[count2][j]=='O':
                    grid_in[count2][j]='.'
                    grid_in[count1][j]='O'
                    count1-=1
                count2-=1

            count1-=1

def slide_west(grid_in):
    for i in range(len(grid_in)):
        count1=0
        count2=0
        while count1<len(grid_in[0]):
            while count1<len(grid_in[0]) and grid_in[i][count1]!='.':
                count1+=1

            count2=count1
            while count2<len(grid_in[0]) and grid_in[i][count2]!='#':
                if grid_in[i][count2]=='O':
                    grid_in[i][count2]='.'
                    grid_in[i][count1]='O'
                    count1+=1
                count2+=1

            count1+=1

def slide_east(grid_in):
    for i in range(len(grid_in)):
        count1=len(grid_in[0])-1
        count2=len(grid_in[0])-1
        while count1>=0:
            while count1>=0 and grid_in[i][count1]!='.':
                count1-=1

            count2=count1
            while count2>=0 and grid_in[i][count2]!='#':
                if grid_in[i][count2]=='O':
                    grid_in[i][count2]='.'
                    grid_in[i][count1]='O'
                    count1-=1
                count2-=1

            count1-=1

def execute_cycle(grid_in):
    slide_north(grid_in)
    slide_west(grid_in)
    slide_south(grid_in)
    slide_east(grid_in)

def serialize_state(grid_in):
    str_out = ''
    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            str_out+=grid_in[i][j]
    return str_out


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    slide_north(data)
    print(eval_score(data))


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    current_str = serialize_state(data)
    current_score = eval_score(data)
    state_dict= {}
    score_lookup = {}
    count = 0

    while current_str not in state_dict:
        state_dict[current_str]=count
        score_lookup[count]=current_score

        execute_cycle(data)
        current_str = serialize_state(data)
        current_score = eval_score(data)
        count+=1

    offset = state_dict[current_str]
    period = count-offset
    num_cycles = 1000000000-offset
    lookup_index = offset+num_cycles%period

    print(score_lookup[lookup_index])


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

