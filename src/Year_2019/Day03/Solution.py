#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd

path = currentdir

direction_dict = {'R':np.array([1,0]),'L':np.array([-1,0]),'U':np.array([0,1]),'D':np.array([0,-1])}

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[','])

    return data

def build_path(move_list):
    coords = np.array([0,0])

    path_list = []

    path_list.append(np.array(coords))

    for item in move_list:
        direction = direction_dict[item[0]]
        magnitude = int(item[1:])
        coords+=magnitude*direction
        path_list.append(np.array(coords))

    return path_list

def check_intersection(p0,p1,p2,p3):
    dx0 = abs(p0[0]-p1[0])
    dy0 = abs(p0[1]-p1[1])
    dx1 = abs(p2[0]-p3[0])
    dy1 = abs(p2[1]-p3[1])

    if dx0==0 and dx1==0:
        return None

    if dy0==0 and dy1==0:
        return None

    x = None
    xmin = None
    xmax = None
    y = None
    ymin = None
    ymax = None

    if dx0==0:
        x = p0[0]
        xmin = min(p2[0],p3[0])
        xmax = max(p2[0],p3[0])
    else:
        x = p2[0]
        xmin = min(p0[0],p1[0])
        xmax = max(p0[0],p1[0])

    if dy0==0:
        y = p0[1]
        ymin = min(p2[1],p3[1])
        ymax = max(p2[1],p3[1])
    else:
        y = p2[1]
        ymin = min(p0[1],p1[1])
        ymax = max(p0[1],p1[1]) 

    if xmin<=x and x<=xmax and ymin<=y and y<=ymax:
        return np.array([x,y])
    else:
        return None       

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    
    path_list0 = build_path(data[0])
    path_list1 = build_path(data[1])

    min_dist = None
    for i in range(len(path_list0)-1):
        for j in range(1,len(path_list1)-1):
            temp_coords = check_intersection(path_list0[i],path_list0[i+1],path_list1[j],path_list1[j+1])
            if temp_coords is not None:
                if min_dist is None:
                    min_dist = abs(temp_coords[0])+abs(temp_coords[1])
                else:
                    min_dist = min(min_dist,abs(temp_coords[0])+abs(temp_coords[1]))
    for i in range(1,len(path_list0)-1):
        for j in range(len(path_list1)-1):
            temp_coords = check_intersection(path_list0[i],path_list0[i+1],path_list1[j],path_list1[j+1])
            if temp_coords is not None:
                if min_dist is None:
                    min_dist = abs(temp_coords[0])+abs(temp_coords[1])
                else:
                    min_dist = min(min_dist,abs(temp_coords[0])+abs(temp_coords[1]))
    print(min_dist)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    
    path_list0 = build_path(data[0])
    path_list1 = build_path(data[1])

    min_dist = None

    dist0 = 0
    for i in range(len(path_list0)-1):
        dist1 = 0
        for j in range(len(path_list1)-1):
            temp_coords = check_intersection(path_list0[i],path_list0[i+1],path_list1[j],path_list1[j+1])
            if temp_coords is not None:
                temp_dist = (dist0+dist1+
                            abs(temp_coords[0]-path_list1[j][0])+abs(temp_coords[1]-path_list1[j][1])+
                            abs(temp_coords[0]-path_list0[i][0])+abs(temp_coords[1]-path_list0[i][1]))

                if min_dist is None:
                    if temp_dist != 0:
                        min_dist = temp_dist
                else:
                    if temp_dist != 0:
                        min_dist = min(min_dist,temp_dist)
            dist1+=abs(path_list1[j+1][0]-path_list1[j][0])+abs(path_list1[j+1][1]-path_list1[j][1])
        dist0+=abs(path_list0[i+1][0]-path_list0[i][0])+abs(path_list0[i+1][1]-path_list0[i][1])

    print(min_dist)

if __name__ == '__main__':
    solution01()
    solution02()
    

