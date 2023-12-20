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
    data = bh.parse_strings(path,fname,delimiters = [' ',','],type_lookup = None, allInt = False, allFloat = False)

    return data

def build_module_dictionaries(data):
    forward_adjacency_dict = {}
    reverse_adjacency_dict = {}
    type_dict = {}

    forward_adjacency_dict['button']=['broadcaster']
    reverse_adjacency_dict['broadcaster']=['button']
    reverse_adjacency_dict['button']=[]

    type_dict['button']='button'

    for module_list in data:
        module_str = module_list[0]

        module_type = None
        module_name = None

        if module_str == 'broadcaster':
            module_type = 'broadcaster'
            module_name = 'broadcaster'
        else:
            module_type = module_str[0]
            module_name = module_str[1:]

        forward_adjacency_dict[module_name] = module_list[2:]

        if module_name not in reverse_adjacency_dict:
            reverse_adjacency_dict[module_name]=[]

        for item in module_list[2:]:
            if item not in forward_adjacency_dict:
                forward_adjacency_dict[item]=[]
            if item not in reverse_adjacency_dict:
                reverse_adjacency_dict[item]=[]

            reverse_adjacency_dict[item].append(module_name)

        type_dict[module_name] = module_type


    return forward_adjacency_dict, reverse_adjacency_dict, type_dict

def initialize_conjunction_dict(forward_adjacency_dict, type_dict):
    memory_dict = {}
    for module_name in type_dict:
        memory_dict[module_name] = {}

    for module_name in forward_adjacency_dict:
        for destination_module_name in forward_adjacency_dict[module_name]:
            if destination_module_name in memory_dict:
                memory_dict[destination_module_name][module_name]=False

    return memory_dict

def initialize_flip_flop_dict(forward_adjacency_dict, type_dict):
    flip_flop_state_dict = {}
    for module_name in type_dict:
        flip_flop_state_dict[module_name]=False

    return flip_flop_state_dict

def update_conjunction_module(memory_dict,module_name,input_module_name,pulse_val):
    memory_dict[module_name][input_module_name] = pulse_val

    val = True

    for key in memory_dict[module_name]:
        val = val and memory_dict[module_name][key]


    return not val

def update_flip_flop_module(flip_flop_state_dict, module_name, pulse_val):
    if not pulse_val:
        flip_flop_state_dict[module_name] = not flip_flop_state_dict[module_name]
    return flip_flop_state_dict[module_name]


def run_on_input_pulse(forward_adjacency_dict, type_dict,memory_dict,flip_flop_state_dict,input_pulse):
    pulse_queue = deque()
    pulse_queue.append(input_pulse)

    low_count = 0
    high_count = 0

    pulse_dict_out = {}


    while len(pulse_queue)>0:
        pulse = pulse_queue.popleft()

        module_name = pulse[0]
        pulse_val = pulse[1]
        input_module_name = pulse[2]

        if module_name in type_dict:
            destination_list = forward_adjacency_dict[module_name]
            module_type = type_dict[module_name]

            send_pulse = True
            output_val = None

            if module_type=='broadcaster' or module_type=='button':
                output_val = pulse_val
            elif module_type=='%':
                if not pulse_val:
                    flip_flop_state_dict[module_name] = not flip_flop_state_dict[module_name]
                    output_val = flip_flop_state_dict[module_name]
                else:
                    send_pulse = False
            elif module_type=='&':
                output_val = update_conjunction_module(memory_dict,module_name,input_module_name,pulse_val)

            val_str = None

            if output_val:
                val_str = ' -high-> '
            else:
                val_str = ' -low-> '
            
            if send_pulse:
                for destination_module_name in destination_list:
                    if output_val:
                        high_count+=1
                    else:
                        low_count+=1

                    output_pulse = [destination_module_name,output_val,module_name]

                    if destination_module_name not in pulse_dict_out:
                        pulse_dict_out[destination_module_name]=[output_pulse]
                    else:
                        pulse_dict_out[destination_module_name].append(output_pulse)
                    pulse_queue.append(output_pulse)



    return low_count,high_count, pulse_dict_out

def run1000times(forward_adjacency_dict, type_dict):

    memory_dict = initialize_conjunction_dict(forward_adjacency_dict, type_dict)
    flip_flop_state_dict = initialize_flip_flop_dict(forward_adjacency_dict, type_dict)
    
    low_total = 0
    high_total = 0
    input_pulse = ['button',False,None]

    for i in range(1000):
        low_count,high_count,pulse_dict_out = run_on_input_pulse(forward_adjacency_dict, type_dict,memory_dict,flip_flop_state_dict,input_pulse)

        low_total+=low_count
        high_total+=high_count


    return low_total*high_total
 

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    forward_adjacency_dict, reverse_adjacency_dict, type_dict = build_module_dictionaries(data)
    
    
    total = run1000times(forward_adjacency_dict, type_dict)
    print(total)

