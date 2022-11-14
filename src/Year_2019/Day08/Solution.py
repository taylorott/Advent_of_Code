#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    return data[0]

def solution01():
    # fname = 'Input01.txt'
    # w = 3
    # h = 2
    
    fname = 'Input02.txt'
    w = 25
    h = 6
    
    data = parse_input01(fname)

 
    num_layers = int(len(data)/(w*h))

    my_stack = []

    for i in range(num_layers):
        my_stack.append([])
        for j in range(h):
            my_stack[i].append([])
            for k in range(w):
                my_stack[i][j].append(int(data[k+w*j+w*h*i]))

    my_stack = np.array(my_stack)

    equals_zero = 1.0*(my_stack == 0)

    num_zero =[]
    for i in range(num_layers):
        num_zero.append(sum(sum(equals_zero[i])))

    best_layer = np.argmin(num_zero)
 
    v=sum(sum(my_stack[best_layer]==1))*sum(sum(my_stack[best_layer]==2))
    print(v)

def solution02():
    # fname = 'Input01.txt'
    # w = 3
    # h = 2
    
    fname = 'Input02.txt'
    w = 25
    h = 6
    
    data = parse_input01(fname)

 
    num_layers = int(len(data)/(w*h))

    my_stack = []

    for i in range(num_layers):
        my_stack.append([])
        for j in range(h):
            my_stack[i].append([])
            for k in range(w):
                my_stack[i][j].append(int(data[k+w*j+w*h*i]))

    my_output = []  

    for i in range(h):
        my_output.append([])
        for j in range(w):
            k=0
            while my_stack[k][i][j]==2.0:
                k+=1
            my_output[i].append(int( my_stack[k][i][j]))

    for item in my_output:
        str_out = ''
        for val in item:
            if val==1:
                str_out+='I'
            else:
                str_out+=' '
        print(str_out)

if __name__ == '__main__':
    solution01()
    solution02()
    

