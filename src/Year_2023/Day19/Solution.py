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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    rule_list = data[0]

    part_list = []

    for item in data[1]:
        dict_string = item.replace('=',':')
        dict_string = dict_string.replace('{','')
        dict_string = dict_string.replace('}','')
        dict_out = bh.convert_strings_to_dict([dict_string])

        for key in dict_out:
            dict_out[key]=int(dict_out[key])
        part_list.append(dict_out)

    return rule_list, part_list

def parse_operation(operation_string):
    operation_string = operation_string.replace('<',' < ')
    operation_string = operation_string.replace('>',' > ')
    operation_string = operation_string.replace(':',' : ')

    symbol_list = operation_string.split(' ')

    if len(symbol_list)>1:
        symbol_list[2]=int(symbol_list[2])
    
    return symbol_list

def parse_rule(rule):
    rule = rule.replace('{',' ')
    rule = rule.replace('}','')

    temp_list = rule.split(' ')
    rule_label = temp_list[0]
    operations_string = temp_list[1]
    operation_string_list = operations_string.split(',')

    operation_list = []

    for operation in operation_string_list:
        symbol_list = parse_operation(operation)
        operation_list.append(symbol_list)
    
    return rule_label, operation_list

def build_workflow_dict(rule_list):
    workflow_dict = {}

    for rule in rule_list:
        rule_label, operation_list = parse_rule(rule)
        workflow_dict[rule_label] = operation_list

    return workflow_dict

def perform_comparison(operation,part_dict):
    q1 = part_dict[operation[0]]
    q2 = operation[2]
    comparison_operator = operation[1]

    if q1 < q2 and comparison_operator=='<':
        return True

    if q1 > q2 and comparison_operator=='>':
        return True

    return False

def run_operation(workflow_dict,part_dict,rule_label):
    operation_list = workflow_dict[rule_label]

    for operation in operation_list:
        if len(operation)==1 or perform_comparison(operation,part_dict):

            next_rule_label = operation[-1]

            if next_rule_label=='A' or next_rule_label=='R':
                return next_rule_label
            else:
                return run_operation(workflow_dict,part_dict,next_rule_label)

#operation is a list describing a comparison operation
#[part_dict_key, ('<' or '>'),  value to compare against, output if comparison returns true]

#part_dict is a dictionary describing a set of value combinations for a part
#{'x':list of ints, 'm': list of ints, 'a': list of ints, 's': list of ints}

#this function returns part_dict_true and part_dict_false
#each are dictionaries of the same form as the input part_dict
#part_dict_true corresponds to the value combinations that return true for the comparison
#part_dict_false corresponds to the value combinations that return false for the comparison
def nondeterministic_comparison(operation,part_dict):
    comparison_key = operation[0]

    #initialize the part dicts
    
    part_dict_true = {}
    part_dict_false = {}

    for temp_key in part_dict:
        if temp_key!= comparison_key:
            part_dict_true[temp_key]=list(part_dict[temp_key])
            part_dict_false[temp_key]=list(part_dict[temp_key])
        else:
            part_dict_true[temp_key]=[]
            part_dict_false[temp_key]=[]

    q2 = operation[2]
    comparison_operator = operation[1]

    for q1 in part_dict[comparison_key]:
        if (q1 < q2 and comparison_operator=='<') or (q1 > q2 and comparison_operator=='>'):
            part_dict_true[comparison_key].append(q1)
        else:
            part_dict_false[comparison_key].append(q1)

    return part_dict_true,part_dict_false


#part_dict is a dictionary describing a set of value combinations for a part
#{'x':list of ints, 'm': list of ints, 'a': list of ints, 's': list of ints}

#this function returns the number of combinations described by part_dict
#which is just the product of the length of the lists
def count_nondeterministic_possibilities(part_dict):
    total = 1
    for key in part_dict:
        total*=len(part_dict[key])
    return total

def run_nondeterministic_operation(workflow_dict,part_dict,rule_label):
    operation_list = workflow_dict[rule_label]

    total = 0

    for operation in operation_list:
        if len(operation)==1:
            if operation[-1]=='A':
                total+=count_nondeterministic_possibilities(part_dict)

            elif operation[-1]!='R':
                total+=run_nondeterministic_operation(workflow_dict,part_dict,operation[-1])

        else:
            part_dict_true,part_dict_false = nondeterministic_comparison(operation,part_dict)

            if operation[-1]=='A':
                total+=count_nondeterministic_possibilities(part_dict_true)
            elif operation[-1]!='R':
                total+=run_nondeterministic_operation(workflow_dict,part_dict_true,operation[-1])

            part_dict = part_dict_false

    return total

def solution01(show_result=True, fname='Input02.txt'):
    rule_list, part_list = parse_input01(fname)
    workflow_dict = build_workflow_dict(rule_list)

    total = 0
    for part_dict in part_list:
        result = run_operation(workflow_dict,part_dict,'in')
        
        if result=='A':
            for key in part_dict:
                total+=part_dict[key]

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):
    rule_list, part_list = parse_input01(fname)
    workflow_dict = build_workflow_dict(rule_list)

    part_dict = {'x':list(range(1,4001)),'m':list(range(1,4001)),'a':list(range(1,4001)),'s':list(range(1,4001))}

    total = run_nondeterministic_operation(workflow_dict,part_dict,'in')

    if show_result: print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

