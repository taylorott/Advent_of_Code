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

def parse_input(fname):
    data = bh.parse_strings(path,fname,delimiters = [' ','=',';',','],type_lookup = None, allInt = False, allFloat = False)

    rate_dict = {}
    valve_adjacency_dict = {}
    
    for line in data:
        valve_name = line[1]
        rate = int(line[5])

        v_out = []
        for i in range(10,len(line)):
            v_out.append(line[i])

        rate_dict[valve_name] = rate
        valve_adjacency_dict[valve_name] = v_out


    return rate_dict,valve_adjacency_dict

def serialize_state(current_valve,valves_opened,t_current):
    valves_opened_list = []

    for valve in valves_opened.keys():
        if valves_opened[valve]:
            valves_opened_list.append(valve)

    valves_opened_list.sort()

    return (current_valve,tuple(valves_opened_list),t_current)

def deserialize_state(key_in):
    current_valve = key_in[0]

    valves_opened = {}

    for valve in key_in[1]:
        valves_opened[valve]=True

    t_current = key_in[2]

    return current_valve, valves_opened, t_current


def compute_next_posssible_states(current_valve, valves_opened, t_current, dist_dict, rate_dict, tmax=30):
    list_out = []

    for next_valve in dist_dict[current_valve].keys():

        t_next = 1+dist_dict[current_valve][next_valve]+t_current

        if (next_valve not in valves_opened or not valves_opened[next_valve]) and t_next<tmax and next_valve!='AA':

            valves_opened[next_valve] = True

            score_increment = rate_dict[next_valve]*(tmax-t_next)
            next_state = serialize_state(next_valve,valves_opened,t_next)
            list_out.append([next_state,score_increment])

            valves_opened[next_valve] = False

    return list_out

def compute_dist_dict(rate_dict,valve_adjacency_dict):
    dist_dict = {}
    myGraph = Graph()

    for valve0 in valve_adjacency_dict.keys():
        for valve1 in valve_adjacency_dict[valve0]:
            myGraph.add_edge(valve0,valve1)

    for valve0 in valve_adjacency_dict.keys():
        dist_dict[valve0]={}

        output_dict = myGraph.compute_dist_BFS(valve0)

        for valve1 in valve_adjacency_dict.keys():
            if valve1 in output_dict['dist_dict'].keys():
                dist_dict[valve0][valve1] = output_dict['dist_dict'][valve1]
            elif valve1==valve0:
                dist_dict[valve0][valve1] = 0
            else:
                dist_dict[valve0][valve1] = np.inf

    pruned_dist_dict = {}
    
    for valve0 in rate_dict.keys():
        if valve0=='AA' or rate_dict[valve0]>0:
            pruned_dist_dict[valve0]={}
            for valve1 in rate_dict.keys():
                if valve1=='AA' or rate_dict[valve1]>0:
                    pruned_dist_dict[valve0][valve1] = dist_dict[valve0][valve1] 

    return pruned_dist_dict

def generate_score_table(rate_dict,dist_dict,tmax):
    serial_state = serialize_state('AA',{},0)

    score_dict = {serial_state: 0}
    visited_dict = {serial_state: None}

    myHeap = AugmentedHeap()
    myHeap.insert_item(serial_state[-1],serial_state)

    while not myHeap.isempty():
        current_time, serial_state = myHeap.pop()

        current_valve, valves_opened, t_current = deserialize_state(serial_state)

        next_state_list = compute_next_posssible_states(current_valve, valves_opened, t_current, dist_dict, rate_dict, tmax)


        for next_state in next_state_list:
            state_next = next_state[0]
            score_increment = next_state[1]
            next_score = score_dict[serial_state]+score_increment

            if state_next in score_dict:
                score_dict[state_next] = max(score_dict[state_next],next_score)
            else:
                score_dict[state_next] = next_score

            if state_next not in visited_dict:
                better_state_exists = False

                visited_dict[state_next]=None
                myHeap.insert_item(state_next[-1],state_next)

    return score_dict


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    rate_dict,valve_adjacency_dict = parse_input(fname)
    dist_dict = compute_dist_dict(rate_dict,valve_adjacency_dict)
    score_dict = generate_score_table(rate_dict,dist_dict,tmax=30)

    max_score = 0
    for item in score_dict.keys():
        max_score = max(max_score,score_dict[item])

    print(max_score)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    rate_dict,valve_adjacency_dict = parse_input(fname)

    dist_dict = compute_dist_dict(rate_dict,valve_adjacency_dict)
    score_dict = generate_score_table(rate_dict,dist_dict,tmax=26)

    subset_score_dict = {}
    for item in score_dict.keys():
        my_subset = item[1]
        my_score = score_dict[item]

        if my_subset in subset_score_dict:
            subset_score_dict[my_subset]=max(subset_score_dict[my_subset],my_score)
        else:
            subset_score_dict[my_subset]=my_score

    score_total = 0
    for key0 in subset_score_dict.keys():
        for key1 in subset_score_dict.keys():
            is_disjoint = True
            check_dict = {}
            for item in key0:
                check_dict[item]=None
            for item in key1:
                is_disjoint = is_disjoint and item not in check_dict

            if is_disjoint:
                score_total = max(score_total, subset_score_dict[key0]+subset_score_dict[key1])

    print(score_total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

