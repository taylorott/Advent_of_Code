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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

#build almanac out of input text
#almanac is in the form of a dictionary
#
#almanac_dict['starting_vals'] = initial seed number data (list of ints)
#which is interpreted differently between parts 1 and 2
#
#almanac_dict[key_in] = map_dict
#where key_in is a label for a given key_in-to-key_out map in the almanac
#
#almanac_dict[key_in]['next_key']=key_out
#almanac_dict[key_in]['range_maps'] is a list of list of ints describing
#the conversion formula in the almanac, 
#where each sub-list has the form [left,right,delta]
#where if left<= x <= right, you add delta to x, otherwise you leave x unchanged
def build_dictionaries(data):

    seed_vals_strings = data[0][0].split(' ')
    seed_vals_list = []

    for i in range(1,len(seed_vals_strings)):
        seed_vals_list.append(int(seed_vals_strings[i]))

    almanac_dict = {'starting_vals':seed_vals_list}

    for i in range(1,len(data)):
        current_map = data[i]

        map_string = current_map[0].split(' ')[0].split('-')
        
        key0 = map_string[0]
        key1 = map_string[2]

        range_maps = []
        for j in range(1,len(current_map)):
            range_strings = current_map[j].split(' ')
            range_list = []

            left_boundary = int(range_strings[1])
            right_boundary = left_boundary+int(range_strings[2])-1
            delta = int(range_strings[0])-left_boundary

            range_maps.append([left_boundary,right_boundary,delta])

        map_dict = {'next_key':key1,'range_maps':range_maps}
        almanac_dict[key0]=map_dict

    return almanac_dict

#simplify a list of intervals of the form [[l_0,r_0],...,[l_i,r_i],...,[l_n,r_n]]
#where l_i <= r_i for all i
#the output list has the form  [[a_0,b_0],...,[a_i,b_i],...,[a_n,b_n]]
#where a_i<=b_i and b_i<a_(i+1) for all i
#in other words, find reduce the input list of intervals into the corresponding
#sorted list of disjoint intervals 
def simplify_interval_list(input_interval_list):
    sorted_interval_list = sorted(input_interval_list, key=lambda interval: interval[0])
    simplified_interval_list = []

    for val_range in sorted_interval_list:
        if len(simplified_interval_list)==0:
            simplified_interval_list.append(val_range)
        elif val_range[0]<=simplified_interval_list[-1][1]:
            simplified_interval_list[-1][1]=max(simplified_interval_list[-1][1],val_range[1])
        else:
            simplified_interval_list.append(val_range)
    return simplified_interval_list

#apply a single line of the forward map of the almanac to an interval
#the output is two lists of intervals
#changed_intervals: the sub_intervals that were changed by applying the forward map
#unchanged_intervals: the sub_intervals that remained the same after applying the forward map
def apply_single_forward_map_to_interval(input_interval,forward_map):

    unchanged_intervals = []
    changed_intervals = []

    left_boundary = forward_map[0]
    right_boundary = forward_map[1]
    delta = forward_map[2]
    

    if input_interval[0]<left_boundary:
        unchanged_intervals.append([input_interval[0],min(left_boundary-1,input_interval[1])])

    if input_interval[1]>right_boundary:
        unchanged_intervals.append([max(right_boundary+1,input_interval[0]),input_interval[1]])

    if not (input_interval[1]<left_boundary or right_boundary<input_interval[0]):
        changed_intervals.append([max(left_boundary,input_interval[0])+delta,min(right_boundary,input_interval[1])+delta])

    return unchanged_intervals,changed_intervals

#execute a conversion step in the almanac
#input_interval_list is sorted list of disjoint intervals
#forward_map_list is the list of formulas to apply for the current conversion step
def update_intervals_single_iteration(input_interval_list,forward_map_list):

    unchanged_intervals = input_interval_list
    changed_intervals = []
    for forward_map in forward_map_list:
        remaining_unchanged_intervals = []
        for current_interval in unchanged_intervals:
            unchanged_intervals_temp, changed_intervals_temp = apply_single_forward_map_to_interval(current_interval,forward_map)

            changed_intervals+=changed_intervals_temp
            remaining_unchanged_intervals+=unchanged_intervals_temp

        unchanged_intervals = remaining_unchanged_intervals

    return simplify_interval_list(unchanged_intervals+changed_intervals)

#execute all conversion steps in the almanac
def compute_final_intervals(input_intervals,current_key,almanac_dict):
    if current_key == 'location':
        return input_intervals

    map_dict = almanac_dict[current_key]
    next_key = map_dict['next_key']
    range_maps = map_dict['range_maps']

    next_intervals = update_intervals_single_iteration(input_intervals,range_maps)

    return compute_final_intervals(next_intervals,next_key,almanac_dict)


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    almanac_dict = build_dictionaries(parse_input01(fname))

    starting_intervals = []

    starting_val_list = almanac_dict['starting_vals']
    for val in starting_val_list:
        starting_intervals.append([val,val])

    ranges_out = compute_final_intervals(starting_intervals,'seed',almanac_dict)
    print(ranges_out[0][0])

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    almanac_dict = build_dictionaries(parse_input01(fname))

    starting_intervals = []

    starting_val_list = almanac_dict['starting_vals']
    for i in range(len(starting_val_list)//2):
        starting_intervals.append([starting_val_list[2*i],starting_val_list[2*i] + starting_val_list[2*i+1]-1])

    ranges_out = compute_final_intervals(starting_intervals,'seed',almanac_dict)
    print(ranges_out[0][0])


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

