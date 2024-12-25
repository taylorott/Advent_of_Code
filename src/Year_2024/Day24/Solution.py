#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [':',' ','-','>'],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_extract_ints_split_by_emptylines(path,fname)
    # data = bh.parse_extract_ints(path,fname)

    return data

def fix_key(instruction,mapping_dict):
    key1 = instruction[0]
    key2 = instruction[2]

    key3 = instruction[3]
    operator = instruction[1]


    # print(key1,key2)
    if key1[1:].isdigit() and key2[1:].isdigit() and key1[1:]==key2[1:]:
        if (key1[0]=='x' and key2[0]=='y') or (key1[0]=='y' and key2[0]=='x'):
            if operator == 'AND':
                # print('hi!')
                mapping_dict[key3] = 'h'+ key2[1:]
                return mapping_dict[key3]
            if operator == 'XOR':
                # print('hello1')
                mapping_dict[key3] = 'q' +key2[1:]
                return mapping_dict[key3]

    return key3

def example_compare_function(x,y):
    q1 = int(x[0][1:])
    q2 = int(y[0][1:])

    if q1>q2: return 1
    if q1<q2: return -1
    if q1==q2: return 0


def example_compare_function1(x,y):
    if x[3][0]!='z' or y[3][0]!='z': return 1
    q1 = int(x[3][1:])
    q2 = int(y[3][1:])

    if q1>q2: return 1
    if q1<q2: return -1
    if q1==q2: return 0

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    value_dict = dict()

    key_list = []
    key_set = set()

    for item in data[0]:
        value_dict[item[0]]=int(item[1])

        if item[0][0]=='z' and item[0] not in key_set:
            key_set.add(item[0])
            key_list.append(item[0])


    # max_index = 0

    for item in data[1]:
        if item[0][0]=='y' and item[2][0]=='x':
            temp = item[0]
            item[0] = item[2]
            item[2] = temp

    #     if item[0][0]=='x':
    #         q = item[0][1:]
    #         v = int(q)
    #         max_index = max(max_index,v)

    #         if item[1] == 'XOR':
    #             item[0] = 'm'+q
    #             item[2] = 'n'+q


    list1 = []
    list2 = []
    list3 = []
    list4 = []
    list5 = []
    for item in data[1]:
        if item[0][0]=='x' and item[1]=='AND': list1.append(item)

        if item[0][0]=='x' and item[1]=='XOR': list2.append(item)

        if item[0][0]!='x' and item[1]=='AND': list3.append(item)

        if item[0][0]!='x' and item[1]=='XOR': list4.append(item)

        if item[0][0]!='x' and item[1]=='OR': list5.append(item)

            # print(item)

    list1 = sorted(list1,key=cmp_to_key(example_compare_function))
    list2 = sorted(list2,key=cmp_to_key(example_compare_function))

    list4 = sorted(list4,key=cmp_to_key(example_compare_function1))

    # for item in list1: print(item)

    # print('')
    # for item in list2: print(item)

    # print('')
    for item in list5: print(item)
    myGraph = Digraph()

    # operator_dict = dict()

    # mapping_dict = dict()

    # for i in range(3):
    #     for item in data[1]:
    #         item[3] = fix_key(item,mapping_dict)

    #         if item[1] in mapping_dict: item[1] = mapping_dict[item[1]]

    #         if item[2] in mapping_dict: item[2] = mapping_dict[item[2]]


    # for item in data[1]:
    #     print(item)


    # for item in data[1]:
    #     v1 = item[0]
    #     v2 = item[2]
    #     operator = item[1]
    #     v3 = item[3]

    #     myGraph.add_edge(v1,v3)
    #     myGraph.add_edge(v2,v3)
    #     operator_dict[v3] = [operator, v1, v2]


    #     fix_key(item)

    #     for q in item:

    #         if q[0]=='z' and q not in key_set:
    #             key_set.add(q)
    #             key_list.append(q)



    

    # print(myGraph.meta_forward_dict)
    # print(len(myGraph.meta_forward_dict))

    # for i in range(len(myGraph.meta_forward_dict)):
    #     current_vertex = myGraph.assigned_lookup[i][0]

    #     if current_vertex in operator_dict:
    #         # print(current_vertex)
    #         operator = operator_dict[current_vertex][0]
    #         v1 = value_dict[operator_dict[current_vertex][1]]
    #         v2 = value_dict[operator_dict[current_vertex][2]]

    #         if operator == 'AND':
    #             value_dict[current_vertex] = v1&v2
    #         if operator == 'OR':
    #             value_dict[current_vertex] = v1|v2
    #         if operator == 'XOR':
    #             value_dict[current_vertex] = v1^v2


    # key_list.sort(reverse=True)
    # total = 0

    # for item in key_list:
    #     total<<=1
    #     total+= value_dict[item]
    # print(total)



    # print(operator_dict)
    # print(value_dict)
    # print(data)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

