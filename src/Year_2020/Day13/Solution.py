#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm

path = currentdir

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[',','x'],allInt=True)

    earliest_time = data[0][0]
    bus_list = data[1]

    # print(earliest_time)
    # print(bus_list)

    min_time = None
    min_ID = None
    for bus in bus_list:
        candidate_time = int(np.ceil(earliest_time/(bus*1.0)))*bus
        
        if min_time is None or candidate_time<min_time:
            min_time = candidate_time
            min_ID = bus

    print((min_time-earliest_time)*min_ID)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[','])

    earliest_time = data[0][0]
    bus_str_list = data[1]

    bus_list = []
    bus_dict = {}

    for i in range(len(bus_str_list)):
        item = bus_str_list[i]
        if item!='x':
            num = int(item)
            bus_list.append(num)
            bus_dict[num]=i

    # print(bus_dict)

    t = 0
    dt = 1

    for i in range(len(bus_list)):
        bus = bus_list[i]
        target_mod = (-bus_dict[bus])%bus

        while t%bus!=target_mod:
            t+=dt
        dt=lcm(dt,bus)
    print(t)


if __name__ == '__main__':
    solution01()
    solution02()
    

