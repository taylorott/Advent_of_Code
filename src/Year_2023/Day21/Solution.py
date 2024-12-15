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
    return bh.parse_char_grid(path,fname)

def adjacency_criteria(grid_in,coord1,coord2):
    char1 = grid_in[coord1[0]][coord1[1]]
    char2 = grid_in[coord2[0]][coord2[1]]
    return char1!='#' and char2!='#'

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria=adjacency_criteria)

    coord_start = None

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='S':
                coord_start = (i,j)

    dist_dict = myGraph.compute_dist_BFS(coord_start)['dist_dict']

    total = 0
    for item in dist_dict:
        if dist_dict[item]%2==0 and dist_dict[item]<=64:
            total+=1
            
    if show_result: print(total)

    return total

def count_extra_periodic_plots_type1(num_steps,base_dist_1,base_dist_2):

    period = base_dist_2-base_dist_1
    steps_remaining = num_steps-base_dist_2

    if steps_remaining<=0:
        return 0

    q = steps_remaining//period

    if steps_remaining%2==0 and period%2==0:
        return q
    if steps_remaining%2==1 and period%2==0:
        return 0
    if steps_remaining%2==0 and period%2==1:
        return q//2
    if steps_remaining%2==1 and period%2==1:
        return (q+1)//2

