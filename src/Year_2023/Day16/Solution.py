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
    return bh.parse_char_grid(path,fname)

north, south, east, west = (-1, 0), ( 1, 0), ( 0, 1), ( 0,-1)

empty_space_rule = {north:[north], south:[south],
                    east:[east],   west:[west]}

vertical_splitter_rule = {north:[north], south:[south],
                          east:[north,south], west:[north,south]}

horizontal_splitter_rule = {north:[east,west], south:[east,west],
                            east:[east], west:[west]}

fwdslash_rule = {north:[east], east:[north], 
                 south:[west], west:[south]}

backslash_rule = {north:[west], west:[north],
                  south:[east], east:[south]}

beam_rule_dict = {'.':empty_space_rule,
    '|':vertical_splitter_rule, '-':horizontal_splitter_rule,
    '/':fwdslash_rule, '\\':backslash_rule}

direction_char_dict = {north:'^', south:'v',
    east:'>', west:'<'}

def single_beam_step(grid_in,coord_in,dir_in):
    coord_out = (coord_in[0]+dir_in[0],coord_in[1]+dir_in[1])

    in_bounds = 0<=coord_out[0] and coord_out[0]<len(grid_in) and 0<=coord_out[1] and coord_out[1]<len(grid_in[0])
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

    beam_set = set()

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
        if grid_out[current_coord[0]][current_coord[1]]=='.':
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

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    start_item = ((0,-1),east)
    energy_out, energize_mat, beam_set = compute_energy(data,start_item)

    # print_beam_grid(data,energize_mat,beam_set)
    # print_energy_grid(data,energize_mat)
    if show_result: print(energy_out)
        
    return energy_out

def is_in_bounds(coord,grid):
    return 0<=coord[0] and coord[0]<len(grid) and 0<=coord[1] and coord[1]<len(grid[0])

def build_lane(current_coord, current_dir, my_graph, grid_in):
    while is_in_bounds(current_coord,grid_in):
        key1 = (current_coord,current_dir)
        vertex_group = set()
      
        while is_in_bounds(current_coord,grid_in) and grid_in[current_coord[0]][current_coord[1]]=='.':
            vertex_group.add(current_coord)
            current_coord = (current_coord[0]+current_dir[0],current_coord[1]+current_dir[1])

        if is_in_bounds(current_coord,grid_in): 
            vertex_group.add(current_coord)
            c = grid_in[current_coord[0]][current_coord[1]]
            for next_dir in beam_rule_dict[c][current_dir]:
                next_coord = (current_coord[0]+next_dir[0],current_coord[1]+next_dir[1])
                key2 = (next_coord,next_dir)
                my_graph.add_edge(key1,key2)
            current_coord = (current_coord[0]+current_dir[0],current_coord[1]+current_dir[1])
        else:
            key2 = (current_coord,current_dir)
            my_graph.add_edge(key1,key2)

        my_graph.vertex_dict[key1]=vertex_group

def build_graph(grid_in):
    my_graph = Digraph()

    for i in range(len(grid_in)):
        build_lane((i,0), east, my_graph, grid_in)
        build_lane((i,len(grid_in[0])-1), west, my_graph, grid_in)
    for j in range(len(grid_in[0])):
        build_lane((0,j), south, my_graph, grid_in)
        build_lane((len(grid_in)-1,j), north, my_graph, grid_in)

    return my_graph

#returns true if and only if v1 has one "child", and that child's only parent is v1
def can_contract(v1,my_graph):
    if len(my_graph.meta_forward_dict[v1])!=1: return False

    v2 = my_graph.meta_forward_list[v1][0]
    return len(my_graph.meta_reverse_dict[v2])==1

def energize(v,my_graph,my_table):
    if v in my_table: return len(my_table[v])

    temp_vert, v_stack, vertex_group = v, [v], set()

    while can_contract(temp_vert,my_graph):
        temp_vert = my_graph.meta_forward_list[temp_vert][0]
        v_stack.append(temp_vert)

    for v_temp in v_stack:
        for q in my_graph.assigned_lookup[v_temp]:
            if my_graph.vertex_dict[q] is not None:
                vertex_group = vertex_group.union(my_graph.vertex_dict[q])

    for v2 in my_graph.meta_forward_dict[v_stack[-1]]:
        energize(v2,my_graph,my_table)
        vertex_group = vertex_group.union(my_table[v2])

    my_table[v] = vertex_group

    return len(my_table[v])


def solution02b(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    my_graph = build_graph(data)
    my_graph.build_metagraph()

    my_table = dict()

    v1 = energize(my_graph.assigned_dict[((0,0),east)],my_graph,my_table)

    v2 = 0
    for i in range(len(data)):
        v2 = max(v2,energize(my_graph.assigned_dict[((i,0),east)],my_graph,my_table))
        v2 = max(v2,energize(my_graph.assigned_dict[((i,len(data[0])-1),west)],my_graph,my_table))

    for j in range(len(data[0])):
        v2 = max(v2,energize(my_graph.assigned_dict[((0,j),south)],my_graph,my_table))
        v2 = max(v2,energize(my_graph.assigned_dict[((len(data)-1,j),north)],my_graph,my_table))

    if show_result: print(str(v1)+'\n'+str(v2))

    return v1, v2


def solution02a(show_result=True, fname='Input02.txt'):
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
    # solution01()
    # solution02a()
    solution02b()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

