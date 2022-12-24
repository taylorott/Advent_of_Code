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

    t_rep = lcm(l0,l1)
    occupied_times = set()

    for i in range(l0):
        period = None
        t_offset = None

        if grid_in[i][j0]=='^':
            period = l0
            t_offset = (i-i0)%period

        elif grid_in[i][j0]=='v':
            period = l0
            t_offset = (i0-i)%period

        if grid_in[i][j0]=='^' or grid_in[i][j0]=='v':
            t = t_offset
            while t<t_rep:
                occupied_times.add(t)
                t+=period

    for j in range(l1):
        period = None
        t_offset = None

        if grid_in[i0][j]=='<':
            period = l1
            t_offset = (j-j0)%period

        elif grid_in[i0][j]=='>':
            period = l1
            t_offset = (j0-j)%period

        if grid_in[i0][j]=='<' or grid_in[i0][j]=='>':
            t = t_offset
            while t<t_rep:
                occupied_times.add(t)
                t+=period

    return occupied_times

def construct_board(grid_in):

    dict_out = {}

    l0 = len(grid_in)
    l1 = len(grid_in[0])

    for i in range(l0):
        for j in range(l1):
            occupied_times = compute_occupied_times(i,j,grid_in)

            dict_out[(i,j)]=occupied_times

    start_coord = (-1,0)
    end_coord = (l0,l1-1)
    period = lcm(l0,l1)

    dict_out[start_coord]=set()
    dict_out[end_coord]=set()

    return dict_out, start_coord, end_coord, period

direction_list = [np.array([0,1]),np.array([1,0]),np.array([0,-1]),np.array([-1,0]),np.array([0,0])]

def serialize_state(coords_in,t):
    return (tuple(coords_in.tolist()),t)

def deserialize_state(key):
    coords = key[0]
    t = key[1]

    return np.array(list(coords)),t

def compute_forward_neighbors(key,board,t_period):

    coords,t = deserialize_state(key)

    t_next = t+1
    t_check = t_next%t_period

    neighbor_list = []

    for direction in direction_list:
        adjacent_coords = coords+direction

        adjacent_key = tuple(adjacent_coords.tolist())

        if adjacent_key in board and t_check not in board[adjacent_key]:
            neighbor_list.append(serialize_state(adjacent_coords,t_next))

    return neighbor_list

def run_BFS(board,period,t_start,start_coord,end_coord):
    current_key = (start_coord,t_start)

    visited_dict = {}
    myQueue = deque()
    myQueue.append(current_key)
    visited_dict[current_key]=True

    while len(myQueue)>0:
        current_key = myQueue.popleft()

        if current_key[0]==end_coord:
            return current_key[1]

        neighbor_list = compute_forward_neighbors(current_key,board,period)

        for neighbor in neighbor_list:
            if neighbor not in visited_dict:
                myQueue.append(neighbor)
                visited_dict[neighbor]=True

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    board, start_coord, end_coord, period = construct_board(data)

    t = 0
    t_finish = run_BFS(board,period,t,start_coord,end_coord)
    print(t_finish)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    board, start_coord, end_coord, period = construct_board(data)

    t = 0

    t = run_BFS(board,period,t,start_coord,end_coord)
    t = run_BFS(board,period,t,end_coord,start_coord)
    t = run_BFS(board,period,t,start_coord,end_coord)

    print(t)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