#counts how many (0<=a,0<=b) exist such that
# d+a*h+b*w<=steps_remaining
# a*h+b*w<=steps_remaining-d
#
# d+a*h+b*w congruent to steps_remaining (mod 2)
# a*h+b*w congruent to steps_remaining-d (mod 2)
def step_counting_helper(steps_remaining,d,h,w):
    steps_remaining-=d

    if steps_remaining<0:
        return 0

    if h%2==1 and w%2==1 and w==h:
        q = h

        if steps_remaining%2==1:
            steps_remaining-=q

            if steps_remaining<0:
                return 0


            q*=2

            total=1+(steps_remaining//q)

            return (total*(total+1))

        else:
            q*=2

            subtotal1 = 1+(steps_remaining//q)
            subtotal1 = (subtotal1*(subtotal1+1))//2


            steps_remaining-=q

            subtotal2 = 0
            if steps_remaining>=0:
                subtotal2 = 1+(steps_remaining//q)
                subtotal2 = (subtotal2*(subtotal2+1))//2

            return subtotal1 + subtotal2

def count_extra_periodic_plots_type2(grid_in, num_steps,corner_base_dist,corner_dist_dict,h,w):
    total = 0

    steps_remaining=num_steps-corner_base_dist

    if steps_remaining<0:
        return 0

    for i in range(h):
        for j in range(w):
            if (i,j) in corner_dist_dict:
                d = corner_dist_dict[(i,j)]
                total += step_counting_helper(steps_remaining,d,h,w)

    return total

def test_on_large_repeat_graph(data,num_steps):
    h = len(data)
    w = len(data[0])    

    coord_start = None

    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='S':
                coord_start = (i,j)

    repeat_factor = 51

    repeat_grid = []
    temp = []

    for i in range(len(data)):
        temp_line = []
        for j in range(repeat_factor):
            temp_line+=data[i]
        temp.append(temp_line)

    for i in range(repeat_factor):
        repeat_grid+=temp

    center_coord_start = (coord_start[0]+h*(repeat_factor//2),coord_start[1]+w*(repeat_factor//2))

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(repeat_grid,adjacency_criteria=adjacency_criteria)

    dist_dict = myGraph.compute_dist_BFS(center_coord_start)['dist_dict']

    total = 0
    total_corner = 0
    total_base = 0
    for item in dist_dict:
        if dist_dict[item]%2==0 and dist_dict[item]<=num_steps:
            total+=1

            i = item[0]
            j = item[1]

            if ((i<h*(repeat_factor//2) or h*(1+repeat_factor//2)<=i) and 
                (j<w*(repeat_factor//2) or w*(1+repeat_factor//2)<=j)):
                total_corner+=1

            if ((i>=h*(repeat_factor//2) and h*(1+repeat_factor//2)>i) and 
                (j>=w*(repeat_factor//2) and w*(1+repeat_factor//2)>j)):
                total_base+=1


    print(total,total_corner,total_base)


def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    num_steps = 26501365

    # test_on_large_repeat_graph(data,num_steps)

    coord_start = None

    h = len(data)
    w = len(data[0])

    for i in range(h):
        for j in range(w):
            if data[i][j]=='S':
                coord_start = (i,j)




    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria=adjacency_criteria)

    NW_corner = (0,0)
    NE_corner = (0,w-1)
    SW_corner = (h-1,0)
    SE_corner = (h-1,w-1)

    base_dist_dict = myGraph.compute_dist_BFS(coord_start)['dist_dict'] 
    NW_dist_dict = myGraph.compute_dist_BFS(NW_corner)['dist_dict']
    NE_dist_dict = myGraph.compute_dist_BFS(NE_corner)['dist_dict']
    SW_dist_dict = myGraph.compute_dist_BFS(SW_corner)['dist_dict']
    SE_dist_dict = myGraph.compute_dist_BFS(SE_corner)['dist_dict']


    NW_base_dist = base_dist_dict[SE_corner]+2
    NE_base_dist = base_dist_dict[SW_corner]+2
    SW_base_dist = base_dist_dict[NE_corner]+2
    SE_base_dist = base_dist_dict[NW_corner]+2


    total = 0

    total+=count_extra_periodic_plots_type2(data, num_steps,NW_base_dist,NW_dist_dict,h,w)
    total+=count_extra_periodic_plots_type2(data, num_steps,NE_base_dist,NE_dist_dict,h,w)
    total+=count_extra_periodic_plots_type2(data, num_steps,SW_base_dist,SW_dist_dict,h,w)
    total+=count_extra_periodic_plots_type2(data, num_steps,SE_base_dist,SE_dist_dict,h,w)

    repeat_factor = 41

    wide_grid = []

    for i in range(h):
        repeat_line = []

        for j in range(repeat_factor):
            repeat_line+=data[i]

        wide_grid.append(repeat_line)

    start_coord_wide = (coord_start[0],coord_start[1]+w*(repeat_factor//2))

    wide_Graph = Graph()
    wide_Graph.build_graph_from_2D_grid(wide_grid,adjacency_criteria=adjacency_criteria)
    wide_dist_dict = wide_Graph.compute_dist_BFS(start_coord_wide)['dist_dict']


    tall_grid = []

    for i in range(repeat_factor):
        tall_grid+=data

    start_coord_tall = (coord_start[0]+h*(repeat_factor//2),coord_start[1])

    tall_Graph = Graph()
    tall_Graph.build_graph_from_2D_grid(tall_grid,adjacency_criteria=adjacency_criteria)
    tall_dist_dict = tall_Graph.compute_dist_BFS(start_coord_tall)['dist_dict']

    for i in range(len(tall_grid)):
        for j in range(w):
            if (i,j) in tall_dist_dict:
                d = tall_dist_dict[(i,j)]
                if d%2==num_steps%2 and d<=num_steps:
                    total+=1

    for i in range(h):
        for j in range(len(wide_grid[0])):
            if (i,j) in wide_dist_dict:
                d = wide_dist_dict[(i,j)]
                if d%2==num_steps%2 and d<=num_steps:
                    total+=1

    subtotal_base = 0
    for i in range(h):
        for j in range(w):
            if (i,j) in base_dist_dict:
                d = base_dist_dict[(i,j)]
                if d%2==num_steps%2 and d<=num_steps:
                    total-=1
                    subtotal_base+=1

    for i in range(h):
        for j in range(w):
            if (i,j) in base_dist_dict:
                coord_N = (i+h,j)
                coord_NN = (i,j)
                coord_S = (i+(repeat_factor-2)*h,j)
                coord_SS = (i+(repeat_factor-1)*h,j)

                coord_E = (i,j+(repeat_factor-2)*w)
                coord_EE = (i,j+(repeat_factor-1)*w)
                coord_W = (i,j+w)
                coord_WW = (i,j)

                total+=count_extra_periodic_plots_type1(num_steps,tall_dist_dict[coord_N],tall_dist_dict[coord_NN])
                total+=count_extra_periodic_plots_type1(num_steps,tall_dist_dict[coord_S],tall_dist_dict[coord_SS])

                total+=count_extra_periodic_plots_type1(num_steps,wide_dist_dict[coord_E],wide_dist_dict[coord_EE])
                total+=count_extra_periodic_plots_type1(num_steps,wide_dist_dict[coord_W],wide_dist_dict[coord_WW])    

    if show_result: print(total)

    return total




if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

