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
    # data = bh.parse_char_grid(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [','],type_lookup = None, allInt = True, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data[0]

direction_list = [np.array([1,0,0]),np.array([-1,0,0]),np.array([0,1,0]),np.array([0,-1,0]),np.array([0,0,1]),np.array([0,0,-1])]

def count_open_faces(cube_coord,cube_dict,exterior_dict = None):
    cube_array = np.array(list(cube_coord))

    total = 0
    for direction in direction_list:
        adjacent_cube = cube_array+direction
        adjacent_key = tuple(adjacent_cube.tolist())
        if (exterior_dict is not None and adjacent_key in exterior_dict) or (exterior_dict is None and adjacent_key not in cube_dict):
            total+=1
    return total

def attempt_to_fill(current_coord,cube_dict,exterior_dict,max_volume):
    visited_dict = {current_coord:True}

    myQueue = deque()
    myQueue.append(current_coord)

    update_list = []

    on_exterior = False

    while len(myQueue)>0:
        current_coord=myQueue.popleft()
        cube_dict[current_coord]='A'
        update_list.append(current_coord)

        if len(update_list)>max_volume:
            on_exterior = True
            break

        current_coord_array = np.array(list(current_coord))

        for direction in direction_list:
            adjacent_cube = current_coord_array+direction
            adjacent_key = tuple(adjacent_cube.tolist())

            if adjacent_key not in cube_dict and adjacent_key not in visited_dict and adjacent_key not in exterior_dict:
                visited_dict[adjacent_key]=True
                myQueue.append(adjacent_key)
            elif adjacent_key in exterior_dict:
                on_exterior = True
                break

    if on_exterior:
        while len(update_list)>0:
            current_coord =  update_list.pop()
            exterior_dict[current_coord] = True
            cube_dict.pop(current_coord)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    cube_dict = {}

    for item in data:
        cube_dict[tuple(item)]=True

    total = 0
    for cube in cube_dict:
        total+=count_open_faces(cube,cube_dict)
    print(total)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    cube_dict = {}
    exterior_dict = {}

    max_volume = np.ceil(np.sqrt(len(data)+1)**3)

    for item in data:
        cube_dict[tuple(item)]='L'

    for item in data:
        cube_array = np.array(item)

        for direction in direction_list:
            adjacent_cube = cube_array+direction
            adjacent_key = tuple(adjacent_cube.tolist())

            if adjacent_key not in cube_dict and adjacent_key not in exterior_dict:
                attempt_to_fill(adjacent_key,cube_dict,exterior_dict,max_volume)

    total = 0
    for item in data:
        total+=count_open_faces(tuple(item),cube_dict,exterior_dict)
    print(total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

