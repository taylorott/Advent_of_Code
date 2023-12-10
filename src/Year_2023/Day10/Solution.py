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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    #pad the grid with a ring of '.'
    data = [['.']*len(data[0])] + data + [['.']*len(data[0])]
    for i in range(len(data)):
        data[i] = ['.']+data[i]+['.']

    return data

horizontal_characters = {'F','7','L','J','S','-'}
vertical_characters = {'F','7','L','J','S','|'}
west_chars={'F','L','-','S'}
east_chars={'J','7','-','S'}
north_chars={'F','7','|','S'}
south_chars={'L','J','|','S'}

#given the character grid grid_in and
#vertices current_vert = (i_0,j_0) and neighbor_vert = (i_1,j_1)
#returns true if current_vert and neighbor_vert are pipe segments that
#are connected together, given their positions and pipe types
#(corresponds to adjaceny in the graph)
#returns false otherwise
def adjacency_criteria(grid_in,current_vert,neighbor_vert):
    i_0 = current_vert[0]
    j_0 = current_vert[1]
    i_1 = neighbor_vert[0]
    j_1 = neighbor_vert[1]

    char_0 = grid_in[i_0][j_0]
    char_1 = grid_in[i_1][j_1]

    horizontal_align = i_0 == i_1
    vertical_align = j_0 == j_1

    if vertical_align and char_0 in vertical_characters and char_1 in vertical_characters:
        if i_0<i_1 and char_0 in north_chars and char_1 in south_chars:
            return True
        if i_1<i_0 and char_1 in north_chars and char_0 in south_chars:
            return True

    if horizontal_align and char_0 in horizontal_characters and char_1 in horizontal_characters:
        if j_0<j_1 and char_0 in west_chars and char_1 in east_chars:
            return True
        if j_1<j_0 and char_1 in west_chars and char_0 in east_chars:
            return True

    return False

#replaces the s in the pipe with the pipe character that correctly connects to the rest of the loop
def replace_s_char(s_coord,grid_in):
    i = s_coord[0]
    j = s_coord[1]

    north_char = grid_in[i-1][j]
    south_char = grid_in[i+1][j]
    east_char = grid_in[i][j+1]
    west_char = grid_in[i][j-1]

    north_adjacent = north_char in north_chars
    south_adjacent = south_char in south_chars
    east_adjacent = east_char in east_chars
    west_adjacent = west_char in west_chars

    if north_adjacent and south_adjacent:
        grid_in[i][j]='|'

    if east_adjacent and west_adjacent:
        grid_in[i][j]='-'

    if north_adjacent and east_adjacent:
        grid_in[i][j]='L'

    if north_adjacent and west_adjacent:
        grid_in[i][j]='J'

    if south_adjacent and east_adjacent:
        grid_in[i][j]='F'

    if south_adjacent and west_adjacent:
        grid_in[i][j]='7'

#check if a given coordinate on the grid is enclosed by the pipe loop
#this function is only called when the input coordinate is not a part of the pipe loop
def test_enclosed(start_coord,grid_in,dist_dict):
    i = start_coord[0]
    j = start_coord[1]

    #we start from an exterior point (k,0)
    #note that we padded our with a ring of '.' characters,
    #so it is guaranteed that (k,j) is exterior to the loop (and not a part of the loop or an interior point)
    k = 0

    #true if we are on the interior of the loop
    on_interior = False

    #now, we walk "downards" from (k=0,j) to (k=i,j)
    while k<i:
        #move one step downwards. note that this corresponds to increasing k due to the sign convention of arrays
        k+=1

        #if we hit a portion of the pipe loop...
        if (k,j) in dist_dict:
            #if we hit a '-' segment, then we clearly are crossing from exterior to interior or visa versa
            if grid_in[k][j]=='-':
                #thus, flip on_interior
                on_interior = not on_interior

            #if we hit a 'F' or and '7'
            elif grid_in[k][j]=='F' or grid_in[k][j]=='7':
                start_char = grid_in[k][j]

                #continue until we hit a L or J
                while grid_in[k][j]!='L' and grid_in[k][j]!='J':
                    k+=1
                end_char = grid_in[k][j]

                #if what we vertically traversed was a big Z or S, we have crossed from exterior to interior or visa versa
                if (start_char=='F' and end_char=='J') or (start_char=='7' and end_char=='L'):
                    #thus, flip on_interior
                    on_interior = not on_interior
                #otherwise, we have vertically traversed a big C or backwards C, in which case, the number of flips was even
                #so on_interior remains the same

    return on_interior

def findLoop(grid_in):
    s_coord = None
    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(grid_in,adjacency_criteria=adjacency_criteria)

    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if grid_in[i][j] == 'S':
                s_coord = (i,j)

    replace_s_char(s_coord,grid_in)
    dist_dict = myGraph.compute_dist_BFS(s_coord)['dist_dict']

    return dist_dict

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    data = parse_input01(fname)
    
    dist_dict= findLoop(data)
  
    max_dist = 0

    for key in dist_dict:
        max_dist = max(max_dist,dist_dict[key])

    print(max_dist)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    data = parse_input01(fname)
    
    dist_dict= findLoop(data)

    
    enclosed_area = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if (i,j) not in dist_dict and test_enclosed((i,j),data,dist_dict):
                enclosed_area+=1

    print(enclosed_area)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

