#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList, UnionFind
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir


def parse_input01(fname):
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [' ',':','x'],type_lookup = None, allInt = False, allFloat = False)

    grid_list = []
    dimension_list = []
    quantity_list = []

    for i in range(len(data)-1):
        grid_list.append(data[i][1:])

    for i in range(len(grid_list)):
        old_grid = grid_list[i]

        new_grid = []

        for old_row in old_grid:
            new_row = []

            for c in old_row[0]:
                new_row.append(c)

            new_grid.append(new_row)

        grid_list[i] = new_grid


    for i in range(len(data[-1])):
        dimension_list.append(data[-1][i][0:2])
        quantity_list.append(data[-1][i][2:])

    for i in range(len(dimension_list)):
        for j in range(2):
            dimension_list[i][j] = int(dimension_list[i][j])

    for i in range(len(quantity_list)):
        for j in range(len(quantity_list[i])):
            quantity_list[i][j] = int(quantity_list[i][j])

    return grid_list, dimension_list, quantity_list

def serialize_shape(grid):
    v = 0
    for i in range(3):
        for j in range(3):
            v += (1<<(3*i+j))*(grid[i][j]=='#')
    return v

def deserialize_shape(shape):
    grid = []

    char_list = ['.','#']

    for i in range(3):
        row = []
        for j in range(3):
            b = (shape >> (3*i+j))&1
            row.append(char_list[b])

        grid.append(row)

    return grid

def compute_shape_area(grid):
    v = 0
    for i in range(3):
        for j in range(3):
            v+=(grid[i][j]=='#')

    return v

#op_code = 0 -> check if shape fits
#op_code = 1 -> insert shape
#op_code = 2 -> remove shape
def update_grid(grid,shape,i0,j0,op_code,shape_num = 1):

    can_fit = True

    for i in range(3):
        for j in range(3):
            b = (shape >> (3*i+j))&1
            can_fit = can_fit and  (not (b==1 and grid[i0+i][j0+j]!='.'))

            if b == 1 and op_code == 1:
                grid[i0+i][j0+j] = shape_num

            if b == 1 and op_code == 2:
                grid[i0+i][j0+j] = '.'

    return can_fit


def termination_heuristic01(h,w,i0,j0,shapes_remaining,shape_areas):
    required_area = 0

    for i in range(len(shapes_remaining)):
        required_area+=shapes_remaining[i]*shape_areas[i]

    available_area = 0
    available_area+=3*(h-i0)
    available_area+=h*(w-3-j0)

    return required_area<=available_area

def check_viability(h,w,i0,j0,shapes_remaining,shape_areas,code_list,grid = None):
    if sum(shapes_remaining)==0:
        return True

    if j0>=w-2:
        return False

    if not termination_heuristic01(h,w,i0,j0,shapes_remaining,shape_areas):
        return False

    if grid is None:
        grid = []
        for i in range(h):
            grid.append(['.']*w)


    i0_next = (i0+1)%(h-2)
    j0_next = j0 + (i0_next == 0)

    solution_found = False

    for k in range(len(shapes_remaining)):
        if shapes_remaining[k]==0:
            continue

        for code in code_list[k]:
            if not update_grid(grid,code,i0,j0,0):
                continue

            shapes_remaining[k]-=1
            update_grid(grid,code,i0,j0,1,chr(ord('A')+k))

            solution_found = check_viability(h,w,i0_next,j0_next,shapes_remaining,shape_areas,code_list,grid)

            shapes_remaining[k]+=1
            update_grid(grid,code,i0,j0,2)

            if solution_found: 
                return True

    solution_found = check_viability(h,w,i0_next,j0_next,shapes_remaining,shape_areas,code_list,grid)

    return solution_found

def solution(show_result=True, fname='Input02.txt'):
    sys.setrecursionlimit(4000)
    # sys.setrecursionlimit(1000)
   

    grid_list, dimension_list, quantity_list = parse_input01(fname)
    code_list = []
    shape_areas = []


    for i in range(len(grid_list)):
        code_set = set()
        
        grid = grid_list[i]
        grid_mirror = bh.reflect_grid(grid,0)

        shape_areas.append(compute_shape_area(grid))

        for j in range(4):
            code_set.add(serialize_shape(bh.rotate_grid(grid,j)))
            code_set.add(serialize_shape(bh.rotate_grid(grid_mirror,j)))

        code_list.append(list(code_set))

    total = 0
    for i in range(len(dimension_list)):
        h,w = dimension_list[i][0], dimension_list[i][1]
        i0, j0 = 0, 0

        shapes_remaining = quantity_list[i]

        if check_viability(h,w,i0,j0,shapes_remaining,shape_areas,code_list):
            total+=1

    if show_result:
        print(total)

    return total


if __name__ == '__main__':
    t0 = time.time()
    solution()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

