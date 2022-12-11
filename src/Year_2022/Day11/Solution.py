#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph, frequency_table
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [':',' ',','])
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    monkeys_list = []
    lcm_divisors = 1
    for monkey in data:
        monkey_dict = {}
        for i in range(len(monkey)):
            items = monkey[i]
                    
            starting_items = []
            for j in range(2,len(monkey[1])):
                starting_items.append(int(monkey[1][j]))
            monkey_dict['held_items'] = starting_items

            monkey_dict['operator'] = monkey[2][-2]

            left_operand = monkey[2][-3]
            if left_operand.isnumeric():
                left_operand = int(left_operand)
            monkey_dict['left_operand'] = left_operand 

            right_operand = monkey[2][-1]
            if right_operand.isnumeric():
                right_operand = int(right_operand)
            monkey_dict['right_operand'] = right_operand 

            monkey_dict['test'] =  int(monkey[3][-1])
            lcm_divisors = lcm(lcm_divisors,monkey_dict['test'] )

            monkey_dict['true'] = int(monkey[4][-1])
            monkey_dict['false'] = int(monkey[5][-1])

            monkey_dict['num_inspections']=0
        monkeys_list.append(monkey_dict)

    return monkeys_list,lcm_divisors

def eval_monkey_round(monkeys_list,lcm_divisors=None):
    
    for current_monkey in monkeys_list:
        held_items = current_monkey['held_items']

        current_monkey['held_items'] = []
        test = current_monkey['test']

        for item in held_items:
            current_monkey['num_inspections']+=1
            left_operand = current_monkey['left_operand']
            right_operand = current_monkey['right_operand']
            operator = current_monkey['operator']

            if left_operand == 'old':
                left_operand = item

            if right_operand == 'old':
                right_operand = item

            result = None

            if operator == '+':
                result = left_operand+right_operand

            if operator == '*':
                result = left_operand*right_operand

            if lcm_divisors is not None:
                result%=lcm_divisors
            else:
                result//=3

            if result%test==0:
                monkeys_list[current_monkey['true']]['held_items'].append(result)
            else:
                monkeys_list[current_monkey['false']]['held_items'].append(result)

def eval_inspections_score(monkeys_list,num_rounds,lcm_divisors=None):
    
    for i in range(num_rounds):
        eval_monkey_round(monkeys_list, lcm_divisors)
    
    inspection_list = []
    for monkey in monkeys_list:
        inspection_list.append(monkey['num_inspections'])

    inspection_list.sort()
    print(inspection_list[-1]*inspection_list[-2])

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    monkeys_list, lcm_divisors = parse_input01(fname)
    
    eval_inspections_score(monkeys_list,20)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    monkeys_list, lcm_divisors = parse_input01(fname)

    eval_inspections_score(monkeys_list,10000,lcm_divisors)

if __name__ == '__main__':
    solution01()
    solution02()
    

