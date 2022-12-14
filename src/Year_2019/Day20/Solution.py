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

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    for i in range(len(data)):
        data[i] = bh.block_to_grid(data[i])
    return data

def adjacency_criteria(grid_in,coord0,coord1):
    return grid_in[coord0[0]][coord0[1]]=='.' and grid_in[coord1[0]][coord1[1]]=='.'

dir_list = [[1,0],[-1,0],[0,-1],[0,1]]


def identify_donut_boundaries(grid_in):
    i_min = np.inf
    i_max = -np.inf
    j_min = np.inf
    j_max = -np.inf

    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if grid_in[i][j]=='#':
                i_min = min(i_min,i)
                i_max = max(i_max,i)
                j_min = min(j_min,j)
                j_max = max(j_max,j)

    return i_min,i_max,j_min,j_max

def build_metagraph(grid_in):
    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(grid_in,adjacency_criteria=adjacency_criteria)

    i_min,i_max,j_min,j_max = identify_donut_boundaries(grid_in)

    l0 = len(grid_in)
    l1 = len(grid_in[0])

    inner_portal_dict = {}
    outer_portal_dict = {}
    portal_lookup = {}
    paired_portal_lookup = {}

    start_coord = None
    end_coord = None

    portal_coord_list = []

    for i in range(l0):
        for j in range(l1):
            current_char = grid_in[i][j]
            if 'A'<=current_char and current_char<='Z':
                for direction in dir_list:
                    i_temp = i+direction[0]
                    j_temp = j+direction[1]

                    if 0<=i_temp and i_temp<l0 and 0<=j_temp and j_temp<l1 and grid_in[i_temp][j_temp]=='.':
                        other_char = grid_in[i-direction[0]][j-direction[1]]

                        portal_code = None

                        coord_tuple = (i_temp,j_temp)

                        portal_coord_list.append(coord_tuple)

                        if direction[0]>0 or direction[1]>0:
                            portal_code = other_char+current_char
                        else:
                            portal_code = current_char+other_char

                        if portal_code=='AA':
                            start_coord = coord_tuple
                            portal_lookup[coord_tuple] = [portal_code,'Entrance']

                        elif portal_code=='ZZ':
                            end_coord = coord_tuple
                            portal_lookup[coord_tuple] = [portal_code,'Exit']

                        elif i_temp==i_min or i_temp==i_max or j_temp==j_min or j_temp==j_max:
                            outer_portal_dict[portal_code] = coord_tuple
                            portal_lookup[coord_tuple] = [portal_code,'O']

                        else:
                            inner_portal_dict[portal_code] = coord_tuple
                            portal_lookup[coord_tuple] = [portal_code,'I']

    dist_dict = {}

    for current_coord in portal_coord_list:
        dist_dict[current_coord] = {}

        output_dict = myGraph.compute_dist_BFS(current_coord)

        for neighbor_coord in portal_coord_list:
            if current_coord!=neighbor_coord and neighbor_coord in output_dict['dist_dict']:
                dist_dict[current_coord][neighbor_coord] = output_dict['dist_dict'][neighbor_coord]

    metaGraph = Graph()

    for key1 in dist_dict:
        for key2 in dist_dict[key1]:
            metaGraph.add_edge(key1,key2,dist_dict[key1][key2])


    for key in inner_portal_dict.keys():
        if key in outer_portal_dict:
            inner_portal_coords = inner_portal_dict[key]
            outer_portal_coords = outer_portal_dict[key]
            paired_portal_lookup[inner_portal_coords] = outer_portal_coords
            paired_portal_lookup[outer_portal_coords] = inner_portal_coords

    maze_dict = {}
    maze_dict['metaGraph'] = metaGraph
    maze_dict['inner_portal_dict'] = inner_portal_dict
    maze_dict['outer_portal_dict'] = outer_portal_dict
    maze_dict['start_coord'] = start_coord
    maze_dict['end_coord'] = end_coord
    maze_dict['dist_dict'] = dist_dict
    maze_dict['portal_lookup'] = portal_lookup
    maze_dict['paired_portal_lookup'] = paired_portal_lookup

    return maze_dict

