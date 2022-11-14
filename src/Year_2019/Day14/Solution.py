#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,['=',',',' ','>'])

    reaction_dict = {}

    for line in data:
        q_list = []
        v_list = []
        for i in range(0,len(line)-2,2):
            q_list.append(int(line[i]))
            v_list.append(line[i+1])

        q_out = int(line[-2])
        v_out = line[-1]

        reaction_dict[v_out]=[q_list,v_list,q_out]
    return reaction_dict

def count_ore(data,num_fuel):
    myGraph = Digraph()

    for output_val in data.keys():
        for i in range(len(data[output_val][1])):
            w = data[output_val][0][i]
            input_val = data[output_val][1][i]
            myGraph.add_edge(output_val,input_val,w)

    myGraph.build_metagraph()

    material_dict = {'FUEL':num_fuel}
    for i in range(myGraph.num_components):
        vertex = myGraph.assigned_lookup[i][0]


        if vertex=='ORE':
            return int(material_dict[vertex])

        num_to_make = material_dict.pop(vertex)
        num_reactions = np.ceil(num_to_make/data[vertex][2])

        for j in range(len(data[vertex][1])):
            w = data[vertex][0][j]
            input_val = data[vertex][1][j]


            if input_val in material_dict:
                material_dict[input_val]+=w*num_reactions
            else:
                material_dict[input_val]=w*num_reactions    

def solution01():
    # fname = 'Input01.txt'
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    res = count_ore(data,1)
    print(res)




def solution02():
    # fname = 'Input01.txt'
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    res = count_ore(data,1)
    
    input_left = 1
    input_right = (2*10**12)//res

    tar_val = 10**12

    while input_right-input_left>1:
        input_mid=(input_left+input_right)//2

        res = count_ore(data,input_mid)

        if res>tar_val:
            input_right = input_mid
        else:
            input_left = input_mid

    print(input_left)



if __name__ == '__main__':
    solution01()
    solution02()
    

