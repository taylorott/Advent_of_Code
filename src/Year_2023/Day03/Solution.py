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
    return bh.parse_char_grid(path,fname)

def is_digit(char_in):
    return '0'<=char_in and char_in<='9'

def is_symbol(char_in):
    return (not is_digit(char_in)) and char_in!='.'

def check_validity(char_dict,i,j):
    is_valid = False

    for delta_i in range(-1,2):
        for delta_j in range(-1,2):
            key = (i+delta_i,j+delta_j)
            is_valid = is_valid or (key in char_dict and is_symbol(char_dict[key]))

    return is_valid

def convert_to_padded_char_dict(grid_in):
    h = len(grid_in)
    w = len(grid_in[0])

    char_dict = {}
    for i in range(h):
        for j in range(w):
            key = (i,j)
            char_dict[key]=grid_in[i][j]

    for i in range(-1,h+1):
        char_dict[(i,-1)]='.'
        char_dict[(i,w)]='.'

    for j in range(-1,w+1):
        char_dict[(-1,j)]='.'
        char_dict[(h,j)]='.'

    return char_dict

def add_gear_coords(char_dict,gear_coords,i,j):
    for delta_i in range(-1,2):
        for delta_j in range(-1,2):
            key = (i+delta_i,j+delta_j)
            if key in char_dict and char_dict[key]=='*':
                gear_coords.add(key)

def solution01(show_result=True, fname='Input02.txt'):

    data = parse_input01(fname)

    h = len(data)
    w = len(data[0])

    char_dict = convert_to_padded_char_dict(data)

    total = 0
    for i in range(h):
        current_number = None
        is_valid = False

        for j in range(w+1):
            key = (i,j)

            current_char = char_dict[key]
            if is_digit(current_char):
                current_digit = ord(current_char)-ord('0')

                if current_number is None:
                    current_number = current_digit
                else:
                    current_number = current_number*10+current_digit

                is_valid = is_valid or check_validity(char_dict,i,j)

            elif current_number is not None:
                if is_valid:
                    total+=current_number
                current_number = None
                is_valid = False

    if show_result: print(total)

    return total

def solution02(show_result=True, fname='Input02.txt'):

    data = parse_input01(fname)

    h = len(data)
    w = len(data[0])

    char_dict = convert_to_padded_char_dict(data)

    gear_dict = {}
    for i in range(h):
        current_number = None
        
        gear_coords = set()

        for j in range(w+1):
            key = (i,j)

            current_char = char_dict[key]
            
            if is_digit(current_char):
                current_digit = ord(current_char)-ord('0')

                if current_number is None:
                    current_number = current_digit
                else:
                    current_number = current_number*10+current_digit
                add_gear_coords(char_dict,gear_coords,i,j)

            elif current_number is not None:
                for gear in gear_coords:
                    if gear in gear_dict:
                        gear_dict[gear].append(current_number)
                    else:
                        gear_dict[gear]=[current_number]
                current_number = None
                gear_coords = set()

    total = 0

    for gear in gear_dict:
        if len(gear_dict[gear])==2:
            total+=gear_dict[gear][0]*gear_dict[gear][1]

    if show_result: print(total)

    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))