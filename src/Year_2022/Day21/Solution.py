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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [':',' '],type_lookup = None, allInt = False, allFloat = False)

    monkey_value_dict = {}
    monkey_adjacency_dict = {}
    operation_dict = {}

    for line in data:
        monkey = line[0]
        if len(line)==2:
            monkey_value_dict[monkey]=int(line[1])
            monkey_adjacency_dict[monkey]=None
            operation_dict[monkey]=None
        else:
            monkey_value_dict[monkey]=None
            monkey_adjacency_dict[monkey]=[line[1],line[3]]
            operation_dict[monkey]=line[2]

    return operation_dict, monkey_adjacency_dict, monkey_value_dict


def print_operation(monkey,operation_dict,monkey_adjacency_dict,monkey_value_dict):
    if operation_dict[monkey] is None:
        return None

    operation = operation_dict[monkey]
    monkey_left = monkey_adjacency_dict[monkey][0]
    monkey_right = monkey_adjacency_dict[monkey][1]
    v0 = monkey_value_dict[monkey_left]
    v1 = monkey_value_dict[monkey_right]

    str0 = monkey_left
    str1 = monkey_right

    if v0 is not None:
        str0 = str(v0)
    if v1 is not None:
        str1 = str(v1)

    str_out = monkey+' = '+str0 +' '+operation+' '+str1

    print(str_out)


def print_operation_chain(monkey,operation_dict,monkey_adjacency_dict,monkey_value_dict):
    if operation_dict[monkey] is None:
        return None

    print_operation(monkey,operation_dict,monkey_adjacency_dict,monkey_value_dict)

    monkey_left = monkey_adjacency_dict[monkey][0]
    monkey_right = monkey_adjacency_dict[monkey][1]
    v0 = monkey_value_dict[monkey_left]
    v1 = monkey_value_dict[monkey_right]

    if v0 is None:
        print_operation_chain(monkey_left,operation_dict,monkey_adjacency_dict,monkey_value_dict)

    if v1 is None:
        print_operation_chain(monkey_right,operation_dict,monkey_adjacency_dict,monkey_value_dict)


def generate_monkey_graph(monkey_adjacency_dict):
    monkeyDigraph = Digraph()

    
    for monkey in monkey_adjacency_dict.keys():
        if monkey_adjacency_dict[monkey] is not None:
            monkeyDigraph.add_edge(monkey,monkey_adjacency_dict[monkey][0])
            monkeyDigraph.add_edge(monkey,monkey_adjacency_dict[monkey][1])

    return monkeyDigraph

def eval_monkey_chain(monkeyDigraph,operation_dict, monkey_adjacency_dict, monkey_value_dict):
    eval_stack = []

    eval_stack.append('root')

    #only give each node two attempts to evaluate
    #the avoid an infinite loop when 'humn' is given as incomplete
    has_attempted_before_dict = {}

    while len(eval_stack)>0:
        current_monkey = eval_stack.pop(-1)

        if operation_dict[current_monkey] is not None:
            monkey_left = monkey_adjacency_dict[current_monkey][0]
            monkey_right = monkey_adjacency_dict[current_monkey][1]
            v0 = monkey_value_dict[monkey_left]
            v1 = monkey_value_dict[monkey_right]

            if v0 is not None and v1 is not None:
                operation = operation_dict[current_monkey]
                v_out = None
                if operation == '+':
                    v_out = v0+v1
                elif operation == '-':
                    v_out = v0-v1
                elif operation == '*':
                    v_out = v0*v1
                elif operation == '/':
                    v_out = v0//v1
                elif operation == '==':
                    v_out = v0==v1

                monkey_value_dict[current_monkey]=v_out
            
            else:
                if current_monkey not in has_attempted_before_dict:
                    eval_stack.append(current_monkey)
                    has_attempted_before_dict[current_monkey]=True

                if v0 is None:
                    eval_stack.append(monkey_left)

                if v1 is None:
                    eval_stack.append(monkey_right)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    operation_dict, monkey_adjacency_dict, monkey_value_dict = parse_input01(fname)
    monkeyDigraph = generate_monkey_graph(monkey_adjacency_dict)
    eval_monkey_chain(monkeyDigraph,operation_dict, monkey_adjacency_dict, monkey_value_dict)

    print(monkey_value_dict['root'])


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    operation_dict, monkey_adjacency_dict, monkey_value_dict = parse_input01(fname)

    monkey_value_dict['humn']=None
    operation_dict['root']='=='

    monkeyDigraph = generate_monkey_graph(monkey_adjacency_dict)
    eval_monkey_chain(monkeyDigraph,operation_dict, monkey_adjacency_dict, monkey_value_dict)

    #f(humn) = (a/b)*humn+(c/d)
    a = 1
    b = 1
    c = 0
    d = 1

    current_monkey = 'humn'

    while current_monkey != 'root':
        operation = operation_dict[current_monkey]

        if operation is not None:
            monkey_left = monkey_adjacency_dict[current_monkey][0]
            monkey_right = monkey_adjacency_dict[current_monkey][1]

            v0 = monkey_value_dict[monkey_left]
            v1 = monkey_value_dict[monkey_right]
            
            if operation == '+':
                v_add = None
                if v0 is not None:
                    v_add = v0
                else:
                    v_add = v1

                c+=v_add*d

            elif operation == '-':
                if v0 is not None:
                    c=v0*d-c
                    a*=-1
                else:
                    c-=v1*d
            elif operation == '*':
                v_mult = None
                if v0 is not None:
                    v_mult = v0
                else:
                    v_mult = v1

                a*=v_mult
                c*=v_mult

            elif operation == '/':
                if v0 is not None:
                    print('uh oh! I cannot handle this!')
                else:
                    b*=v1
                    d*=v1

            temp = gcd(a,b)
            a//=temp
            b//=temp

            temp = gcd(c,d)
            c//=temp
            d//=temp

            if b<0:
                a*=-1
                b*=-1

            if d<0:
                c*=-1
                d*=-1

        for parent in monkeyDigraph.reverse_adjacency[current_monkey]:
            if monkey_value_dict[parent] is None:
                current_monkey=parent

    monkey_left = monkey_adjacency_dict['root'][0]
    monkey_right = monkey_adjacency_dict['root'][1]

    v0 = monkey_value_dict[monkey_left]
    v1 = monkey_value_dict[monkey_right]

    v_equality = None

    if v0 is not None:
        v_equality = v0
    else:
        v_equality = v1

    

    ans = (v_equality*b*d-b*c)//(a*d)

    str_out1 = str(a)+'/'+str(b)+' humn + '+str(c)+'/'+str(d)+' = '+str(v_equality)
    str_out2 = 'humn = '+str(ans)

    print(str_out1)
    print(str_out2)

    # print_operation_chain('root',operation_dict,monkey_adjacency_dict,monkey_value_dict)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

