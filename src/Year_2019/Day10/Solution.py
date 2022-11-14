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

    return data

def count_asteroids_LOS(data,x,y):
    LOS_dict = {}
    num_asteroids = 0
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='#' and (i!=x or j!=y):
                dx = i-x
                dy = j-y

                q = gcd(abs(dx),abs(dy))
                my_key = (int(dx/q),int(dy/q))
                my_val = [dx,dy]
                if my_key not in LOS_dict:
                    LOS_dict[my_key]=[]
                    num_asteroids+=1
                LOS_dict[my_key].append(my_val)
    return num_asteroids, LOS_dict


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    max_val = 0
    x = None
    y = None
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='#':
                temp_val, dummy = count_asteroids_LOS(data,i,j)
                if temp_val>max_val:
                    max_val = temp_val
                    x = i
                    y = j
    print(max_val)


def sort_by_magnitude(list_in):
    list_out = []

    mag_list = []
    mag_dict = {}

    for i in range(len(list_in)):
        mag_val = abs(list_in[i][0])
        mag_dict[mag_val]=list(list_in[i])
        mag_list.append(mag_val)

    mag_list.sort(reverse=True)

    for mag_val in mag_list:
        list_out.append(mag_dict[mag_val])

    return list_out

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    LOS_dict = None
    max_val = 0
    x = None
    y = None
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='#':
                temp_val, temp_dict = count_asteroids_LOS(data,i,j)
                if temp_val>max_val:
                    max_val = temp_val
                    x = i
                    y = j
                    LOS_dict = temp_dict


    theta_dict = {}
    theta_list = []
    for key in LOS_dict.keys():
        theta = np.arctan2(key[1],-key[0])
        while theta<0:
            theta+=2*np.pi
        theta_dict[theta] = key
        theta_list.append(theta)
        LOS_dict[key] = sort_by_magnitude(LOS_dict[key])

    theta_list.sort()



    asteroid_count = 0

    counts_dict = {1:None,2:None,3:None,10:None,20:None,50:None,100:None,199:None,200:None,201:None,299:None}

    # print(y,x)
    while asteroid_count<max_val:
        for i in range(len(theta_list)):
            theta = theta_list[i]
            key = theta_dict[theta]

            if len(LOS_dict[key])>0:
                dP = LOS_dict[key].pop(-1)
                asteroid_count+=1

                x_out = x+dP[0]
                y_out = y+dP[1]

                if asteroid_count == 200:
                    print(y_out*100+x_out)
                    return None
                # if asteroid_count in counts_dict:
                    # print(asteroid_count,y_out,x_out)

  

if __name__ == '__main__':
    solution01()
    solution02()
    

