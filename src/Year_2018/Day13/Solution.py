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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    cart_list = []

    for i in range(len(data)):
        for j in range(len(data[0])):
            c = data[i][j]
            if c in cart_to_track:
                cart_list.append([(i,j),c,0])

    return data, cart_list

motion_dict = {'<':(0,-1),'>':(0,1),'^':(-1,0),'v':(1,0)}

l_dict = {'>':'^','^':'<','<':'v','v':'>'}
s_dict = {'>':'>','^':'^','<':'<','v':'v'}
r_dict = {'>':'v','v':'<','<':'^','^':'>'}
turn_list = [l_dict,s_dict,r_dict]

bounce_fs = {'>':'^','^':'>','v':'<','<':'v'}
bounce_bs = {'>':'v','v':'>','<':'^','^':'<'}

cart_to_track = {'>':'-','<':'-','v':'|','^':'|'}

def update_cart(cart,grid_in):
    i = cart[0][0]
    j = cart[0][1]
    c = cart[1]
    turn_num = cart[2]

    motion = motion_dict[c]
    i+=motion[0]
    j+=motion[1]

    if grid_in[i][j] == '/':
        c = bounce_fs[c]
    if grid_in[i][j] == '\\':
        c = bounce_bs[c]
    if grid_in[i][j] == '+':
        c = turn_list[turn_num%3][c]
        turn_num+=1

    cart[0] = (i,j)
    cart[1] = c
    cart[2] = turn_num

def cart_compare(a,b):
    if a[0]>b[0]: return 1
    if a[0]<b[0]: return -1
    if a[0]==b[0]:
        if a[1]>b[1]: return 1
        if a[1]<b[1]: return -1
        if a[1]==b[1]: return 0

def update_carts(cart_list,grid_in,remove_carts=False):
    cart_list.sort(key=cmp_to_key(cart_compare))
    
    prev_coords,next_coords = set(), set()
    for cart in cart_list: prev_coords.add(cart[0])

    to_do_list = []
    while len(cart_list)>0: to_do_list.append(cart_list.pop(-1))

    cc = None
    while len(to_do_list)>0:
        cart = to_do_list.pop(-1)

        prev_coords.discard(cart[0])
        update_cart(cart,grid_in)
        coord = cart[0]

        if coord in next_coords or coord in prev_coords:
            if remove_carts:
                next_coords.discard(coord)
                prev_coords.discard(coord)

                k = 0
                while k<len(cart_list):
                    if cart_list[k][0]==coord: cart_list.pop(k)
                    else: k+=1

                k = 0
                while k<len(to_do_list):
                    if to_do_list[k][0]==coord: to_do_list.pop(k)
                    else: k+=1
            else:
                cc = coord
                break
        else: 
            next_coords.add(coord)
            cart_list.append(cart)

    return cc

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    grid,cart_list = parse_input01(fname)

    cc = None
    while cc is None:
        cc = update_carts(cart_list,grid)

    print(str(cc[1])+','+str(cc[0]))

def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    grid,cart_list = parse_input01(fname)

    while len(cart_list)>1:
        update_carts(cart_list,grid,True)
    cc = cart_list[0][0]
    
    print(str(cc[1])+','+str(cc[0]))

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

