#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph

path = currentdir



direction_dict = {'N':np.array([0,1]),'S':np.array([0,-1]),'E':np.array([1,0]),'W':np.array([-1,0])}
heading_circle = ['E','N','W','S']

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    heading_index = 0

    coords = np.array([0,0])

    for item in data:
        command = item[0]
        num = int(item[1:])

        if command in direction_dict:
            coords+=direction_dict[command]*num
        elif command == 'F':
            coords+=direction_dict[heading_circle[heading_index]]*num
        elif command == 'R':
            heading_index-=int(num/90)
            heading_index%=4
        elif command == 'L':
            heading_index+=int(num/90)
            heading_index%=4

    print(abs(coords[0])+abs(coords[1]))

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = bh.parse_strings(path,fname)

    waypoint = np.array([10,1])

    coords = np.array([0,0])

    for item in data:
        command = item[0]
        num = int(item[1:])

        if command in direction_dict:
            waypoint+=direction_dict[command]*num
        elif command == 'F':
            coords+=waypoint*num
        elif command == 'R':
            num_rot=int(num/90)

            for i in range(num_rot):
                waypoint=np.array([waypoint[1],-waypoint[0]])
            
        elif command == 'L':
            num_rot=int(num/90)

            for i in range(num_rot):
                waypoint=np.array([-waypoint[1],waypoint[0]])
            
    print(abs(coords[0])+abs(coords[1]))


if __name__ == '__main__':
    solution01()
    solution02()
    

