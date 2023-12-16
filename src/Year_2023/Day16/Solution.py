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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

north = (-1, 0)
south = ( 1, 0)
east = ( 0, 1)
west = ( 0,-1)

empty_space_rule = {
    north:[north],
    south:[south],
    east:[east],
    west:[west]
}

vertical_splitter_rule = {
    north:[north],
    south:[south],
    east:[north,south],
    west:[north,south]
}

horizontal_splitter_rule = {
    north:[east,west],
    south:[east,west],
    east:[east],
    west:[west]
}

fwdslash_rule = {
    north:[east],
    south:[west],
    east:[north],
    west:[south]
}

backslash_rule = {
    north:[west],
    south:[east],
    east:[south],
    west:[north]
}

beam_rule_dict = {
    '.':empty_space_rule,
    '|':vertical_splitter_rule,
    '-':horizontal_splitter_rule,
    '/':fwdslash_rule,
    '\\':backslash_rule
}

direction_char_dict = {
    north:'^',
    south:'v',
    east:'>',
    west:'<'
}


def check_coord_in_bounds(grid_in,current_coord):
    return 0<=current_coord[0] and current_coord[0]<len(grid_in) and 0<=current_coord[1] and current_coord[1]<len(grid_in[0])

def single_beam_step(grid_in,coord_in,dir_in):
    coord_out = (coord_in[0]+dir_in[0],coord_in[1]+dir_in[1])

    in_bounds = check_coord_in_bounds(grid_in,coord_out)
    dir_out_list = []

    if in_bounds:
        next_char = grid_in[coord_out[0]][coord_out[1]]
        dir_out_list = beam_rule_dict[next_char][dir_in]

    return coord_out, dir_out_list, in_bounds


def run_sim(grid_in,energize_mat,beam_set,update_list):
    while len(update_list)>0:
        current_item = update_list.pop(-1)
        current_coord = current_item[0]
        current_dir = current_item[1]

        coord_out, dir_out_list, in_bounds = single_beam_step(grid_in,current_coord,current_dir)

        if in_bounds:
            for dir_out in dir_out_list:
                next_item = (coord_out,dir_out)
                if next_item not in beam_set:
                    beam_set.add(next_item)
                    energize_mat[coord_out[0]][coord_out[1]]+=1
                    update_list.append(next_item)

def compute_energy(grid_in,start_item):
    energize_mat = []
    for i in range(len(grid_in)):
        energize_mat.append([0]*len(grid_in[0]))

    beam_set = {start_item}

    run_sim(grid_in,energize_mat,beam_set,[start_item])

    total = 0
    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if energize_mat[i][j]>0:
                total+=1
    return total, energize_mat, beam_set

def print_beam_grid(grid_in,energize_mat,beam_set):
    grid_out = []
    for i in range(len(grid_in)):
        line_out = []
        for j in range(len(grid_in[0])):
            line_out.append(grid_in[i][j])
        grid_out.append(line_out)

    for item in beam_set:
        current_coord = item[0]
        current_dir = item[1]
        if check_coord_in_bounds(grid_in,current_coord) and grid_out[current_coord[0]][current_coord[1]]=='.':
            if energize_mat[current_coord[0]][current_coord[1]]==1:
                grid_out[current_coord[0]][current_coord[1]]=direction_char_dict[current_dir]
            else:
                grid_out[current_coord[0]][current_coord[1]]=str(energize_mat[current_coord[0]][current_coord[1]])

    bh.print_char_matrix(grid_out)
    print()

def print_energy_grid(grid_in,energize_mat):
    grid_out = []
    for i in range(len(grid_in)):
        line_out = []
        for j in range(len(grid_in[0])):
            line_out.append(grid_in[i][j])
        grid_out.append(line_out)

    for i in range(len(grid_out)):
        for j in range(len(grid_out[0])):
            if energize_mat[i][j]==0:
                grid_out[i][j]='.'
            else:
                grid_out[i][j]='#'
    bh.print_char_matrix(grid_out)
    print()


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    start_item = ((0,-1),east)
    energy_out, energize_mat, beam_set = compute_energy(data,start_item)

    # print_beam_grid(data,energize_mat,beam_set)
    # print_energy_grid(data,energize_mat)
    print(energy_out)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    max_energy = 0
    for i in range(len(data)):
        left_item = ((i,-1),east)
        right_item = ((i,len(data[0])),west)

        energy_out, energize_mat, beam_set = compute_energy(data,left_item)
        max_energy = max(max_energy,energy_out)

        energy_out, energize_mat, beam_set = compute_energy(data,right_item)
        max_energy = max(max_energy,energy_out)


    for j in range(len(data[0])):
        top_item = ((-1,j),south)
        bottom_item = ((len(data[0]),j),north)

        energy_out, energize_mat, beam_set = compute_energy(data,top_item)
        max_energy = max(max_energy,energy_out)
        energy_out, energize_mat, beam_set = compute_energy(data,bottom_item)
        max_energy = max(max_energy,energy_out)

    print(max_energy)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

