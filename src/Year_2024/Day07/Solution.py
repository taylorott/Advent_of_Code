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
    return bh.parse_strings(path,fname,delimiters = [':',' '],type_lookup = None, allInt = True, allFloat = False)

def is_correct_recursive(val,subtotal,num_list,i,p2_flag=False):
    if i==len(num_list):
        return val==subtotal

    b1 = is_correct_recursive(val,subtotal*num_list[i],num_list,i+1,p2_flag)
    b2 = is_correct_recursive(val,subtotal+num_list[i],num_list,i+1,p2_flag)
    b3 = is_correct_recursive(val,int(str(subtotal)+str(num_list[i])),num_list,i+1,p2_flag)

    return b1 or b2 or (b3 and p2_flag)

def solution01(show_result=True, fname='Input02.txt'):
    num_table = parse_input01(fname)
    
    total1, total2 = 0, 0
    for num_list in num_table:
        if is_correct_recursive(num_list[0],num_list[1],num_list,2): total1+=num_list[0]
        if is_correct_recursive(num_list[0],num_list[1],num_list,2,True): total2+=num_list[0]

    if show_result:
        print(total1)
        print(total2)
    return total1, total2

def is_correct_dynamic(num_list,p2_flag=False):
    val, subtotal_set = num_list[0], {num_list[1]}

    for i in range(2,len(num_list)):
        next_subtotal_set = set()
        num2 = num_list[i]

        for num1 in subtotal_set:
            next_subtotal_set.add(num1+num2)
            next_subtotal_set.add(num1*num2)
            if p2_flag: next_subtotal_set.add(int(str(num1)+str(num2)))

        subtotal_set = next_subtotal_set

    for num in subtotal_set:
        if num==val: return True
    return False

def solution02(show_result=True, fname='Input02.txt'):
    num_table = parse_input01(fname)

    total1, total2 = 0, 0
    for num_list in num_table:
        if is_correct_dynamic(num_list): total1+=num_list[0]
        if is_correct_dynamic(num_list,True): total2+=num_list[0]

    if show_result:
        print(total1)
        print(total2)
    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    # solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