def solve_maze01(grid_in):
    maze_dict = build_metagraph(grid_in)
    metaGraph = maze_dict['metaGraph']
    inner_portal_dict = maze_dict['inner_portal_dict']
    outer_portal_dict = maze_dict['outer_portal_dict']
    start_coord = maze_dict['start_coord']
    end_coord = maze_dict['end_coord']

    for key in inner_portal_dict.keys():
        if key in outer_portal_dict:
            metaGraph.add_edge(inner_portal_dict[key],outer_portal_dict[key],1)


    output_dict = metaGraph.compute_dist_dijkstra(start_coord,end_coord)
    print(output_dict['path_length'])

def solve_maze02(grid_in):
    maze_dict = build_metagraph(grid_in)
    metaGraph = maze_dict['metaGraph']
    inner_portal_dict = maze_dict['inner_portal_dict']
    outer_portal_dict = maze_dict['outer_portal_dict']
    start_coord = maze_dict['start_coord']
    end_coord = maze_dict['end_coord']
    dist_dict = maze_dict['dist_dict']
    portal_lookup = maze_dict['portal_lookup']
    paired_portal_lookup = maze_dict['paired_portal_lookup']

    myHeap = AugmentedHeap()

    dist_dict_recursive_donut = {}
    visited_dict_recursive_donut = {}

    myHeap.insert_item(0,(start_coord,0))

    max_depth = 0

    while not myHeap.isempty():
        temp_dist,current_vertex = myHeap.pop()

        dist_dict_recursive_donut[current_vertex] = temp_dist

        current_coords = current_vertex[0]
        current_level = current_vertex[1]

        portal_label = portal_lookup[current_coords]
        portal_code = portal_label[0]
        portal_type = portal_label[1]

        if current_coords == end_coord and current_level == 0:
            print(temp_dist)
            break

        #add neighbor on current level (distance is path length on current level)
        for neighbor_coords in dist_dict[current_coords]:
            neighbor_vertex_same_level = (neighbor_coords,current_level)
            next_dist = temp_dist+dist_dict[current_coords][neighbor_coords]

            if neighbor_vertex_same_level not in dist_dict_recursive_donut:
                if neighbor_vertex_same_level in visited_dict_recursive_donut:
                    myHeap.decrement_key(next_dist,neighbor_vertex_same_level)
                else:
                    visited_dict_recursive_donut[neighbor_vertex_same_level]=True
                    myHeap.insert_item(next_dist,neighbor_vertex_same_level)

        #add neighbor (from outer on current level to inner on level below, distance is 1 away)
        if portal_type=='O' and current_level>=1:
            neighbor_coords = paired_portal_lookup[current_coords]
            neighbor_vertex_previous_level = (neighbor_coords,current_level-1)

            next_dist = temp_dist+1

            if neighbor_vertex_previous_level not in dist_dict_recursive_donut:
                if neighbor_vertex_previous_level in visited_dict_recursive_donut:
                    myHeap.decrement_key(next_dist,neighbor_vertex_previous_level)
                else:
                    visited_dict_recursive_donut[neighbor_vertex_previous_level]=True
                    myHeap.insert_item(next_dist,neighbor_vertex_previous_level)


        #add neighbor (from inner on current level to outer on level below, distance is 1 away)
        if portal_type=='I':
            neighbor_coords = paired_portal_lookup[current_coords]
            neighbor_vertex_next_level = (neighbor_coords,current_level+1)

            next_dist = temp_dist+1
            if neighbor_vertex_next_level not in dist_dict_recursive_donut:
                if neighbor_vertex_next_level in visited_dict_recursive_donut:
                    myHeap.decrement_key(next_dist,neighbor_vertex_next_level)
                else:
                    visited_dict_recursive_donut[neighbor_vertex_next_level]=True
                    myHeap.insert_item(next_dist,neighbor_vertex_next_level)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    for item in data:
        solve_maze01(item)

def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    for item in data:
        solve_maze02(item)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

