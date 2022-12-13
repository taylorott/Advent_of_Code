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

def compare_packets(packet0,packet1):
    islist0 = isinstance(packet0, list)
    islist1 = isinstance(packet1, list)

    if not islist0 and not islist1:
        if packet0<packet1:
            return -1
        if packet0==packet1:
            return 0
        if packet0>packet1:
            return 1

    elif islist0 and islist1:

        l0 = len(packet0)
        l1 = len(packet1)
        lmin = min(l0,l1)

        current_val = 0

        count = 0
        while count < lmin:
            item0 = packet0[count]
            item1 = packet1[count]
            temp_result = compare_packets(item0,item1)
            if temp_result!=0:
                return temp_result
            count+=1

        if l0==l1:
            return 0
        elif l0<l1:
            return -1
        elif l0>l1:
            return 1

    elif not islist0:
        return compare_packets([packet0],packet1)
    elif not islist1:
        return compare_packets(packet0,[packet1])

#a min heap by default
#can change to a max heap if desired
class packet_class(object):
    def __init__(self,data):
        self.data = data

    def __eq__(self, other):
        v = compare_packets(self.data,other.data)
        return v==0

    def __gt__(self, other):
        v = compare_packets(self.data,other.data)
        return v==1

    def __lt__(self, other):
        v = compare_packets(self.data,other.data)
        return v==-1

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    total = 0
    for i in range(len(data)):
        packet0 = packet_class(eval(data[i][0]))
        packet1 = packet_class(eval(data[i][1]))
        if packet0<packet1:
            total+=(i+1)

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # data = parse_input01(fname)

    data = parse_input01(fname)

    packet_list = []
    for i in range(len(data)):
        packet_list.append(packet_class(eval(data[i][0])))
        packet_list.append(packet_class(eval(data[i][1])))

    packet_list.append(packet_class([[2]]))
    packet_list.append(packet_class([[6]]))

    myHeap = AugmentedHeap()

    while len(packet_list)>0:
        myHeap.insert_item(packet_list.pop(-1),None)

    while not myHeap.isempty():
        key,val = myHeap.pop()
        packet_list.append(key)

    total = 1
    for i in range(len(packet_list)):
        if tuple(packet_list[i].data)==tuple([[2]]) or tuple(packet_list[i].data)==tuple([[6]]):
            total*=(i+1)

    print(total)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

