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
    data = bh.parse_strings(path,fname,delimiters = [','],type_lookup = None, allInt = True, allFloat = False)

    return data

def compute_area(c1,c2):
    dx = abs(c1[0]-c2[0])+1
    dy = abs(c1[1]-c2[1])+1
    return dx*dy

def compute_area_transformed_coords(coord1,coord2,x_lookup,y_lookup):
    return compute_area(transform_coord(coord1,x_lookup,y_lookup),
                        transform_coord(coord2,x_lookup,y_lookup))

def transform_coord(coord,x_lookup,y_lookup):
    return (x_lookup[coord[0]],y_lookup[coord[1]])

def construct_coord_lookups(coord_list):
    x_set, y_set = set(), set()
    
    for coord in coord_list:
        for i in range(-1,2):
            x_set.add(coord[0]+i)
            y_set.add(coord[1]+i)

    x_forward, y_forward = sorted(list(x_set)), sorted(list(y_set))
    
    x_reverse, y_reverse = dict(), dict()

    n = len(coord_list)

    for i in range(len(x_forward)):
        x_reverse[x_forward[i]] = i

    for i in range(len(y_forward)):
        y_reverse[y_forward[i]] = i

    coord_list_transformed = []
    for coord in coord_list:
        coord_list_transformed.append(transform_coord(coord,x_reverse,y_reverse))

    return x_forward, x_reverse, y_forward, y_reverse, coord_list_transformed

delta_list = [(1,0),(-1,0),(0,1),(0,-1)]
def flood_fill(grid):
    w = len(grid)
    h = len(grid[0])
    todo_list = [(0,0)]

    while len(todo_list)>0:       
        coord = todo_list.pop()
        grid[coord[0]][coord[1]]=False
        
        for delta in delta_list:
            next_coord = (coord[0]+delta[0],coord[1]+delta[1])

            if (0<=next_coord[0] and 
                next_coord[0]<w  and 
                0<=next_coord[1] and
                next_coord[1]<h  and
                grid[next_coord[0]][next_coord[1]] is None):

                todo_list.append(next_coord)

    for i in range(w):
        for j in range(h):
            if grid[i][j] is None:
                grid[i][j] = True


def directional_increment(coord,coord_target):
    x = coord[0]+np.sign(coord_target[0]-coord[0])
    y = coord[1]+np.sign(coord_target[1]-coord[1])
    return (x,y)


def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    area = 0
    for i in range(len(data)):
        for j in range(i+1,len(data)):
            area = max(area,compute_area(data[i],data[j]))
    
    if show_result:
        print(area)
    return area

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    x_forward, x_reverse, y_forward, y_reverse, coord_list_transformed = construct_coord_lookups(data)

    n = len(data)

    w = len(x_forward)
    h = len(y_forward)

    fill_set = set()
    grid = []
    bottom_dict = []

    for i in range(w):
        grid.append([None]*h)
        bottom_dict.append([None]*h)

    for i in range(n):
        coord = coord_list_transformed[i]
        coord_target = coord_list_transformed[(i+1)%n]

        fill_set.add(coord)
        grid[coord[0]][coord[1]]=True
        while coord!=coord_target:
            coord = directional_increment(coord,coord_target)
            grid[coord[0]][coord[1]]=True
            fill_set.add(coord)

    flood_fill(grid)

    for i in range(len(x_forward)):
        bottom_most_coord = None
        for j in range(len(y_forward)):
            
            if grid[i][j]:
                if bottom_most_coord is None:
                    bottom_most_coord = j
                bottom_dict[i][j] = bottom_most_coord
            else:
                bottom_most_coord = None
                bottom_dict[i][j] = np.inf

    coords_sorted = sorted(coord_list_transformed, key=lambda item: item[0]*h+item[1])

    area = 0
    for i in range(len(coords_sorted)):
        coord1 = coords_sorted[i]
        x1, y1, x = coord1[0], coord1[1], coord1[0]

        max_bottom = bottom_dict[x1][y1]
        for j in range(len(coords_sorted)):
            coord2 = coords_sorted[j]
            x2, y2 = coord2[0], coord2[1]

            if x2<x1:
                continue

            while x<x2:
                x+=1
                max_bottom = max(max_bottom,bottom_dict[x][y1])

            if max_bottom<=y2 and y2<=y1:
                area = max(area,compute_area_transformed_coords(coord1,coord2,x_forward,y_forward))

    for i in range(len(coords_sorted)-1,-1,-1):
        coord1 = coords_sorted[i]
        x1, y1, x = coord1[0], coord1[1], coord1[0]

        max_bottom = bottom_dict[x1][y1]
        for j in range(len(coords_sorted)-1,-1,-1):
            coord2 = coords_sorted[j]
            x2, y2 = coord2[0], coord2[1]

            if x2>x1:
                continue

            while x>x2:
                x-=1
                max_bottom = max(max_bottom,bottom_dict[x][y1])

            if max_bottom<=y2 and y2<=y1:
                area = max(area,compute_area_transformed_coords(coord1,coord2,x_forward,y_forward))

    if show_result:
        print(area)
    return area


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

