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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [',',' '],type_lookup = None, allInt = True, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data



def update_regions(dist_grid,area_dict,coord_list,coord_in):
    
    min_dist = None
    nearest_coord = None

    for test_coord in coord_list:
        d = bh.manhattan_distance(coord_in,test_coord)

        if min_dist is None or d < min_dist:
            min_dist = d
            nearest_coord = test_coord
            
        elif d == min_dist:
            nearest_coord = None

    dist_grid[coord_in] = nearest_coord

    if nearest_coord in area_dict:
        area_dict[nearest_coord]+=1
    else:
        area_dict[nearest_coord]=1



def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    coord_list = parse_input01(fname)[0]
    coord_list_T = np.transpose(coord_list)

    for i in range(len(coord_list)):
        coord_list[i]=tuple(coord_list[i])
    
    min_x = min(coord_list_T[0])
    max_x = max(coord_list_T[0])
    min_y = min(coord_list_T[1])
    max_y = max(coord_list_T[1])


    dist_grid = dict()
    area_dict = dict()

    boundary_coords = set()

    for x in range(min_x-1,max_x+2):
        for y in range(min_y-1,max_y+2):
            coord_in = (x,y)
            update_regions(dist_grid,area_dict,coord_list,coord_in)

            if x==min_x-1 or x==max_x+1 or y==min_y-1 or y==max_y+1:
                boundary_coords.add(dist_grid[coord_in])

    max_area = 0

    for test_coord in coord_list:
        if test_coord is not None and test_coord not in boundary_coords:
            max_area = max(max_area,area_dict[test_coord])

    print(max_area)
    
    coord_mat = np.array(coord_list_T)

    max_dist_sum = 10000

    x_dist_dict = dict()
    y_dist_dict = dict()

    for x in range(min_x,max_x+1):
        x_dist_dict[x] = np.sum(np.abs(coord_mat[0]-x))

    for y in range(min_y,max_y+1):
        y_dist_dict[y] = np.sum(np.abs(coord_mat[1]-y))

    x = max_x+1
    while x_dist_dict[x-1]<max_dist_sum:
        x_dist_dict[x]=x_dist_dict[x-1]+len(coord_list)
        x+=1

    y = max_y+1
    while y_dist_dict[y-1]<max_dist_sum:
        y_dist_dict[y]=y_dist_dict[y-1]+len(coord_list)
        y+=1

    x = min_x-1
    while x_dist_dict[x+1]<max_dist_sum:
        x_dist_dict[x]=x_dist_dict[x+1]+len(coord_list)
        x-=1

    y = min_y-1
    while y_dist_dict[y+1]<max_dist_sum:
        y_dist_dict[y]=y_dist_dict[y+1]+len(coord_list)
        y-=1

    area = 0

    for x in x_dist_dict:
        for y in y_dist_dict:
            if x_dist_dict[x]+y_dist_dict[y]<max_dist_sum:
                area+=1
    print(area)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

