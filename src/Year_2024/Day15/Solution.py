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

move_dict = {'^':(-1,0),'>':(0,1),'<':(0,-1),'v':(1,0)}
def parse_input01(fname):
    return  bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

def build_grid(grid):
    state_dict = {}

    robot_coord = None
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            c = grid[i][j]

            key = (i,j)
            if c!='.' and c!='@':
                state_dict[key]=c

            if c=='@':
                robot_coord = key

    return state_dict, robot_coord

def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def get_children_recursive(current_coord, move_dir, state_dict, visited_set):
    if current_coord in visited_set or current_coord not in state_dict: return True 
        
    visited_set.add(current_coord)

    if state_dict[current_coord]=='#': return False
        
    result = get_children_recursive(coord_addition(current_coord,move_dir), move_dir, state_dict, visited_set)
    if state_dict[current_coord]=='[':
        result &= get_children_recursive(coord_addition(current_coord,(0,1)), move_dir, state_dict, visited_set)
    if state_dict[current_coord]==']':
        result &= get_children_recursive(coord_addition(current_coord,(0,-1)), move_dir, state_dict, visited_set)

    return result
    
def update_state2(move_char,state_dict,robot_coord):
    move_dir = move_dict[move_char]

    visited_set = set()

    next_coord = (robot_coord[0]+move_dir[0],robot_coord[1]+move_dir[1])

    can_move = get_children_recursive(next_coord, move_dir, state_dict, visited_set)

    if not can_move: return robot_coord 

    temp_dict = dict()
    for coord in visited_set:
        temp_dict[coord] = state_dict.pop(coord)

    for coord in visited_set:
        temp_next = (coord[0]+move_dir[0],coord[1]+move_dir[1])
        state_dict[temp_next] = temp_dict[coord]

    return next_coord

def compute_score(state_dict):
    total = 0
    for key in state_dict:
        if state_dict[key]=='O' or state_dict[key]=='[':
            total+=100*key[0]+key[1]

    return total     

def double_grid(grid_in):
    grid_out = []

    for item in grid_in:
        str_temp = ''
        for c in item:
            if c=='#':
                str_temp+='##'
            if c=='.':
                str_temp+='..'
            if c=='O':
                str_temp+='[]'
            if c=='@':
                str_temp+='@.'
        grid_out.append(str_temp)
    return grid_out

def run_all_commands(robot_coord, state_dict, command_list):
    for item in command_list:
        for move_char in item:
            robot_coord = update_state2(move_char,state_dict,robot_coord)

    return compute_score(state_dict)

def solution(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    state_dict, robot_coord = build_grid(data[0])
    v1 = run_all_commands(robot_coord, state_dict, data[1])

    state_dict, robot_coord = build_grid(double_grid(data[0]))
    v2 = run_all_commands(robot_coord, state_dict, data[1])

    if show_result: print(str(v1)+'\n'+str(v2))

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    
