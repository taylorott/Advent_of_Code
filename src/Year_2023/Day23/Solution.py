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

    return data


def adjacency_criteria_part1(grid_in, coord0, coord1):
    i0 = coord0[0]
    j0 = coord0[1]
    i1 = coord1[0]
    j1 = coord1[1]

    c0 = grid_in[i0][j0]
    c1 = grid_in[i1][j1]

    if c0=='#' or c1=='#':
        return False

    if (c0=='^' and i1-i0 != -1) or (c0=='v' and i1-i0 != 1) or (c0=='<' and j1-j0 != -1) or (c0=='>' and j1-j0 != 1):
        return False

    if (c1=='^' and i1-i0 == 1) or (c1=='v' and i1-i0 == -1) or (c1=='<' and j1-j0 == 1) or (c1=='>' and j1-j0 == -1):
        return False
    
    return True

def adjacency_criteria_part2(grid_in, coord0, coord1):
    i0 = coord0[0]
    j0 = coord0[1]
    i1 = coord1[0]
    j1 = coord1[1]

    c0 = grid_in[i0][j0]
    c1 = grid_in[i1][j1]

    if c0=='#' or c1=='#':
        return False

    return True

def compute_next_step_list_part1(myGraph,path_stack,visited_dict):
    next_step_list = []
    for item in myGraph.forward_adjacency[path_stack[-1]]:
        if not visited_dict[item]:
            next_step_list.append(item)

    return next_step_list

def find_longest_path_recursive_part1(myGraph,path_stack,visited_dict,destination):

    base_dist = 0
    next_step_list = compute_next_step_list_part1(myGraph,path_stack,visited_dict)

    while len(next_step_list)==1 and path_stack[-1]!=destination:
        base_dist+=1
        path_stack.append(next_step_list[0])
        visited_dict[path_stack[-1]]=True
        next_step_list = compute_next_step_list_part1(myGraph,path_stack,visited_dict)

    if path_stack[-1]==destination:
        for i in range(base_dist):
            visited_dict[path_stack[-1]]=False
            path_stack.pop(-1)
        return base_dist

    elif len(next_step_list) == 0:
        for i in range(base_dist):
            visited_dict[path_stack[-1]]=False
            path_stack.pop(-1)
        return 0

    max_length_remaining = 0
    for next_vertex in myGraph.forward_adjacency[path_stack[-1]]:
        if next_vertex == destination:
            max_length_remaining = max(max_length_remaining,base_dist+1)
        elif not visited_dict[next_vertex]:
            visited_dict[next_vertex]=True
            path_stack.append(next_vertex)

            candidate_length = base_dist+1+find_longest_path_recursive_part1(myGraph,path_stack,visited_dict,destination)            
            max_length_remaining = max(max_length_remaining,candidate_length)

            path_stack.pop(-1)
            visited_dict[next_vertex]=False

    for i in range(base_dist):
        visited_dict[path_stack[-1]]=False
        path_stack.pop(-1)

    return max_length_remaining

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    myGraph = Digraph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria=adjacency_criteria_part1)
    
    visited_dict = {}
    for vertex in myGraph.forward_adjacency:
        visited_dict[vertex]=False

    starting_vertex = (0,1)
    end_vertex = (len(data)-1,len(data[0])-2)

    path_stack = [starting_vertex]
    visited_dict[starting_vertex]=True

    total = find_longest_path_recursive_part1(myGraph,path_stack,visited_dict,end_vertex)
    print(total)


def compute_next_steps_list_part2(myGraph,vertex_set,current_vertex):
    next_step_list = []

    for next_vertex in myGraph.adjacency_set[current_vertex]:
        if next_vertex not in vertex_set:
            next_step_list.append(next_vertex)
    return next_step_list

def contract_edge(contracted_graph,original_graph,visited_set,starting_vertex):
    edge_vertex_set = set()
    edge_vertex_set.add(starting_vertex)

    edge_length = 0

    next_step_list = compute_next_steps_list_part2(original_graph,edge_vertex_set,starting_vertex)

    vertex_A = starting_vertex
    vertex_B = starting_vertex

    if len(next_step_list)==2:
        vertex_A = next_step_list[0]
        vertex_B = next_step_list[1]
        edge_length = 2
    elif len(next_step_list)==1:
        vertex_B = next_step_list[0]
        edge_length = 1

    edge_vertex_set.add(vertex_A)
    edge_vertex_set.add(vertex_B)

    can_update = True

    while can_update:
        can_update = False

        next_step_list = compute_next_steps_list_part2(original_graph,edge_vertex_set,vertex_A)

        if len(next_step_list)==1:
            vertex_A=next_step_list[0]
            edge_length+=1
            edge_vertex_set.add(vertex_A)
            can_update=True

        next_step_list = compute_next_steps_list_part2(original_graph,edge_vertex_set,vertex_B)

        if len(next_step_list)==1:
            vertex_B=next_step_list[0]
            edge_length+=1
            edge_vertex_set.add(vertex_B)
            can_update=True

    if vertex_A in contracted_graph.vertex_dict and vertex_B in contracted_graph.edge_dict[vertex_A]:
        new_weight = max(contracted_graph.edge_dict[vertex_A][vertex_B],edge_length)
        contracted_graph.edge_dict[vertex_A][vertex_B]=new_weight
        contracted_graph.edge_dict[vertex_B][vertex_A]=new_weight
    else:
        contracted_graph.add_edge(vertex_A,vertex_B,w=edge_length)

    for vertex in edge_vertex_set:
        visited_set.add(vertex)

def contract_graph(original_graph):
    contracted_graph = Graph()

    visited_set = set()

    for vertex in original_graph.vertex_set:
        if vertex not in visited_set and len(original_graph.adjacency_set[vertex])<=2:
            contract_edge(contracted_graph,original_graph,visited_set,vertex)

    return contracted_graph

def find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,destination):
    max_length_remaining = 0
    for next_vertex in myGraph.adjacency_set[path_stack[-1]]:
        edge_length = myGraph.edge_dict[path_stack[-1]][next_vertex]
        if next_vertex == destination:
            max_length_remaining = max(max_length_remaining,edge_length)
        elif not visited_dict[next_vertex]:
            visited_dict[next_vertex]=True
            path_stack.append(next_vertex)

            candidate_length = edge_length+find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,destination)            
            max_length_remaining = max(max_length_remaining,candidate_length)

            path_stack.pop(-1)
            visited_dict[next_vertex]=False

    return max_length_remaining

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria=adjacency_criteria_part2)
    
    starting_vertex = (0,1)
    end_vertex = (len(data)-1,len(data[0])-2)

    myGraph = contract_graph(myGraph)

    visited_dict = {}
    for vertex in myGraph.vertex_set:
        visited_dict[vertex]=False

    path_stack = [starting_vertex]
    visited_dict[starting_vertex]=True

    total = find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,end_vertex)
    print(total)



if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

