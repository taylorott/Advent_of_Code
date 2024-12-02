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
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

def play_game(num_players,max_marble):
    score_list = [0]*num_players

    myList = LinkedList(0)
    myList.next = myList
    myList.prev = myList

    for i in range(1,max_marble+1):
     
        if i%23==0:
            score_list[i%num_players]+=i
            myList = myList[-7]

            score_list[i%num_players]+=myList.val

            temp = myList.next
   
            myList.delete_self()
            myList = temp

        else:
            myList = myList.next
            myList.insert_next_val(i)
            myList = myList.next
    return max(score_list)

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # num_players = 9
    # max_marble = 25

    num_players = 476
    max_marble1 = 71431
    max_marble2 = 7143100

    print(play_game(num_players,max_marble1))
    print(play_game(num_players,max_marble2))

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

