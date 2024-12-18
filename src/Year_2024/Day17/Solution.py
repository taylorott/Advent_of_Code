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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_extract_ints_split_by_emptylines(path,fname)
    data = bh.parse_extract_ints(path,fname)

    return data

def get_operand(instructions, instruction_pointer, state_list):
    operand = instructions[instruction_pointer+1]

    if 0<=operand and operand<=3: return operand

    if operand==4: return state_list[0]

    if operand==5: return state_list[1]

    if operand==6: return state_list[2]

def run_program(instructions, state_list):
    instruction_pointer = 0

    output = []
    result = ''
    while instruction_pointer<len(instructions):
        q = instructions[instruction_pointer]
        combo_operand = get_operand(instructions, instruction_pointer, state_list)
        literal_operand = instructions[instruction_pointer+1]

        instruction_pointer+=2
        if q==0:

            state_list[0]//=(2**combo_operand)
        if q==1:

            state_list[1]^=literal_operand

        if q==2:

            state_list[1]=combo_operand%8

        if q==3:
            if state_list[0]!=0:
                instruction_pointer = literal_operand
        if q==4:
            state_list[1]^=state_list[2]
        if q==5:
            output.append(combo_operand%8)
            result+=str(combo_operand%8)+','

        if q==6:
            state_list[1]= state_list[0]//(2**combo_operand)
        if q==7:
            state_list[2]= state_list[0]//(2**combo_operand)

    result = result[0:(len(result)-1)]

    return result



def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    A = data[0][0]
    B = data[1][0]
    C = data[2][0]

    state_list = [A,B,C]

    instructions = data[4]

    result = run_program(instructions, state_list)

    print(result)




def digit_fromA(A):
    B = A%8
    B^=1
    C = A//(2**B)
    B^=5
    B^=C

    return B%8

def computeA_recursive(instructions,A=0):
    if len(instructions)==0: return A

    item = instructions.pop(-1)

    for i in range(8):
        if digit_fromA(A*8+i)==item:
            test = computeA_recursive(instructions,A*8+i)
            if test is not None:
                return test

    instructions.append(item)
    return None

def solution02():
    fname = 'Input02.txt'

    data = parse_input01(fname)

    instructions = data[4]

    result = computeA_recursive(instructions)

    print(result)




if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

