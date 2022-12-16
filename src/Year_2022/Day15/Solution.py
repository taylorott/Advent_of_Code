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
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [':',',','='],type_lookup = None, allInt = False, allFloat = False)

    list_out = []
    for line in data:
        x_sensor = int(line[1])
        y_sensor = int(line[3])
        x_beacon = int(line[5])
        y_beacon = int(line[7])
        list_out.append([x_sensor,y_sensor,x_beacon,y_beacon])
    return list_out

def manhattan_distance(x_sensor,y_sensor,x_beacon,y_beacon):
    return abs(x_sensor-x_beacon)+abs(y_sensor-y_beacon)


def compute_overlapping_segments(segment_list_in):
    segment_dict = {}

    left_bound_list = []
    for segment in segment_list_in:
        if segment[0] in segment_dict:
            segment_dict[segment[0]]=max(segment_dict[segment[0]],segment[1])
        else:
            segment_dict[segment[0]]=segment[1]
            left_bound_list.append(segment[0])
    left_bound_list.sort()
    right_bound_list = []

    for left_bound in left_bound_list:
        right_bound_list.append(segment_dict[left_bound])

    segment_list_out = []
    
    min_val = None
    max_val = None

    for i in range(len(left_bound_list)):

        min_val_current = left_bound_list[i]
        max_val_current = right_bound_list[i]

        if min_val is None:
            min_val=min_val_current
            max_val=max_val_current

        elif max_val<min_val_current:
            segment_list_out.append([min_val,max_val])
            
            min_val=min_val_current
            max_val=max_val_current

        else:
            max_val= max(max_val,max_val_current)

    segment_list_out.append([min_val,max_val])
    return segment_list_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
   
    dist_list = []

    beacon_dict = {}
    item_list = []

    #compute the corresponding manhattan distance for each sensor/beacon pair and then store it
    for item in data:
        x_sensor = item[0]
        y_sensor = item[1]
        x_beacon = item[2]
        y_beacon = item[3]
        beacon_dict[(x_beacon,y_beacon)]=None

        item_list.append([x_sensor,y_sensor])
        dist_list.append(manhattan_distance(x_sensor,y_sensor,x_beacon,y_beacon))


    segment_list = []

    y = 2000000

    #for each sensor...
    for i in range(len(item_list)):
        x_sensor = item_list[i][0]
        y_sensor = item_list[i][1]

        #if the exclusion area of the sensor intersects the row
        if abs(y-y_sensor)<=dist_list[i]:
            #compute line segment corresponding to exclusion area and row=y
            x_min = x_sensor-(dist_list[i]-abs(y-y_sensor))
            x_max = x_sensor+(dist_list[i]-abs(y-y_sensor))

            #add line segment to list
            segment_list.append([x_min,x_max])

    #compute union of all line segments
    segment_list = compute_overlapping_segments(segment_list)

    total = 0

    #total length of overlapping segments
    for segment in segment_list:
        total += segment[1]-segment[0]+1

    #subtract spaces in that row occupied by beacons
    for beacon in beacon_dict:
        if beacon[1]==y:
            total-=1

    print(total)


def transform_constraints(x_sensor,y_sensor,dist_in):
    left_corner = [x_sensor-dist_in,y_sensor]
    right_corner = [x_sensor+dist_in,y_sensor]

    top_left_line_x_intercept = x_sensor-dist_in-y_sensor
    bottom_right_line_x_intercept = x_sensor+dist_in-y_sensor
    
    bottom_left_line_x_intercept = x_sensor-dist_in+y_sensor
    top_right_line_x_intercept = x_sensor+dist_in+y_sensor

    return [top_left_line_x_intercept,
            bottom_right_line_x_intercept,
            bottom_left_line_x_intercept,
            top_right_line_x_intercept]

# def find_location():
def test_point(x,y,item_list,dist_list):
    test_val = True
    for i in range(len(item_list)):
        item=item_list[i]
        test_val = test_val and abs(x-item[0])+abs(y-item[1])>dist_list[i]

    return test_val

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    x_max = 4000000
    y_max = 4000000

    data = parse_input01(fname)
    
    dist_list = []

    beacon_dict = {}
    sensor_dict = {}
    constraints_list = []
    item_list = []
    for item in data:
        dist_list.append(manhattan_distance(item[0],item[1],item[2],item[3]))
        beacon_dict[(item[2],item[3])]=None
        sensor_dict[(item[0],item[1])]=None
        constraints_list.append(transform_constraints(item[0],item[1],dist_list[-1]))

        item_list.append([item[0],item[1]])
        item_list.append([item[2],item[3]])
        dist_list.append(0)

    x_intercept_left_diagonal_list = []
    x_intercept_right_diagonal_list = []

    for constraint in constraints_list:
        x_intercept_right_diagonal_list.append(constraint[0]-1)
        x_intercept_right_diagonal_list.append(constraint[1]+1)
        x_intercept_left_diagonal_list.append(constraint[2]-1)
        x_intercept_left_diagonal_list.append(constraint[3]+1)


    x_intercept_left_diagonal_list.sort()
    x_intercept_right_diagonal_list.sort()

    temp_list = x_intercept_left_diagonal_list
    x_intercept_left_diagonal_list = []
    for item in temp_list:
        if len(x_intercept_left_diagonal_list)==0 or item!=x_intercept_left_diagonal_list[-1]:
            x_intercept_left_diagonal_list.append(item)


    temp_list = x_intercept_right_diagonal_list
    x_intercept_right_diagonal_list = []
    for item in temp_list:
        if len(x_intercept_right_diagonal_list)==0 or item!=x_intercept_right_diagonal_list[-1]:
            x_intercept_right_diagonal_list.append(item)

    for i in range(len(x_intercept_left_diagonal_list)):
        for j in range(len(x_intercept_right_diagonal_list)):
            xl_test = x_intercept_left_diagonal_list[i]
            xr_test = x_intercept_right_diagonal_list[j]

            x = (xl_test+xr_test)/2.0
            y = x-xr_test
            if 0<=x and x<=x_max and 0<=y and y<=y_max and x==round(x) and y==round(y):
                x = round(x)
                y = round(y)
                if test_point(x,y,item_list,dist_list):
                    print(4000000*x+y)
                    break

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

