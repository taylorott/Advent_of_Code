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

###NOTES:
#Longest simple path is an NP-hard problem. However, this problem has some exploitable
#structure that allows us to implement several speedups (current time ~4 seconds)
#Speedup #1: there are many subpaths that don't have any possibility of branching
#these subpaths can be contracted into a single edge whose weight is the length of the subpath
#Speedup #2: we can memoize the recursion, where the table maps
#(vertices already visited on this path, current vertex) -> max path length
#I created a custom hash for the vertices already visited, specifically, assign each vertex 
#a number from 0 to n-1, and then generate the n digit binary number B where B_n = 1 if 
#vertex is on the current path, and B_n = 0 if not on current path.
#Speedup #3: since this is a planar graph, the outside edges can only be traversed in 
#a single direction (otherwise you trap yourself and can't reach the destination)
#this means we can prune a few extra edges in the digraph, which speed things up a bit.

def parse_input01(fname):
    return bh.parse_char_grid(path,fname)

def adjacency_criteria_part1(grid_in, coord0, coord1):
    i0, j0, i1, j1 = coord0[0], coord0[1], coord1[0], coord1[1]
    c0, c1 = grid_in[i0][j0], grid_in[i1][j1]

    if c0=='#' or c1=='#':
        return False

    if (c0=='^' and i1-i0 != -1) or (c0=='v' and i1-i0 != 1) or (c0=='<' and j1-j0 != -1) or (c0=='>' and j1-j0 != 1):
        return False

    if (c1=='^' and i1-i0 == 1) or (c1=='v' and i1-i0 == -1) or (c1=='<' and j1-j0 == 1) or (c1=='>' and j1-j0 == -1):
        return False
    
    return True

def adjacency_criteria_part2(grid_in, coord0, coord1):
    i0, j0, i1, j1 = coord0[0], coord0[1], coord1[0], coord1[1]
    c0, c1 = grid_in[i0][j0], grid_in[i1][j1]

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

def solution01(show_result=True, fname='Input02.txt'):
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
    
    if show_result: print(total)

    return total


def compute_next_steps_list_part2(myGraph,vertex_set,current_vertex):
    next_step_list = []

    for next_vertex in myGraph.adjacency_set[current_vertex]:
        if next_vertex not in vertex_set:
            next_step_list.append(next_vertex)
    return next_step_list

def contract_edge(contracted_graph,original_graph,visited_set,starting_vertex, boundary_dict):

    A_to_B = True
    B_to_A = True


    edge_vertex_set = set()
    edge_vertex_set.add(starting_vertex)

    edge_length = 0

    next_step_list = compute_next_steps_list_part2(original_graph,edge_vertex_set,starting_vertex)

    vertex_queue = deque()
    vertex_queue.append(starting_vertex)

    vertex_A = starting_vertex
    vertex_B = starting_vertex

    if len(next_step_list)==2:
        vertex_A = next_step_list[0]
        vertex_B = next_step_list[1]

        vertex_queue.appendleft(vertex_A)
        vertex_queue.append(vertex_B)

        edge_length = 2
    elif len(next_step_list)==1:
        vertex_B = next_step_list[0]

        vertex_queue.append(vertex_B)
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
            vertex_queue.appendleft(vertex_A)

        next_step_list = compute_next_steps_list_part2(original_graph,edge_vertex_set,vertex_B)

        if len(next_step_list)==1:
            vertex_B=next_step_list[0]
            edge_length+=1
            edge_vertex_set.add(vertex_B)
            can_update=True
            vertex_queue.append(vertex_B)

    vertex_list = list(vertex_queue)

    for i in range(len(vertex_list)):
        current_vertex = vertex_list[i]
        if current_vertex in boundary_dict:
            bad_direction = boundary_dict[current_vertex]
            bad_next_vertex = (current_vertex[0]+bad_direction[0],current_vertex[1]+bad_direction[1])
            bad_prev_vertex = (current_vertex[0]-bad_direction[0],current_vertex[1]-bad_direction[1])

            if i+1<len(vertex_list) and bad_next_vertex == vertex_list[i+1]:
                A_to_B = False
            if i-1>=0 and bad_next_vertex == vertex_list[i-1]:
                B_to_A = False

            if i+1<len(vertex_list) and bad_prev_vertex == vertex_list[i+1]:
                B_to_A = False
            if i-1>=0 and bad_prev_vertex == vertex_list[i-1]:
                A_to_B = False

    if A_to_B:
        if vertex_A in contracted_graph.vertex_dict and vertex_B in contracted_graph.edge_dict[vertex_A]:
            new_weight = max(contracted_graph.edge_dict[vertex_A][vertex_B],edge_length)

            contracted_graph.edge_dict[vertex_A][vertex_B]=new_weight
        else:
            contracted_graph.add_edge(vertex_A,vertex_B,w=edge_length)
    if B_to_A:
        if vertex_B in contracted_graph.vertex_dict and vertex_A in contracted_graph.edge_dict[vertex_B]:
            new_weight = max(contracted_graph.edge_dict[vertex_B][vertex_A],edge_length)

            contracted_graph.edge_dict[vertex_B][vertex_A]=new_weight
        else:
            contracted_graph.add_edge(vertex_B,vertex_A,w=edge_length)

    for vertex in edge_vertex_set:
        visited_set.add(vertex)

