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
    return bh.parse_extract_ints(path,fname)[0]

def update(table_in):
    table_out = dict()

    for stone in table_in:
        key1,key2  = None, None
        if stone==0:
            key1 = 1    
        else:
            if len(str(stone))%2==0:
                stone_str = str(stone)
                key1 = int(stone_str[0:(len(stone_str)//2)])
                key2 = int(stone_str[(len(stone_str)//2):])

                if key2 not in table_out: table_out[key2]=table_in[stone]
                else: table_out[key2]+=table_in[stone]
            else:
                key1 = stone*2024
        if key1 in table_out: table_out[key1]+=table_in[stone]
        else: table_out[key1]=table_in[stone]
    return table_out

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    
    table = dict()
    for item in data:
        if item in table: table[item]+=1
        else:   table[item]=1

    for i in range(25):
        table = update(table)

    total1 = 0
    for item in table: total1+=table[item]

    for i in range(50):
        table = update(table)

    total2 = 0
    for item in table: total2+=table[item]

    if show_result:
        print(total1)
        print(total2)
    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

