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

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    grid_out = []

    for i in range(1,(len(data)-1)):
        line = data[i]
        grid_out.append(line[1:(len(line)-1)])

    return grid_out

def compute_occupied_times(i0,j0,grid_in):
    l0 = len(grid_in)
    l1 = len(grid_in[0])

    occupied_times_vertical = set()
    occupied_times_horizontal = set()

    for i in range(l0):
        if grid_in[i][j0]=='^':
            occupied_times_vertical.add((i-i0)%l0)

        elif grid_in[i][j0]=='v':
            occupied_times_vertical.add((i0-i)%l0)
                
    for j in range(l1):
        if grid_in[i0][j]=='<':
            occupied_times_horizontal.add((j-j0)%l1)

        elif grid_in[i0][j]=='>':
            occupied_times_horizontal.add((j0-j)%l1)

    return occupied_times_vertical, occupied_times_horizontal

def construct_board(grid_in):

    dict_out_vertical = {}
    dict_out_horizontal = {}

    l0 = len(grid_in)
    l1 = len(grid_in[0])

    for i in range(l0):
        for j in range(l1):
            occupied_times_vertical, occupied_times_horizontal = compute_occupied_times(i,j,grid_in)

            dict_out_vertical[(i,j)]=occupied_times_vertical
            dict_out_horizontal[(i,j)]=occupied_times_horizontal

    start_coord = (-1,0)
    end_coord = (l0,l1-1)

    dict_out_vertical[start_coord]=set()
    dict_out_vertical[end_coord]=set()
    dict_out_horizontal[start_coord]=set()
    dict_out_horizontal[end_coord]=set()

    return dict_out_vertical, dict_out_horizontal, start_coord, end_coord, l0, l1

direction_list = [np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0]),np.array([0,0])]

def serialize_state(coords_in,t):
    return (tuple(coords_in.tolist()),t)

def deserialize_state(key):
    coords = key[0]
    t = key[1]

    return np.array(list(coords)),t

def compute_forward_neighbors(key,board_v, board_h, height, width):

    coords,t = deserialize_state(key)

    t_next = t+1

    neighbor_list = []

    for direction in direction_list:
        adjacent_coords = coords+direction

        adjacent_key = tuple(adjacent_coords.tolist())

        if (adjacent_key in board_v and 
            t_next%height not in board_v[adjacent_key] and t_next%width not in board_h[adjacent_key]):
        
            neighbor_list.append(serialize_state(adjacent_coords,t_next))

    return neighbor_list

def run_BFS(board_v, board_h, height, width,t_start,start_coord,end_coord):
    current_key = (start_coord,t_start)

    visited_dict = {}
    myQueue = deque()
    myQueue.append(current_key)
    visited_dict[current_key]=True

    while len(myQueue)>0:
        current_key = myQueue.popleft()

        if current_key[0]==end_coord:
            return current_key[1]

        neighbor_list = compute_forward_neighbors(current_key,board_v, board_h, height, width)

        for neighbor in neighbor_list:
            if neighbor not in visited_dict:
                myQueue.append(neighbor)
                visited_dict[neighbor]=True

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    board_v, board_h, start_coord, end_coord, height, width = construct_board(data)

    t = 0
    t_finish = run_BFS(board_v, board_h, height, width,t,start_coord,end_coord)
    print(t_finish)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    board_v, board_h, start_coord, end_coord, height, width = construct_board(data)

    t = 0

    t = run_BFS(board_v, board_h, height, width,t,start_coord,end_coord)
    t = run_BFS(board_v, board_h, height, width,t,end_coord,start_coord)
    t = run_BFS(board_v, board_h, height, width,t,start_coord,end_coord)

    print(t)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

