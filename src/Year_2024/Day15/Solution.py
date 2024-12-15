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
double_map = {'#':'##','.':'..','O':'[]','@':'@.'}

def parse_input01(fname):
    return  bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

def build_grid(grid):
    state_dict, robot_coord = {}, None

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            c, coord = grid[i][j], (i,j)

            if c!='.' and c!='@': state_dict[coord]=c

            if c=='@': robot_coord = coord

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
    
def update_state(move_char,state_dict,robot_coord):
    move_dir = move_dict[move_char]

    visited_set = set()

    next_coord = coord_addition(robot_coord,move_dir)

    can_move = get_children_recursive(next_coord, move_dir, state_dict, visited_set)

    if not can_move: return robot_coord 

    temp_dict = dict()
    for coord in visited_set: temp_dict[coord] = state_dict.pop(coord)

    for coord in visited_set: state_dict[coord_addition(coord,move_dir)] = temp_dict[coord]

    return next_coord

def compute_score(state_dict):
    total = 0
    for coord in state_dict:
        if state_dict[coord]=='O' or state_dict[coord]=='[': total+=100*coord[0]+coord[1]
            
    return total

def double_grid(grid_in):
    grid_out = []
    for item in grid_in:
        str_temp = ''
        for c in item: str_temp+=double_map[c]

        grid_out.append(str_temp)
    return grid_out

def run_all_commands(robot_coord, state_dict, command_list):
    for item in command_list:
        for move_char in item:
            robot_coord = update_state(move_char,state_dict,robot_coord)

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