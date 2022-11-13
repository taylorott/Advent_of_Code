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

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,'\)')

    return data

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    myGraph = Digraph()

    for item in data:
        myGraph.add_edge(item[0],item[1])

    myGraph.build_metagraph()

    num_descendents_dict = {}

    total = 0
    for i in range(myGraph.num_components-1,-1,-1):
        for vertex in myGraph.assigned_lookup[i]:
            num_descendents_dict[vertex]=0
            for child in myGraph.forward_adjacency[vertex]:
                num_descendents_dict[vertex]+=1+num_descendents_dict[child]
            total+=num_descendents_dict[vertex]
    print(total)


def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    myGraph = Digraph()

    for item in data:
        myGraph.add_edge(item[0],item[1])

    vertex_list1 = []
    current_vertex = 'YOU'

    while current_vertex != 'COM':
        current_vertex = myGraph.reverse_adjacency[current_vertex][0]
        vertex_list1.append(current_vertex)


    vertex_list2 = []
    current_vertex = 'SAN'

    while current_vertex != 'COM':
        current_vertex = myGraph.reverse_adjacency[current_vertex][0]
        vertex_list2.append(current_vertex)


    while len(vertex_list1)>0 and len(vertex_list2)>0 and vertex_list1[-1]==vertex_list2[-1]:
        vertex_list1.pop(-1)
        vertex_list2.pop(-1)

    # print(vertex_list1)
    # print(vertex_list2)
    print(len(vertex_list1)+len(vertex_list2))

if __name__ == '__main__':
    solution01()
    solution02()
    

