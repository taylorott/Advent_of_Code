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

def turn_left(dir_in):
    return (-dir_in[1],dir_in[0])
def turn_right(dir_in):
    return (dir_in[1],-dir_in[0])

def compute_interior_directions(command_list):
    winding_number = 0

    for i in range(len(command_list)):
  
        direction0 = direction_dict[command_list[i][0]]
        direction1 = direction_dict[command_list[(i+1)%len(command_list)][0]]

        if direction1 == turn_left(direction0):
            winding_number+=1
        elif direction1 == turn_right(direction0):
            winding_number-=1

    winding_number//=4

    interior_direction_list = []

    for command in command_list:
        direction = direction_dict[command[0]]

        if winding_number == 1:
            interior_direction_list.append(turn_left(direction))
        elif winding_number == -1:
            interior_direction_list.append(turn_right(direction))

    return interior_direction_list
   
def build_large_trench(command_list):
    interior_direction_list = compute_interior_directions(command_list)


    trench_dict = {}
    row_set = set()
    col_set = set()

    perimeter = 0

    start_coord = (0,0)
    

    current_coord = start_coord
    interior_direction = None

    coord_list = [start_coord]

    for i in range(len(command_list)):
        command = command_list[i]

        dist = command[1]

        perimeter+=dist

        direction = direction_dict[command[0]]

        row_set.add(current_coord[0])
        col_set.add(current_coord[1])

        current_coord = (current_coord[0]+direction[0]*dist,current_coord[1]+direction[1]*dist)

        coord_list.append(current_coord)


    row_list = list(row_set)
    row_list.sort()

    col_list = list(col_set)
    col_list.sort()

    
    index_lookup_dict = {}
    coord_lookup_dict = {}

    row_zero_index = row_list.index(0)
    col_zero_index = col_list.index(0)

    for i in range(len(row_list)):
        for j in range(len(col_list)):
            index_lookup_dict[(row_list[i],col_list[j])]=(i-row_zero_index,j-col_zero_index)

    for key in index_lookup_dict:
        val = index_lookup_dict[key]
        coord_lookup_dict[val] = key


    trench_dict_reduced = {}

    for i in range(len(coord_list)-1):

        direction = direction_dict[command_list[i][0]]

        coord0 = coord_list[i]
        interior_direction0 = interior_direction_list[i]

        reduced_coord0 = index_lookup_dict[coord0]

        if reduced_coord0 not in trench_dict_reduced:
            trench_dict_reduced[reduced_coord0] = {interior_direction0}

        coord1 = coord_list[i+1]
        interior_direction1 = interior_direction_list[(i+1)%len(command_list)]

        reduced_coord1 = index_lookup_dict[coord1]

        if reduced_coord1 not in trench_dict_reduced:
            trench_dict_reduced[reduced_coord1] = {interior_direction0, interior_direction1}

        current_reduced_coord = reduced_coord0

        while current_reduced_coord!=reduced_coord1:
            current_reduced_coord = (current_reduced_coord[0]+direction[0],current_reduced_coord[1]+direction[1])

            if current_reduced_coord not in trench_dict_reduced:
                trench_dict_reduced[current_reduced_coord] = {interior_direction0}


    return trench_dict_reduced, index_lookup_dict, coord_lookup_dict, perimeter

def build_trench(command_list):
    interior_direction_list = compute_interior_directions(command_list)

    trench_dict = {}
    start_coord = (0,0)
    current_coord = start_coord

    trench_dict[start_coord] = set()
    interior_direction = None

    for i in range(len(command_list)):
        command = command_list[i]

        dist = command[1]
        direction = direction_dict[command[0]]

        interior_direction = interior_direction_list[i]

        if current_coord in trench_dict and i!=0:
            trench_dict[current_coord].add(interior_direction)

        for i in range(dist):
            current_coord = (current_coord[0]+direction[0],current_coord[1]+direction[1])
            trench_dict[current_coord]= {interior_direction}



    return trench_dict

def trench_boundaries_by_row(trench_dict):
    row_dict = {}

    for coord in trench_dict:
        if coord[0] not in row_dict:
            row_dict[coord[0]] = [coord[1]]
        else:
            row_dict[coord[0]].append(coord[1])

    for row_key in row_dict:
        row_dict[row_key].sort()

    return row_dict



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    trench_dict = build_trench(data)
    row_dict = trench_boundaries_by_row(trench_dict)
    area = compute_area_by_row(trench_dict,row_dict)
    print(area)
    print()


    # print(trench_set)
    # print(data)

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

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)

    command_list = decode_command_list(data)
    trench_dict_reduced, index_lookup_dict, coord_lookup_dict, perimeter = build_large_trench(command_list)
    row_dict = trench_boundaries_by_row(trench_dict_reduced)
  

    # for key in trench_dict:
    #     print(key,trench_dict[key])

    # print(trench_dict)



if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

