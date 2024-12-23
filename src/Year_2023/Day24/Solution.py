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
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    return bh.parse_extract_ints(path,fname)

def find_intersection_2D(stone0,stone1):
    px0 = stone0[0]
    py0 = stone0[1]

    vx0 = stone0[3]
    vy0 = stone0[4]

    px1 = stone1[0]
    py1 = stone1[1]

    vx1 = stone1[3]
    vy1 = stone1[4]

    A = np.array([[-vy0,vx0],[-vy1,vx1]])
    B = np.array([px0*-vy0+py0*vx0,px1*-vy1+py1*vx1])

    det = (-vy0*vx1)-(vx0*-vy1)

    if det!=0:
        pos = np.linalg.solve(A,B)
        test_future0 = np.dot(pos-np.array([px0,py0]),np.array([vx0,vy0]))>=0
        test_future1 = np.dot(pos-np.array([px1,py1]),np.array([vx1,vy1]))>=0

        if test_future0 and test_future1:
            return pos
        else:
            return None
    else:
        same_line_test = B[0]*A[1]-B[1]*A[0]
        if same_line_test[0]==0 and same_line_test[1]==0:
            print('uh oh!')

        return None

def inside_min_max_2D(pos,min_val,max_val):
    x_test = min_val<=pos[0] and pos[0]<=max_val
    y_test = min_val<=pos[1] and pos[1]<=max_val
    return x_test and y_test

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    total = 0

    # min_val = 7
    # max_val = 27

    min_val = 200000000000000
    max_val = 400000000000000

    for i in range(len(data)):
        for j in range(i+1,len(data)):
            pos = find_intersection_2D(data[i],data[j])
            if pos is not None and inside_min_max_2D(pos,min_val,max_val):
                total+=1

    if show_result: print(total)

    return total

def compute_error(data, pos,vel,t_list):
    pos = np.array(pos)
    vel = np.array(vel)
    t_list = np.array(t_list)

    X = np.hstack([pos,vel,t_list])
    Y = np.array([])
    Jacobian = np.zeros((3*len(data),len(data)+6))
    

    for i in range(len(data)):
        item = data[i]
        p_i = np.array(item[:3])
        v_i = np.array(item[3:6])
        t_i = t_list[i]

        v_error = (vel-v_i)*t_i+pos-p_i
        Y=np.hstack([Y,v_error])

        for j in range(3):
            Jacobian[3*i+j][i]=vel[j]-v_i[j]
            Jacobian[3*i+j][len(data)+j]=1
            Jacobian[3*i+j][len(data)+3+j]=t_i

    return Y,Jacobian

def solution02a(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    t_list = np.array([0]*len(data))
    for i in range(len(data)):
        t_list[i] = 10*i

    pos = np.array([0.0,0.0,0.0])
    vel = np.array([0.0,0.0,0.0])
    for item in data:
        pos+=np.array(item[:3])
        vel+=np.array(item[3:])

    pos/=float(len(data))
    vel/=float(len(data))

    Y = None
    while Y is None or max(Y)>.25 or min(Y)<-.25:
        Y,Jacobian = compute_error(data, pos,vel,t_list)
     
        X = np.hstack([t_list,pos,vel])
        Delta_X = -np.linalg.solve(np.dot(Jacobian.T,Jacobian), np.dot(Jacobian.T,Y))
      
        X_new = X+Delta_X

        t_list = np.array(X_new[:len(data)])

        pos = np.array(X_new[len(data):3+len(data)])
        vel = np.array(X_new[len(data)+3:])

    result = round(pos[0]+pos[1]+pos[2])

    if show_result: print(result)

    return result

def solution02b(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)

    M = np.zeros((0,6))
    Y = np.array([])
    for i in range(len(data)-1):
        item0 = data[i]
        item1 = data[i+1]

        p0 = np.array(item0[:3])
        v0 = np.array(item0[3:])

        p1 = np.array(item1[:3])
        v1 = np.array(item1[3:])

        y = np.cross(p1,v1)-np.cross(p0,v0)
        a = v0-v1
        b = p1-p0

        A = np.array([[    0,-a[2], a[1]],
                      [ a[2],    0,-a[0]],
                      [-a[1], a[0],    0]])

        B = np.array([[    0,-b[2], b[1]],
                      [ b[2],    0,-b[0]],
                      [-b[1], b[0],    0]])        

        sub_mat = np.hstack([A,B])
        M = np.vstack([M,sub_mat])
        Y = np.hstack([Y,y])

    result = np.linalg.solve(np.dot(M.T,M),np.dot(M.T,Y))

    pos_sum = round(np.sum(result[:3]))

    if show_result: print(pos_sum)

    return pos_sum

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02a()
    solution02b()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

