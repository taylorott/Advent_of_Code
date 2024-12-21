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

up, down, left, right = (-1,0), (1,0), (0,-1), (0,1)

direction_dict = {'^':up, 'v':down, '>':right, '<':left}
direction_lookup = {up:'^', down:'v', right:'>', left:'<'}

numeric_forward = {'7':(0,0),'8':(0,1),'9':(0,2),'4':(1,0),'5':(1,1),'6':(1,2),'1':(2,0),'2':(2,1),'3':(2,2),'0':(3,1),'A':(3,2)} 
numeric_reverse = {(0,0):'7',(0,1):'8',(0,2):'9',(1,0):'4',(1,1):'5',(1,2):'6',(2,0):'1',(2,1):'2',(2,2):'3',(3,1):'0',(3,2):'A'}

keypad_forward = {'^':(0,1),'A':(0,2),'<':(1,0),'v':(1,1),'>':(1,2)}
keypad_reverse = {(0,1):'^',(0,2):'A',(1,0):'<',(1,1):'v',(1,2):'>'}


def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def parse_input01(fname):
    return  bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

def keystrokes(button1, button2, is_numeric=False):
    press_list, fixed_order, coord1, coord2, bad_coord = [], True, None, None, None

    if is_numeric: coord1, coord2, bad_coord = numeric_forward[button1], numeric_forward[button2], (3,0)

    else: coord1, coord2, bad_coord = keypad_forward[button1], keypad_forward[button2], (0,0)

    di, dj = coord2[0]-coord1[0], coord2[1]-coord1[1]
    if abs(di)!=0: press_list.append((direction_lookup[(di//abs(di),0)],abs(di)))
    if abs(dj)!=0: press_list.append((direction_lookup[(0,dj//abs(dj))],abs(dj)))

    if len(press_list)==2:
        fixed_order = False

        if (coord2[0],coord1[1]) == bad_coord:
            fixed_order = True
            press_list.reverse()

        elif (coord1[0],coord2[1]) == bad_coord:
            fixed_order = True

    return press_list, fixed_order

def recursive_helper(press_list,cost_table,layer,max_depth):
    total = 0
    current_button = 'A'
    for item in press_list:
        next_button = item[0]
        next_key = (current_button,next_button,layer+1)

        total += compute_cost_recursive((current_button,next_button,layer+1),cost_table,max_depth)
        total += (item[1]-1)*compute_cost_recursive((next_button,next_button,layer+1),cost_table,max_depth)

        current_button = next_button

    total+= compute_cost_recursive((current_button,'A',layer+1),cost_table,max_depth)
    return total

def compute_cost_recursive(key,cost_table, max_depth=25):
    if key in cost_table: return cost_table[key]

    button1, button2, layer = key[0], key[1], key[2]
    press_list, fixed_order, result = [], False, 0

    if layer==0: press_list, fixed_order = keystrokes(button1, button2, True)
    else: press_list, fixed_order = keystrokes(button1, button2)

    if layer==max_depth:
        result = 1
        for item in press_list: result+=item[1]
    
    else:
        result = recursive_helper(press_list,cost_table,layer,max_depth)

        if not fixed_order:
            press_list.reverse()
            result = min(result, recursive_helper(press_list,cost_table,layer,max_depth))

    cost_table[key] = result
    return cost_table[key]

def compute_str_cost(str_in,cost_table,max_depth):
    str_in = 'A'+str_in

    total = 0
    for i in range(len(str_in)-1):
        key = (str_in[i],str_in[i+1],0)

        total+=compute_cost_recursive(key,cost_table,max_depth)

    return int(str_in[1:4])*total

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total1, total2, cost_table1, cost_table2 = 0, 0, dict(), dict()

    for item in data:
        total1+=compute_str_cost(item,cost_table1,2)
        total2+=compute_str_cost(item,cost_table2,25)

    if show_result: print(str(total1)+'\n'+str(total2))

    return total1, total2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

