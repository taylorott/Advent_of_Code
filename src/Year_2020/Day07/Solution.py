#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh

from Helpers.DSA_helpers import Digraph

path = currentdir

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    myDigraph = Digraph()

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    for item in data:
        split_str01 = item[0:-1].split('contain ')
        outer = split_str01[0]
        inner_bags = split_str01[1].split(', ')
        outer = outer[0:-6]
        inner_list = []

        # print(inner_bags)
        
        if inner_bags[0]!='no other bags':
            for inner in inner_bags:
                split_str02 = inner.split(' ',1)
                num_bags = int(split_str02[0])

                inner = None
                if num_bags==1:
                    inner = split_str02[1][0:-4]
                else:
                    inner = split_str02[1][0:-5]

                myDigraph.add_edge(outer,inner,num_bags)
                
    print(len(myDigraph.list_ancestors('shiny gold'))-1)

def count_nested_bags_recursive(my_graph,bag_type,num_children_dict):
    if bag_type not in num_children_dict:
        total = 0
        for child in my_graph.forward_adjacency[bag_type]:
            total+= my_graph.edge_dict[bag_type][child]*(1+count_nested_bags_recursive(my_graph,child,num_children_dict))

        num_children_dict[bag_type]=total
    return num_children_dict[bag_type] 


def count_nested_bags(my_graph,bag_type):
    num_children_dict = {}
    count_nested_bags_recursive(my_graph,bag_type,num_children_dict)
    return num_children_dict[bag_type]



def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    # fname = 'Input03.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    myDigraph = Digraph()

    for item in data:
        split_str01 = item[0:-1].split('contain ')
        outer = split_str01[0]
        inner_bags = split_str01[1].split(', ')
        outer = outer[0:-6]
        inner_list = []

        # print(inner_bags)
        
        if inner_bags[0]!='no other bags':
            for inner in inner_bags:
                split_str02 = inner.split(' ',1)
                num_bags = int(split_str02[0])

                inner = None
                if num_bags==1:
                    inner = split_str02[1][0:-4]
                else:
                    inner = split_str02[1][0:-5]

                myDigraph.add_edge(outer,inner,num_bags)
                
    print(count_nested_bags(myDigraph,'shiny gold'))

if __name__ == '__main__':
    solution01()
    solution02()
    

