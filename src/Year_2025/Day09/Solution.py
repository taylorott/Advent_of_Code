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

def compute_winding(coord_list):
    n = len(coord_list)
    total = 0
    for i in range(n):
        j = (i+1)%n
        k = (i+2)%n

        dx1 = coord_list[j][0]-coord_list[i][0]
        dy1 = coord_list[j][1]-coord_list[i][1]

        dx2 = coord_list[k][0]-coord_list[j][0]
        dy2 = coord_list[k][1]-coord_list[j][1]


        total+=np.sign(dx1*dy2-dy1*dx2)

    return round(total/4)

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

def flood_fill(start_coord,fill_set):
    todo_list = [start_coord]

    while len(todo_list)>0:       
        coord = todo_list.pop()
        fill_set.add(coord)

        for delta in delta_list:
            next_coord = (coord[0]+delta[0],coord[1]+delta[1])

            if next_coord not in fill_set:
                todo_list.append(next_coord)

def run_flood_fill(coord_list,fill_set):
    winding = compute_winding(coord_list)

    n = len(coord_list)
    for i in range(n):
        j = (i+1)%n
        k = (i+2)%n

        dx1 = coord_list[j][0]-coord_list[i][0]
        dy1 = coord_list[j][1]-coord_list[i][1]
        dx2 = coord_list[k][0]-coord_list[j][0]
        dy2 = coord_list[k][1]-coord_list[j][1]

        turn = np.sign(dx1*dy2-dy1*dx2)

        if turn == winding:
            x = coord_list[j][0]+np.sign(dx2)-np.sign(dx1)
            y = coord_list[j][1]+np.sign(dy2)-np.sign(dy1)

            flood_fill((x,y),fill_set)

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

    fill_set = set()

    for i in range(n):
        coord = coord_list_transformed[i]
        coord_target = coord_list_transformed[(i+1)%n]

        fill_set.add(coord)
        while coord!=coord_target:
            coord = directional_increment(coord,coord_target)
            fill_set.add(coord)

    run_flood_fill(coord_list_transformed,fill_set)

    bottom_dict = dict()
    for i in range(len(x_forward)):
        bottom_most_coord = None
        for j in range(len(y_forward)):
            if (i,j) in fill_set:
                if bottom_most_coord is None:
                    bottom_most_coord = j
                bottom_dict[(i,j)] = bottom_most_coord
            else:
                bottom_most_coord = None
                bottom_dict[(i,j)] = np.inf

    area = 0
    for i in range(len(coord_list_transformed)):
        coord1 = coord_list_transformed[i]
        for j in range(i+1,len(coord_list_transformed)):
            coord2 = coord_list_transformed[j]

            y_bottom = min(coord1[1],coord2[1])
            y_top = max(coord1[1],coord2[1])

            is_full = True
            for x in range(min(coord1[0],coord2[0]),max(coord1[0],coord2[0])+1):
                if bottom_dict[(x,y_top)]>y_bottom:
                    is_full = False
                    break

            if is_full:
                area = max(area,compute_area_transformed_coords(coord1,coord2,x_forward,y_forward))

    if show_result:
        print(area)
    return area


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