def find_period(forward_adjacency_dict, reverse_adjacency_dict, type_dict, 
                input_sequence,input_period,observe_list,destination_module_list):
    state_set = set()

    output_sequence_dict = {}

    for destination_module_name in destination_module_list:
        output_sequence_dict[destination_module_name]=[]
    


    memory_dict = initialize_conjunction_dict(forward_adjacency_dict, type_dict)
    flip_flop_state_dict = initialize_flip_flop_dict(forward_adjacency_dict, type_dict)

    current_state_list = []
    for module in observe_list:
        current_state_list.append(flip_flop_state_dict[module])
        state_set.add(tuple(current_state_list))
    
    turn_number=0
    while True:
        for input_command in input_sequence:
            input_pulse = input_command[0:3]
            low_count,high_count,pulse_dict_out = run_on_input_pulse(forward_adjacency_dict, type_dict,memory_dict,flip_flop_state_dict,input_pulse)

            for destination_module_name in destination_module_list:
                if destination_module_name in pulse_dict_out:
                    for output_pulse in pulse_dict_out[destination_module_name]:
                        output_sequence_dict[destination_module_name].append(output_pulse+[input_command[-1]+turn_number])

        turn_number+=input_period

        current_state_list = []
        for module in observe_list:
            current_state_list.append(flip_flop_state_dict[module])
            
        if tuple(current_state_list) in state_set:
            break
        else:
            state_set.add(tuple(current_state_list))

    return turn_number, output_sequence_dict


def buildGraph(forward_adjacency_dict, reverse_adjacency_dict):
    myGraph = Digraph()

    for v1 in forward_adjacency_dict:
        for v2 in forward_adjacency_dict[v1]:
            myGraph.add_edge(v1,v2)

    myGraph.build_metagraph()


    input_dict = {}
    output_dict = {}
    
    for meta_label in myGraph.assigned_lookup:
        input_dict[meta_label] = []
        output_dict[meta_label] = []
        for v0 in myGraph.assigned_lookup[meta_label]:
            for v_input in reverse_adjacency_dict[v0]:
                if myGraph.assigned_dict[v_input]!=meta_label:
                    input_dict[meta_label].append([v_input,v0])
            for v_output in forward_adjacency_dict[v0]:
                if myGraph.assigned_dict[v_output]!=meta_label:
                    output_dict[meta_label].append([v_output,v0])

    return myGraph, input_dict, output_dict

def find_rx_steps(forward_adjacency_dict, reverse_adjacency_dict, type_dict, myGraph, input_dict, output_dict):
    sequence_dict = {}
    period_dict = {}

    sequence_dict['button']={'broadcaster':[['broadcaster',False,'button',0]]}
    period_dict[0]=1

    meta_queue = deque()
    meta_queue.append(1)

    while len(meta_queue)>0:
        meta_label = meta_queue.pop()
        input_sequence = meta_label

        if len(input_dict[meta_label])>1:
            continue
        else:

            observe_list = myGraph.assigned_lookup[meta_label]
            
            input_module = input_dict[meta_label][0][0]
            starting_module = input_dict[meta_label][0][1]
            input_sequence = sequence_dict[input_module][starting_module]
            input_period = period_dict[myGraph.assigned_dict[input_module]]

            destination_module_list = []
            output_module = None

            for item in output_dict[meta_label]: 
                destination_module_list.append(item[0])
                output_module = item[1]


            period, output_sequence_dict = find_period(forward_adjacency_dict, reverse_adjacency_dict, type_dict,
                input_sequence,input_period,observe_list,destination_module_list)

            period_dict[meta_label] = period

            sequence_dict[output_module] = {}

            for key in output_sequence_dict:
                sequence_dict[output_module][key] = output_sequence_dict[key]

            for destination_module_name in destination_module_list:
                meta_queue.append(myGraph.assigned_dict[destination_module_name])


    total = 1

    for key in period_dict:
        total = lcm(total,period_dict[key])

    print(total)



def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    forward_adjacency_dict, reverse_adjacency_dict, type_dict = build_module_dictionaries(data)
    myGraph, input_dict, output_dict = buildGraph(forward_adjacency_dict, reverse_adjacency_dict)
    find_rx_steps(forward_adjacency_dict, reverse_adjacency_dict, type_dict, myGraph, input_dict, output_dict)
    
    


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

