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
    data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    
    str_list, int_list = [], []

    for item in data:
        str_list.append(item[0])
        int_list.append(int(item[1:]))

    return str_list, int_list

def solution(show_result=True, fname='Input02.txt'):
    str_list, int_list = parse_input01(fname)

    sign_dict = {'L':-1,'R':1}
    val = 50
    count1, count2 = 0, 0
    for i in range(0,len(str_list)):
        count2+=int_list[i]//100
        int_list[i] = int_list[i]%100

        val_next = val + sign_dict[str_list[i]]*int_list[i]

        if (val_next<=0 or 100<=val_next) and val!=0: count2+=1

        val = val_next%100

        if val == 0: count1+=1

    if show_result:
        print(count1)
        print(count2)
    return count1, count2


if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

