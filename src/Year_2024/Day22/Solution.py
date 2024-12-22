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
    return bh.parse_num_column(path,fname)

def mix_then_prune(val,secret): return (val^secret)%16777216

def update_secret(secret):
    secret = mix_then_prune(secret*64,secret)
    secret = mix_then_prune(secret//32,secret)
    secret = mix_then_prune(secret*2048,secret)
    return secret

def run_sequence(a,total_dict):
    visited = set()
    sequence=deque()

    for i in range(2000):
        b = update_secret(a)
        sequence.append((b%10)-(a%10))
        while len(sequence)>4:
            sequence.popleft()
        if len(sequence)==4:
            key = tuple(sequence)
            if key not in visited:
                visited.add(key)
                if key not in total_dict: total_dict[key]=(b%10)
                else: total_dict[key]+=(b%10)
        a = b
    return b

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    total, max_val, total_dict = 0, 0, dict()
    for item in data:
        total+=run_sequence(item,total_dict)
    for key in total_dict: max_val = max(max_val,total_dict[key])

    if show_result: print(str(total)+'\n'+str(max_val))

    return total, max_val

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

