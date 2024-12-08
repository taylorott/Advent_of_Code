#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
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

    obstacle_set = set()
    elf_heap = AugmentedHeap()
    goblin_heap = AugmentedHeap()

    for i in range(len(data)):
        for j in range(len(data)):
            coord = (i,j)
            if data[i][j]=='#': obstacle_set.add(coord)
            if data[i][j]=='E': elf_set.add(coord)
            if data[i][j]=='G': goblin_set.add(coord)


    return obstacle_set, elf_set, goblin_set


def is_adjacent(coord1,coord2):
    test1 =  coord2[0]-coord1[0] == 0 and abs(coord2[1]-coord1[1])==1
    test2 =  abs(coord2[0]-coord1[0])==1 and coord2[1]-coord1[1] == 0
    return test1 or test2

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    grid = parse_input01(fname)
    

    bh.print_char_matrix(grid)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