def contract_graph(original_graph, boundary_dict):
    contracted_graph = Digraph()

    visited_set = set()

    for vertex in original_graph.vertex_set:
        if vertex not in visited_set and len(original_graph.adjacency_set[vertex])<=2:
            contract_edge(contracted_graph,original_graph,visited_set,vertex, boundary_dict)

    return contracted_graph

def find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,destination,result_dict,vertex_coding, hash_val):
    max_length_remaining = 0

    q = vertex_coding[path_stack[-1]]
    hash_val+= (1<<q)
    lookup_key = (hash_val,q)

    if lookup_key in result_dict: return result_dict[lookup_key]

    for next_vertex in myGraph.forward_adjacency[path_stack[-1]]:
        edge_length = myGraph.edge_dict[path_stack[-1]][next_vertex]

        if next_vertex == destination:
            max_length_remaining = max(max_length_remaining,edge_length)
        elif not visited_dict[next_vertex]:
            visited_dict[next_vertex]=True
            path_stack.append(next_vertex)

            candidate_length = edge_length+find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,destination,result_dict,vertex_coding, hash_val)            
            max_length_remaining = max(max_length_remaining,candidate_length)

            path_stack.pop(-1)
            visited_dict[next_vertex]=False

    result_dict[lookup_key] = max_length_remaining
    return max_length_remaining

def build_boundary_dict(grid):
    boundary_dict = dict()

    for i in range(len(grid)):
        j = 0
        while j<len(grid[0]) and grid[i][j]=='#':
            j+=1
        boundary_dict[(i,j)]=(-1,0)

        j = len(grid[0])-1
        while j>=0 and grid[i][j]=='#':
            j-=1
        boundary_dict[(i,j)]=(-1,0) 

    for j in range(len(grid[0])):
        i = 0
        while i<len(grid) and grid[i][j]=='#':
            i+=1
        boundary_dict[(i,j)]=(0,-1)
        
        i = len(grid)-1
        while i>=0 and grid[i][j]=='#':
            i-=1
        boundary_dict[(i,j)]=(0,-1)

    boundary_dict.pop((0,1))
    boundary_dict.pop((len(grid)-1,len(grid[0])-2))

    return boundary_dict  

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    myGraph = Graph()
    myGraph.build_graph_from_2D_grid(data,adjacency_criteria=adjacency_criteria_part2)
    
    starting_vertex = (0,1)
    end_vertex = (len(data)-1,len(data[0])-2)

    boundary_dict = build_boundary_dict(data)

    myGraph = contract_graph(myGraph, boundary_dict)

    vertex_coding = dict()

    count = 0
    for vertex in myGraph.vertex_set:
        vertex_coding[vertex]=count
        count+=1

    result_dict = {}
    visited_dict = {}
    for vertex in myGraph.vertex_set:
        visited_dict[vertex]=False

    path_stack = [starting_vertex]
    visited_dict[starting_vertex]=True

    total = find_longest_path_recursive_part2(myGraph,path_stack,visited_dict,end_vertex,result_dict,vertex_coding,0)
    
    if show_result: print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

