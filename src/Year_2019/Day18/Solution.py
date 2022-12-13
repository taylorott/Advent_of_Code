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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    for i in range(len(data)):
        data[i] = bh.block_to_grid(data[i])
        number_entrances(data[i])
    return data

def number_entrances(grid_in):
    count = 0
    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if grid_in[i][j]=='@':
                grid_in[i][j]=str(count)
                count+=1

def adjacency_criteria(grid_in,vert0,vert1):
    c0 = grid_in[vert0[0]][vert0[1]]
    c1 = grid_in[vert1[0]][vert1[1]]


    return c0!='#' and c1!='#'

def can_vist(next_char,current_key_set_set,doors_in_path_dict,entrance_tuple):
    for entrance in entrance_tuple:
        test_bool = True
        for door in doors_in_path_dict[entrance][next_char]:
            test_bool = test_bool and (door in current_key_set_set)
        if test_bool:
            return True

    return False


def solve_grid(grid):

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(grid,adjacency_criteria=adjacency_criteria)

    coord_dict = {}
    char_dict = {}
    path_data_dict = {}

    doors_dict = {}
    vertex_dict = {}

    dist_dict = {}
    entrance_list = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            my_char = grid[i][j]
            current_coord = (i,j)
            char_dict[current_coord]=my_char

            if ('0'<=my_char and my_char<='9') or ('a'<=my_char and my_char<='z'):
                coord_dict[my_char]=current_coord
                path_data_dict[my_char] = myGraph.compute_dist_BFS(current_coord)
                vertex_dict[my_char]=None

            if 'A'<=my_char and my_char<='Z':
                doors_dict[my_char]=None

            if ('0'<=my_char and my_char<='9'):
                entrance_list.append(my_char)
    entrance_list.sort()
    entrance_tuple = tuple(entrance_list)

    doors_in_path_dict = {}
    for key0 in vertex_dict.keys():
        dist_dict[key0] = {}

        doors_in_path_dict[key0]={}
        for key1 in vertex_dict.keys():
            doors_in_path_dict[key0][key1]={}

            if key0!=key1:
                temp_dict = {}
                current_vert = coord_dict[key1]

                if current_vert in path_data_dict[key0]['dist_dict']:
                    dist_dict[key0][key1]=path_data_dict[key0]['dist_dict'][current_vert]

                    while current_vert is not None:
                        current_char = char_dict[current_vert]
                        if current_char in doors_dict:
                            doors_in_path_dict[key0][key1][current_char.lower()]=None

                        current_vert = path_data_dict[key0]['predecessor_dict'][current_vert]
                else:
                    dist_dict[key0][key1]=np.inf
                    doors_in_path_dict[key0][key1]['*']=None

    
    key_list = []
    for key in vertex_dict.keys():
        key_list.append(key)

    key_list.sort()
    final_tuple = tuple(key_list)

    lookup_table = {}
    lookup_table[entrance_tuple] = {}
    lookup_table[entrance_tuple][entrance_tuple]=0

    my_queue = deque()
    my_queue.append(entrance_tuple)

    while len(my_queue)!=0:
        current_key_set_tuple = my_queue.popleft()
        current_key_set_list = list(current_key_set_tuple) 
        current_key_set_set = set(current_key_set_list)

        for next_char in vertex_dict.keys():
            if next_char not in current_key_set_set and can_vist(next_char,current_key_set_set,doors_in_path_dict,entrance_tuple):

                next_list = list(current_key_set_list)
                next_list.append(next_char)
                next_list.sort()
                next_tuple = tuple(next_list)

                if next_tuple not in lookup_table:
                    my_queue.append(next_tuple)
                    lookup_table[next_tuple] = {}

                for start_state in lookup_table[current_key_set_tuple].keys():

                    for i in range(len(start_state)):
                        start_char = start_state[i]
                        if dist_dict[start_char][next_char]<np.inf:

                            next_state_list = list(start_state)
                            next_state_list[i]=next_char
                            next_state_tuple = tuple(next_state_list)

                            dist = lookup_table[current_key_set_tuple][start_state]+dist_dict[start_char][next_char]

                            if next_state_tuple not in lookup_table[next_tuple]:
                                lookup_table[next_tuple][next_state_tuple]=dist
                            else:
                                lookup_table[next_tuple][next_state_tuple] = min(dist,lookup_table[next_tuple][next_state_tuple])


    min_dist = np.inf

    for state_tuple in lookup_table[final_tuple]:
        min_dist = min(min_dist,lookup_table[final_tuple][state_tuple])


    print(min_dist)



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    for grid in data:
        solve_grid(grid)


def solution02():
    # fname = 'Input03.txt'
    fname = 'Input04.txt'

    data = parse_input01(fname)

    for grid in data:
        solve_grid(grid)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))