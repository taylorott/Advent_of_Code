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
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [' ',','],type_lookup = None, allInt = False, allFloat = False)

    spring_str_list = []
    grouping_list = []
    for item in data:
        spring_str_list.append(item[0])
        num_list = []
        for i in range(1,len(item)):
            num_list.append(int(item[i]))
        grouping_list.append(num_list)

    return spring_str_list,grouping_list

def expand_problem(spring_str,grouping):
    spring_str_out = spring_str
    for j in range(4):
        spring_str_out+='?'+spring_str

    grouping_out = []
    for j in range(5):
        grouping_out+=list(grouping)

    return spring_str_out,grouping_out

#find the number of valid spring arrangements
#method uses recursion + memoization
#spring_string is the string of '#', '.', and '?' characters describing the operational/damaged springs
#grouping is a list of integers describing the size of each contiguous group of damaged springs
#memo_dict is our memoization table
#we will be recursing on suffixes of spring_str and grouping
def num_valid_arrangements(spring_str,grouping,memo_dict):
    
    #hash the input as a tuple of its lengths
    key = (len(spring_str),len(grouping))

    #if we've already seen this input before, return the stored value
    if key in memo_dict:
        return memo_dict[key]

    #the default value in the memoization table for the current input is zero
    memo_dict[key] = 0

    #base case #1, empty spring string
    if len(spring_str)==0:
        #if there are no more spring groups, then this is a single valid arrangement. Set table to 1 and return
        if len(grouping)==0:
            memo_dict[key] = 1
       
    #base case #2, no more broken spring groups
    elif len(grouping)==0:
        #check the spring_string to make sure there are no more guaranteed broken springs 
        #(i.e. string doesn't contain '#' characters)
        string_valid_test = True
        for test_char in spring_str:
            if test_char=='#':
                string_valid_test = False

        #if there are no more guaranteed broken springs, this is a single valid arrangement. Set table to 1 and return
        if string_valid_test:
            memo_dict[key] = 1    

    #if the length of the spring string is at least the length of the first contiguous group of damaged springs...
    elif grouping[0]<=len(spring_str):
        #examine the first character of the spring group

        #case 1: first character read as an operational spring
        if spring_str[0]=='.' or spring_str[0]=='?':
            #recurse on the suffix of the spring string
            memo_dict[key] += num_valid_arrangements(spring_str[1:],grouping,memo_dict)
            
        #case 2: first character read as a broken spring
        if spring_str[0]=='#' or spring_str[0]=='?':
            #check to see if there is a valid prefix of the string that corresponds to
            #a contiguous group of damaged springs of length grouping[0]
            block_valid_test = True
            for i in range(grouping[0]):
                if spring_str[i]=='.':
                    block_valid_test = False
        
            #if such a valid prefix exists
            if block_valid_test:
                #if that prefix is the string itself, (and there are no more groups of damaged springs) 
                #there is a single valid arrangement. increment the table and return
                if grouping[0]==len(spring_str) and len(grouping)==1:
                    memo_dict[key] += 1
                    
                #if the next character after the valid prefix is not a '#'
                elif grouping[0]<len(spring_str) and spring_str[grouping[0]]!='#':
                    #then we are done with the prefix+next character, and the current contiguous group
                    #recurse on the suffix string and the remainder of the grouping list
                    memo_dict[key] += num_valid_arrangements(spring_str[grouping[0]+1:],grouping[1:],memo_dict)

    return memo_dict[key]


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    spring_str_list, grouping_list = parse_input01(fname)
    
    total = 0
    for i in range(len(spring_str_list)):
        total+= num_valid_arrangements(spring_str_list[i],grouping_list[i],{})
    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    spring_str_list, grouping_list = parse_input01(fname)
    
    total = 0
    for i in range(len(spring_str_list)):
        spring_str,grouping = expand_problem(spring_str_list[i],grouping_list[i])
        total+= num_valid_arrangements(spring_str,grouping,{})
    print(total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))