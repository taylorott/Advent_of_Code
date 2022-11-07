#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import Helpers.basic_helpers as bh

path = '/home/taylorott/Documents/Advent_of_Code/src/Year_2020/Day03'

def solution01():
    # fname = 'test.txt'
    fname = 'Input01.txt'

    data = bh.parse_strings(path,fname)

    height = len(data)
    width = len(data[0])

    i = 0
    j = 0

    di = 1
    dj = 3

    num_trees = 0

    while i<height:
        if data[i][j]=='#':
            num_trees+=1

        i+=di
        j+=dj

        j=j%width

    print(num_trees)

def solution02():
    # fname = 'test.txt'
    fname = 'Input01.txt'

    data = bh.parse_strings(path,fname)

    height = len(data)
    width = len(data[0])

    slope_list = [(1,1),(3,1),(5,1),(7,1),(1,2)]


    cum_prod = 1
    for slope in slope_list:
        i = 0
        j = 0

        di = slope[1]
        dj = slope[0]

        num_trees = 0

        while i<height:
            if data[i][j]=='#':
                num_trees+=1

            i+=di
            j+=dj

            j%=width

        cum_prod*=num_trees

    print(cum_prod)




if __name__ == '__main__':
    solution01()
    solution02()
    

