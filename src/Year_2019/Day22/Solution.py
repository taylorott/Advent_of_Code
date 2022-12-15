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

    for block in data:
        for i in range(len(block)):
            block[i] = parse_line(block[i])

    return data

def parse_line(line):
    words = line.split(' ')
    
    if words[0]=='cut':
        return ['cut',int(words[-1])]

    if words[2]=='new':
        return ['new']

    return ['inc',int(words[-1])]

#multiplicative inverse under modular operation (ripped from stack overflow)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
#multiplicative inverse under modular operation (ripped from stack overflow)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

def perform_operation(a,b,deck_size,command,reverse=False):
    if not reverse:
        if command[0]=='new':
            return (-a)%deck_size, (deck_size-1-b)%deck_size
        if command[0]=='cut':
            return a,(b-command[1])%deck_size
        if command[0]=='inc':
            return (a*command[1])%deck_size,(b*command[1])%deck_size
    elif reverse:
        if command[0]=='new':
            return (-a)%deck_size, (deck_size-1-b)%deck_size
        if command[0]=='cut':
            return a,(b+command[1])%deck_size
        if command[0]=='inc':
            return (a*modinv(command[1], deck_size))%deck_size,(b*modinv(command[1], deck_size))%deck_size

def execute_shuffle(deck_size,commands,reverse=False):
    a,b = 1,0

    if not reverse:
        for i in range(len(commands)):
            a,b = perform_operation(a,b,deck_size,commands[i],reverse)
    else:
        for i in range(len(commands)-1,-1,-1):
            a,b = perform_operation(a,b,deck_size,commands[i],reverse)

    return a,b

def test_shuffle01(data):

    for block in data:
        card_positions = []
        a,b = execute_shuffle(10,block)

        list_out = [None]*10
        for i in range(10):
            list_out[(a*i+b)%10]=i

        print(list_out)

def test_shuffle02(data):

    for block in data:
        list_out = []
        a,b = execute_shuffle(10,block,True)
        for i in range(10):
            list_out.append((a*i+b)%10)

        print(list_out)

def exponentiate(a,b,power,deck_size):
    a_out = 1
    b_out = 0

    a_current=a
    b_current=b

    bin_str = bin(power)

    for i in range(len(bin_str)-1,-1,-1):
        if bin_str[i]=='b':
            break
        elif bin_str[i]=='1':
            a_out = (a_current*a_out)%deck_size
            b_out = (a_current*b_out+b_current)%deck_size

        a_temp = (a_current*a_current)%deck_size
        b_temp = (a_current*b_current+b_current)%deck_size

        a_current = a_temp
        b_current = b_temp

    return a_out,b_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    deck_size = 10007
    a,b = execute_shuffle(deck_size,data[0])
    result = (a*2019+b)%deck_size

    print(result)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    deck_size = 119315717514047
    power = 101741582076661
    a,b = execute_shuffle(119315717514047,data[0],True)
    a,b = exponentiate(a,b,power,deck_size)
    
    result = (a*2020+b)%deck_size

    print(result)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

