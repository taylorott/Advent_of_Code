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

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = ['p','=','v',',',' '],type_lookup = None, allInt = True, allFloat = False)

    return data

def update(robot_list,w=101,h=103):
    for robot in robot_list:
        robot[0]=(robot[0]+robot[2])%w
        robot[1]=(robot[1]+robot[3])%h

def count_robot_list(robot_list,w=101,h=103):
    q1, q2, q3, q4 = 0, 0, 0, 0

    for robot in robot_list:
        x, y = robot[0], robot[1]

        if x<w//2 and y<h//2: q1+=1

        if x>w//2 and y<h//2: q2+=1

        if x<w//2 and y>h//2: q3+=1

        if x>w//2 and y>h//2: q4+=1

    return q1*q2*q3*q4

def print_robot_list(robot_list,w=101,h=103):
    grid = []

    for i in range(h): grid.append(['.']*w)

    for robot in robot_list: grid[robot[1]][robot[0]] = '#'

    bh.print_char_matrix(grid)

def draw_line_from_coord(start_coord,robot_coords,visited_set):
    if start_coord in visited_set: return 0
        
    count = -1
    visited_set.add(start_coord)
    current_coord = start_coord
    while current_coord in robot_coords:
        count+=1
        visited_set.add(current_coord)
        current_coord = (current_coord[0],current_coord[1]+1)

    current_coord = start_coord
    while current_coord in robot_coords:
        count+=1
        visited_set.add(current_coord)
        current_coord = (current_coord[0],current_coord[1]-1)
    return count

def vertical_line_detection(robot_list):
    robot_coords, visited_set = set(), set()

    for robot in robot_list: robot_coords.add((robot[0],robot[1]))
        
    l = 0
    for coord in robot_coords:
        l = max(l,draw_line_from_coord(coord,robot_coords,visited_set))

    return l

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    w, h = 101, 103

    n = 100
    for i in range(100):
        update(data,w,h)

    result = count_robot_list(data,w,h)

    if show_result: print(result)
    
    return result

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    w, h = 101, 103

    count = 0
    while vertical_line_detection(data)<8:
        update(data,w,h)
        count+=1

    if show_result:print(count)

    return count
    
if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

