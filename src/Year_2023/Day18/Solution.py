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
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)
    for item in data:
        item[1]=int(item[1])

    return data

direction_dict = {'U':(-1,0),'D':(1,0),'L':(0,-1),'R':(0,1)}
direction_list = [(-1,0),(1,0),(0,-1),(0,1)]

decode_dict = {'0':'R','1':'D','2':'L','3':'U'}

def decode_command(command_in):
    command_str = command_in[2]
    command_str = command_str[2:(len(command_str)-1)]

    command_dist = int(command_str[:len(command_str)-1],16)
    command_direction = decode_dict[command_str[-1]]
    return [command_direction,command_dist]

def decode_command_list(command_list_in):
    command_list_out = []

    for command in command_list_in:
        command_list_out.append(decode_command(command))

    return command_list_out

def floodfill_exterior(trench_dict):
    coord_stack = [(0,0)]

    while len(coord_stack)>0:
        current_coord = coord_stack.pop(-1)

        trench_dict[current_coord] = 'O'

        for direction in direction_list:
            next_coord = (current_coord[0]+direction[0],current_coord[1]+direction[1])

            if next_coord in trench_dict and trench_dict[next_coord]=='I':
                trench_dict[next_coord] = 'O'
                coord_stack.append(next_coord)

def build_trench(command_list):

    row_set = set()
    col_set = set()

    start_coord = (0,0)
    
    coord_list = [start_coord]

    current_coord = start_coord


    for i in range(len(command_list)):
        command = command_list[i]
        dist = command[1]
        direction = direction_dict[command[0]]

        row_set.add(current_coord[0]-1)
        row_set.add(current_coord[0])
        row_set.add(current_coord[0]+1)

        col_set.add(current_coord[1]-1)
        col_set.add(current_coord[1])
        col_set.add(current_coord[1]+1)

        current_coord = (current_coord[0]+direction[0]*dist,current_coord[1]+direction[1]*dist)

        coord_list.append(current_coord)


    row_list = list(row_set)
    row_list.sort()

    col_list = list(col_set)
    col_list.sort()

    
    index_lookup_dict = {}
    coord_lookup_dict = {}


    for i in range(len(row_list)):
        for j in range(len(col_list)):
            index_lookup_dict[(row_list[i],col_list[j])]=(i,j)


    for key in index_lookup_dict:
        val = index_lookup_dict[key]
        coord_lookup_dict[val] = key



    trench_dict = {}
    for i in range(len(row_list)):
        for j in range(len(col_list)):
            trench_dict[(i,j)]='I'



    for i in range(len(coord_list)-1):
        command = command_list[i]
        dist = command[1]
        direction = direction_dict[command[0]]

        coord0 = coord_list[i]
        reduced_coord0 = index_lookup_dict[coord0]

        coord1 = coord_list[i+1]
        reduced_coord1 = index_lookup_dict[coord1]

        current_reduced_coord = reduced_coord0

        while current_reduced_coord!=reduced_coord1:
            current_reduced_coord = (current_reduced_coord[0]+direction[0],current_reduced_coord[1]+direction[1])

            trench_dict[current_reduced_coord] = 'B'

    floodfill_exterior(trench_dict)

    return trench_dict, coord_lookup_dict

def compute_square_area(trench_dict, coord_lookup_dict, top_left):
    bottom_left = (top_left[0]+1,top_left[1])
    top_right = (top_left[0],top_left[1]+1)
    bottom_right = (top_left[0]+1,top_left[1]+1)

    top_left_coord = coord_lookup_dict[top_left]

    top_right_coord = None
    bottom_left_coord = None
    h = None
    w = None

    top_left_char = trench_dict[top_left]
    top_right_char = trench_dict[top_right]
    bottom_left_char = trench_dict[bottom_left]
    bottom_right_char = trench_dict[bottom_right]


    if bottom_left in coord_lookup_dict:
        bottom_left_coord = coord_lookup_dict[bottom_left]
        h = bottom_left_coord[0]-top_left_coord[0]-1


    if top_right in coord_lookup_dict:
        top_right_coord = coord_lookup_dict[top_right]
        w = top_right_coord[1]-top_left_coord[1]-1


    area = 0

    if top_left_char!='O':
        area+=1

    if top_left_char!='O' and top_right_char!='O':
        area+=w

    if top_left_char!='O' and bottom_left_char!='O':
        area+=h

    if top_left_char!='O' and top_right_char!='O' and bottom_left_char!='O' and bottom_right_char!='O':
        area+=h*w

    return area

def compute_total_area(trench_dict, coord_lookup_dict):
    area = 0
    for top_left in trench_dict:
        if trench_dict[top_left]!='O':
            area+=compute_square_area(trench_dict, coord_lookup_dict, top_left)

    return area


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    trench_dict, coord_lookup_dict = build_trench(data)
    area = compute_total_area(trench_dict, coord_lookup_dict)
    print(area)




def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    command_list = decode_command_list(data)
    trench_dict, coord_lookup_dict = build_trench(command_list)
    
    area = compute_total_area(trench_dict, coord_lookup_dict)
    print(area)




if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

