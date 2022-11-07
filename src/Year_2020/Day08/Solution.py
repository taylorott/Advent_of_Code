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

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,' ',['str','int'])

    visited_dict = {}
    acc = 0
    line_num = 0

    while line_num not in visited_dict:
        visited_dict[line_num]=None

        if data[line_num][0]=='acc':
            acc+=data[line_num][1]
            line_num+=1
        elif data[line_num][0]=='jmp':
            line_num+=data[line_num][1]
        elif data[line_num][0]=='nop':
            line_num+=1

    print(acc)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = bh.parse_strings(path,fname,' ',['str','int'])

    myDigraph = Digraph()

    for line_num in range(len(data)):
        if data[line_num][0]=='acc':
            myDigraph.add_edge(line_num,line_num+1)
        elif data[line_num][0]=='jmp':
            myDigraph.add_edge(line_num,min(line_num+data[line_num][1],len(data)))
        elif data[line_num][0]=='nop':
            myDigraph.add_edge(line_num,line_num+1)

    forward_reachable = myDigraph.list_descendents(0)
    backward_reachable = myDigraph.list_ancestors(len(data))

    forward_reachable_dict = {}
    backward_reachable_dict = {}

    for item in forward_reachable:
        forward_reachable_dict[item] = None

    for item in backward_reachable:
        backward_reachable_dict[item] = None

    for line_num in range(len(data)):
        if data[line_num][0]=='jmp' and line_num in forward_reachable_dict and line_num+1 in backward_reachable_dict:
            data[line_num][0]='nop'
            break
        elif data[line_num][0]=='nop' and line_num in forward_reachable_dict and line_num+data[line_num][1] in backward_reachable_dict:
            data[line_num][0]='jmp'
            break

    acc = 0
    line_num = 0

    while line_num < len(data):
        if data[line_num][0]=='acc':
            acc+=data[line_num][1]
            line_num+=1
        elif data[line_num][0]=='jmp':
            line_num+=data[line_num][1]
        elif data[line_num][0]=='nop':
            line_num+=1

    print(acc)


if __name__ == '__main__':
    solution01()
    solution02()
    

