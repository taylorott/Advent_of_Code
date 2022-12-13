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

    return data

def adjacency_criteria(grid_in,vert0,vert1):
    c0 = grid_in[vert0[0]][vert0[1]]
    c1 = grid_in[vert1[0]][vert1[1]]


    return c0!='#' and c1!='#'

def can_vist(next_char,current_set,doors_in_path_dict):
    for door in doors_in_path_dict['@'][next_char]:
        if door not in current_set:
            return False

    return True


def solve_grid_01(grid):

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(grid,adjacency_criteria=adjacency_criteria)

    coord_dict = {}
    char_dict = {}
    path_data_dict = {}

    doors_dict = {}
    vertex_dict = {}

    dist_dict = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            my_char = grid[i][j]
            current_coord = (i,j)
            char_dict[current_coord]=my_char
            if my_char!='.' and my_char!='#':
                coord_dict[my_char]=current_coord
                
                path_data_dict[my_char] = myGraph.compute_dist_BFS(current_coord)

            if my_char=='@' or ('a'<=my_char and my_char<='z'):
                vertex_dict[my_char]=None

            if 'A'<=my_char and my_char<='Z':
                doors_dict[my_char]=None


    doors_in_path_dict = {}
    num_doors_in_path = {}
    for key0 in vertex_dict.keys():
        dist_dict[key0] = {}

        doors_in_path_dict[key0]={}
        num_doors_in_path[key0]={}
        starting_vert = coord_dict[key0]
        for key1 in vertex_dict.keys():
            doors_in_path_dict[key0][key1]={}
            num_doors_in_path[key0][key1]=0

            if key0!=key1:
                temp_dict = {}
                current_vert = coord_dict[key1]
                dist_dict[key0][key1]=path_data_dict[key0]['dist_dict'][current_vert]

                while current_vert is not None:
                    current_char = char_dict[current_vert]
                    if current_char in doors_dict:
                        doors_in_path_dict[key0][key1][current_char.lower()]=None
                        num_doors_in_path[key0][key1]+=1

                    current_vert = path_data_dict[key0]['predecessor_dict'][current_vert]

    lookup_table = {}
    key_list = []
    for key in vertex_dict.keys():
        lookup_table[key]={}
        key_list.append(key)

    key_list.sort()
    final_tuple = tuple(key_list)

    lookup_table[('@')]['@']=0
    my_queue = deque()
    my_queue.append(('@'))

    while len(my_queue)!=0:
        current_tuple = my_queue.popleft()
        current_list = list(current_tuple) 
        current_set = set(current_list)

        for next_char in vertex_dict.keys():
            if next_char not in current_set and can_vist(next_char,current_set,doors_in_path_dict):
                dist = np.inf

                next_list = list(current_list)
                next_list.append(next_char)
                next_list.sort()
                next_tuple = tuple(next_list)

                for start_char in current_list:
                    if start_char in lookup_table[current_tuple]:
                        temp_dist = lookup_table[current_tuple][start_char]+dist_dict[start_char][next_char]
                        dist = min(dist,temp_dist)

                if next_tuple not in lookup_table:
                    my_queue.append(next_tuple)
                    lookup_table[next_tuple] = {}

                lookup_table[next_tuple][next_char]=dist


    min_dist = np.inf

    for final_char in lookup_table[final_tuple]:
        min_dist = min(min_dist,lookup_table[final_tuple][final_char])


    print(min_dist)



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    for grid in data:
        solve_grid_01(grid)


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

