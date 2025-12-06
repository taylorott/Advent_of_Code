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
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)
    return data

def parse_input02(fname):
    data = bh.parse_char_grid(path,fname)
    return data

def sum_list(nums):
    total = 0
    for item in nums:
        total+=int(item)
    return total

def prod_list(nums):
    total = 1
    for item in nums:
        total*=int(item)
    return total

def parse_column(grid,i):
    total, empty_column = 0, True
     
    for k in range(len(grid)-1):
        if grid[k][i]!=' ':
            total=10*total + int(grid[k][i])
            empty_column = False
            
    return empty_column, total


def solution01(show_result=True, fname='Input02.txt'):

    data = parse_input01(fname)

    height, width = len(data)-1, len(data[0])

    operator_list = data[-1]

    total = 0
    for i in range(width):
        nums = []

        for j in range(height):
            nums.append(data[j][i])

        if operator_list[i]=='+':
            total += sum_list(nums)
        if operator_list[i]=='*':
            total += prod_list(nums)

    if show_result:
        print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):

    data = parse_input02(fname)

    i = len(data[0])-1
    total = 0
    while i>=0:
        nums = []
        
        operator = None

        while i>=0:
            empty_column, temp = parse_column(data,i)

            if empty_column: 
                break
                
            nums.append(temp)
            if i<len(data[-1]) and data[-1][i]!=' ':
                operator = data[-1][i]

            i-=1

        if operator=='+':
            total += sum_list(nums)
        if operator=='*':
            total += prod_list(nums)

        i-=1

    if show_result:
        print(total)

    return total


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

