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
    data = bh.parse_strings(path,fname,delimiters = [',','~'],type_lookup = None, allInt = True, allFloat = False)

    return data

def lower_brick(height_dict,brick_graph,brick):

    i = brick[0]
    j = brick[1]
    count = 0
    num_cubes = abs(brick[0]-brick[3])+abs(brick[1]-brick[4])+1

    supporting_height = 0
    supporting_block_set = set()



    while count<num_cubes or i!=brick[3] or j!=brick[4]:
        if (i,j) in height_dict:

            top_cube = height_dict[(i,j)]
            candidate_height = top_cube[0]
            cube_label = top_cube[1]

            if candidate_height==supporting_height:
                supporting_block_set.add(cube_label)

            elif candidate_height>supporting_height:
                supporting_height = candidate_height
                supporting_block_set = set()
                supporting_block_set.add(cube_label)

        if i<brick[3]:
            i+=1
        elif i>brick[3]:
            i-=1
        if j<brick[4]:
            j+=1
        elif j>brick[4]:
            j-=1

        count+=1

    min_z = min(brick[2],brick[5])

    brick[2]=brick[2]-min_z+supporting_height+1
    brick[5]=brick[5]-min_z+supporting_height+1

    new_supporting_height = max(brick[2],brick[5])

    for item in supporting_block_set:
        brick_graph.add_edge(item,brick[6])
    
    i = brick[0]
    j = brick[1]
    count = 0

    while count<num_cubes or i!=brick[3] or j!=brick[4]:
        height_dict[(i,j)]=[new_supporting_height,brick[6]]

        if i<brick[3]:
            i+=1
        elif i>brick[3]:
            i-=1
        if j<brick[4]:
            j+=1
        elif j>brick[4]:
            j-=1

        count+=1

def construct_brick_graph(brick_list):
    brick_heap = AugmentedHeap(useIndex_dict=False)

    for brick in brick_list:
        lowest_height = min(brick[2],brick[5])
        brick_heap.insert_item(lowest_height,brick)   

    height_dict = {}
    brick_graph = Digraph()

    while not brick_heap.isempty():
        dummy, next_brick = brick_heap.pop()
        lower_brick(height_dict,brick_graph,next_brick)

    return brick_graph


def find_supported_bricks(brick_graph,starting_brick):

    if starting_brick not in brick_graph.forward_adjacency:
        return 0

    total = 0

    moved_brick_set = set()
    moved_brick_set.add(starting_brick)

    brick_queue = deque()
    for item in brick_graph.forward_adjacency[starting_brick]:
        brick_queue.append(item)

    while len(brick_queue)>0:
        current_brick=brick_queue.popleft()
        is_still_supported = False

        for supporting_brick in brick_graph.reverse_adjacency[current_brick]:
            if supporting_brick not in moved_brick_set:
                is_still_supported = True
                break

        if not is_still_supported and current_brick not in moved_brick_set:
            total+=1
            moved_brick_set.add(current_brick)

            for item in brick_graph.forward_adjacency[current_brick]:
                brick_queue.append(item)

    return total


def solution():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    brick_list = parse_input01(fname)
    for i in range(len(brick_list)):
        brick_list[i].append(i)

    brick_graph = construct_brick_graph(brick_list)

    #part 1
    total = 0
    for i in range(len(brick_list)):
        if i not in brick_graph.forward_adjacency:
            total+=1
        else:
            can_remove = True
            for j in brick_graph.forward_adjacency[i]:
                if j in brick_graph.reverse_adjacency and len(brick_graph.reverse_adjacency[j])==1:
                    can_remove = False   
            if can_remove:
                total+=1

    print(total) 

    #part 2
    total = 0
    for i in range(len(brick_list)):
        total+=find_supported_bricks(brick_graph,i)

    print(total)





if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

