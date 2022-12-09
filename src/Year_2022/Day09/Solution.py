#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph, frequency_table
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    for line in data:
        line[1]=int(line[1])

    return data

move_dict = {'R':np.array([1,0]),'L':np.array([-1,0]),'U':np.array([0,1]),'D':np.array([0,-1])}

def gap_dist(c1,c2):
    return max(abs(c1[0]-c2[0]),abs(c1[1]-c2[1]))

def update_knot_one_step(head_coords,tail_coords):
    current_dist = gap_dist(head_coords,tail_coords)

    if current_dist<2:
        return None

    tail_coords[0]+=np.sign(head_coords[0]-tail_coords[0])
    tail_coords[1]+=np.sign(head_coords[1]-tail_coords[1])

def update_coords(coord_list,move,visited_dict):
    move_dir = move_dict[move[0]]
    move_mag = move[1]

    for i in range(move_mag):
        coord_list[0]+=move_dir

        for i in range(0,len(coord_list)-1):
            update_knot_one_step(coord_list[i],coord_list[i+1])

        key_visit = (coord_list[-1][0],coord_list[-1][1])
        visited_dict[key_visit]=None

def eval_knots_snake(commands,num_coords):

    coord_list = []
    for i in range(num_coords):
        coord_list.append(np.array([0,0]))

    visited_dict = {}
    visited_dict[(0,0)]=None
    for move in commands:
        update_coords(coord_list,move,visited_dict)

    count = 0
    for key in visited_dict.keys():
        count+=1

    print(count)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    eval_knots_snake(data,2)


def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    eval_knots_snake(data,10)

if __name__ == '__main__':
    solution01()
    solution02()
    

