#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh

path = currentdir

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    for item in data:
        split_str01 = item[0:-1].split('contain ')
        outer = split_str01[0]
        inner_bags = split_str01[1].split(', ')
        outer = outer[0:-6]
        inner_list = []

        # print(inner_bags)
        
        if inner_bags[0]!='no other bags':
            for inner in inner_bags:
                split_str02 = inner.split(' ',1)
                num_bags = int(split_str02[0])

                if num_bags==1:
                    inner_list.append((num_bags,split_str02[1][0:-4]))
                else:
                    inner_list.append((num_bags,split_str02[1][0:-5]))

        print(outer+' : '+str(inner_list))

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

if __name__ == '__main__':
    solution01()
    solution02()
    

