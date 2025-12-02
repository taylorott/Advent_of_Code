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
    data = bh.parse_strings(path,fname,delimiters = [',','-'],type_lookup = None, allInt = True, allFloat = False)[0]
  
    int_list1, int_list2 = [], []
    for i in range(len(data)//2):
        int_list1.append(data[i*2])
        int_list2.append(data[i*2+1])

    return int_list1, int_list2

def is_invalid_k(id_str,k):
    l = len(id_str)

    if l%k!=0: 
        return False

    l_sub = l//k

    base = id_str[0:l_sub]

    for i in range(k):
        if id_str[(i*l_sub):((i+1)*l_sub)]!=base: 
            return False

    return True


def solution(show_result=True, fname='Input02.txt'):

    int_list1, int_list2 = parse_input01(fname)
    
    total1, total2 = 0, 0
    for i in range(len(int_list1)):
        for j in range(int_list1[i],int_list2[i]+1):
            id_str = str(j)

            if is_invalid_k(id_str,2): total1+=j

            for k in range(2,len(str(j))+1):
                if is_invalid_k(id_str,k): 
                    total2+=j
                    break
    if show_result:
        print(total1)
        print(total2)

    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

