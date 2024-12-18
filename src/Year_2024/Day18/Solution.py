#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

up, down, left, right = (-1,0), (1,0), (0,-1), (0,1)

direction_list = [up,down,left,right]

def in_bounds(coord,l):
    return 0<=coord[0] and coord[0]<=l and 0<=coord[1] and coord[1]<=l

def coord_addition(coord1,coord2): return (coord1[0]+coord2[0],coord1[1]+coord2[1])

def parse_input01(fname):
    blocked_list =  bh.parse_extract_ints(path,fname)
    for i in range(len(blocked_list)): blocked_list[i] = tuple(blocked_list[i])

    return blocked_list

def bfs(start_coord, target_coord, blocked_set,l):
    my_queue = deque()

    my_queue.append(start_coord)

    visited_set, dist_dict = set(), dict()
    dist_dict[start_coord]=0

    while len(my_queue)>0:
        current_coord = my_queue.popleft()

        if current_coord not in visited_set:
            visited_set.add(current_coord)

            if current_coord==target_coord: return dist_dict[current_coord]

            for temp_dir in direction_list:
                next_coord = coord_addition(current_coord,temp_dir)

                if next_coord not in visited_set and next_coord not in blocked_set and in_bounds(next_coord,l):
                    dist_dict[next_coord]=dist_dict[current_coord]+1
                    my_queue.append(next_coord)
    return None

def get_distance(num_blocked, blocked_list,l):
    blocked_set = set(blocked_list[0:num_blocked])
    return bfs((0,0), (l,l), blocked_set, l)

def binary_search(blocked_list,l):
    if get_distance(0, blocked_list,l) is None: return None
    if get_distance(len(blocked_list), blocked_list,l) is not None: return None

    left_val = 0
    right_val = len(blocked_list)-1

    while left_val+1<right_val:
        mid_val = (left_val+right_val)//2

        if get_distance(mid_val, blocked_list,l) is None: right_val = mid_val

        else: left_val = mid_val

    return right_val

def solution(show_result=True, fname='Input02.txt'):
    blocked_list = parse_input01(fname)


    l, num_blocked = None, None
    if fname=='Input01.txt': l, num_blocked = 6, 12
    else: l, num_blocked = 70, 1024

    
    v1 = get_distance(num_blocked, blocked_list,l)

    my_index = binary_search(blocked_list,l)-1

    v2 = str(blocked_list[my_index][0])+','+str(blocked_list[my_index][1])

    if show_result: print(str(v1)+'\n'+v2)

    return v1, v2

if __name__ == '__main__':
    t0 = time.time()
    solution()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

