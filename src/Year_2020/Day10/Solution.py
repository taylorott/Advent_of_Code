#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph

path = currentdir


    
# def find_hamiltonian_path_via_backtracking(my_graph,v0,vf):
#     visited_dict = {}
#     for vertex in my_graph.vertex_list:
#         visited_dict[vertex] = False

#     hamiltonian_path = []

#     find_hamiltonian_path_via_backtracking_recursive(my_graph,v0,vf,visited_dict,hamiltonian_path)
    
#     return hamiltonian_path

# def find_hamiltonian_path_via_backtracking_recursive(my_graph,v_current,vf,visited_dict,hamiltonian_path):
#     if not visited_dict[v_current]:
#         visited_dict[v_current]=True
#         hamiltonian_path.append(v_current)
        
#         if v_current == vf:
#             if len(hamiltonian_path)==len(my_graph.vertex_list):
#                 return True
#             else:
#                 hamiltonian_path.pop(-1)
#                 visited_dict[v_current]=False
#                 return False

#         for child in my_graph.forward_adjacency[v_current]:
#             if find_hamiltonian_path_via_backtracking_recursive(my_graph,child,vf,visited_dict,hamiltonian_path):
#                 return True

#         hamiltonian_path.pop(-1)
#         visited_dict[v_current]=False

#     return False



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)


    num_list.append(0)
    num_list.append(max(num_list)+3)

    num_list.sort()

    diff1 = 0
    diff3 = 0

    for i in range(1,len(num_list)):
        if num_list[i]-num_list[i-1]==1:
            diff1+=1
        if num_list[i]-num_list[i-1]==3:
            diff3+=1

    print(diff1*diff3)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)


    num_list.append(0)
    num_list.append(max(num_list)+3)

    num_list.sort()
    num_dict = {}
    num_paths = {0:1}


    for i in range(len(num_list)):
        num = num_list[i]
        num_dict[num]=i

        if num!=0:
            total = 0
            for prev_num in range(num-3,num):
                if prev_num in num_dict:
                    total+= num_paths[prev_num]
            num_paths[num]=total
    print(num_paths[max(num_list)])



if __name__ == '__main__':
    solution01()
    solution02()
    

