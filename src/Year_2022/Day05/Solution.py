#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False)

    return data[0],data[1]

def parse_commands(command_list_in):

    list_out = []

    for item in command_list_in:
        temp_list = item.split(' ')
        temp_list = [int(temp_list[1]),int(temp_list[3]),int(temp_list[5])]
        list_out.append(temp_list)

    return list_out

def parse_cargo(cargo_list):
    max_len = 0 
    list_out = []
    for item in cargo_list:
        temp_list = []
        count = 1
        while count<len(item):
            temp_list.append(item[count])
            count+=4

        max_len = max(max_len,len(temp_list))
        list_out.append(temp_list)

    for item in list_out:
        while len(item)<max_len:
            item.append(' ')

    return list_out

def convert_cargo_to_stacks(cargo):
    stack_list = []
    for i in range(len(cargo[0])):
        stack_list.append([])

        j = len(cargo)-2
        while j>=0 and cargo[j][i]!=' ':
            stack_list[i].append(cargo[j][i])
            j-=1

    return stack_list

def run_operation1(stack_list,command):
    index1 = command[1]-1
    index2 = command[2]-1

    for i in range(command[0]):
        stack_list[index2].append(stack_list[index1].pop(-1))


def run_operation2(stack_list,command):
    index1 = command[1]-1
    index2 = command[2]-1

    for i in range(command[0]):
        stack_list[index2].append(stack_list[index1][i-command[0]])
    for i in range(command[0]):
        stack_list[index1].pop(-1)

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    cargo,commands = parse_input01(fname)

    commands = parse_commands(commands)
    cargo = parse_cargo(cargo)
    stack_list = convert_cargo_to_stacks(cargo)

    for command in commands:
        run_operation1(stack_list,command)

    str_out = ''
    for stack in stack_list:
        str_out+=stack[-1]
    print(str_out)


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    cargo,commands = parse_input01(fname)

    commands = parse_commands(commands)
    cargo = parse_cargo(cargo)
    stack_list = convert_cargo_to_stacks(cargo)

    for command in commands:
        run_operation2(stack_list,command)

    str_out = ''
    for stack in stack_list:
        str_out+=stack[-1]
    print(str_out)

if __name__ == '__main__':
    solution01()
    solution02()
    

