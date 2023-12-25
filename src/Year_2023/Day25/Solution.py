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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [':',' '],type_lookup = None, allInt = False, allFloat = False)

    return data


def compute_dist_BFS(myGraph,start_vert,target_vert,used_edge_set):
    output_dict = {}

    if start_vert not in myGraph.vertex_dict:
        return output_dict

    dist_dict = {start_vert:0}
    output_dict['dist_dict'] = dist_dict

    predecessor_dict = {start_vert:None}
    output_dict['predecessor_dict'] = predecessor_dict
    
    to_visit = deque()
    to_visit.append(start_vert)

    while len(to_visit)!=0:
        current_vert = to_visit.popleft()
        current_dist = dist_dict[current_vert]

        if current_vert == target_vert:
            path_stack = [target_vert]
            while predecessor_dict[path_stack[-1]] is not None:
                path_stack.append(predecessor_dict[path_stack[-1]])

            path_out = []
            while len(path_stack)>0:
                path_out.append(path_stack.pop(-1))

            output_dict['path_length'] = current_dist
            output_dict['path'] = path_out

            return output_dict

        next_dist = current_dist+1
        for neighbor_vert in myGraph.adjacency_list[current_vert]:
            edge_tuple = (min(current_vert,neighbor_vert),max(current_vert,neighbor_vert))

            if neighbor_vert not in dist_dict and edge_tuple not in used_edge_set:
                dist_dict[neighbor_vert] = next_dist
                to_visit.append(neighbor_vert)
                predecessor_dict[neighbor_vert]=current_vert

    return output_dict

def compute_connection_strength(myGraph,start_vert,target_vert):
    used_edge_set = set()

    for i in range(4):
        output_dict = compute_dist_BFS(myGraph,start_vert,target_vert,used_edge_set)

        if 'path' in output_dict:
            graph_path = output_dict['path']

            for j in range(len(graph_path)-1):
                v0 = graph_path[j]
                v1 = graph_path[j+1]

                edge_tuple = (min(v0,v1),max(v0,v1))
                used_edge_set.add(edge_tuple)
        else:
            return False

    return True

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    myGraph = Graph()

    vertex_set = set()

    vertex_lookup = {}
    vertex_list = []

    num_vertices = 0
    for item in data:
        for vertex in item:
            if vertex not in vertex_lookup:
                vertex_lookup[vertex] = num_vertices
                vertex_list.append(vertex)
                num_vertices+=1

    for item in data:
        for i in range(1,len(item)):
            v0 = vertex_lookup[item[0]]
            v1 = vertex_lookup[item[i]]
            myGraph.add_edge(v0,v1)

    size1 = 1
    size2 = 0

    for i in range(1,num_vertices):
        is_connected = compute_connection_strength(myGraph,start_vert=0,target_vert=i)

        if is_connected:
            size1+=1
        else:
            size2+=1

    print(size1*size2)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

