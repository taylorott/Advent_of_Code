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

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[',','=','<','>','x','y','z',' '],allFloat=True)

    return np.array(data)

def update_system(positions,velocities):
    for i in range(len(positions)):
        for j in range(len(positions)):
            if i!=j:
                for k in range(3):
                    if positions[i][k]>positions[j][k]:
                        velocities[i][k]-=1
                    elif positions[i][k]<positions[j][k]:
                        velocities[i][k]+=1
    positions+=velocities

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    positions = parse_input01(fname)
    num_moons = len(positions)

    velocities = np.zeros([num_moons,3])

    for i in range(1000):
        update_system(positions,velocities)
    
    E = 0

    for i in range(num_moons):
        E+=int(sum(np.abs(positions[i]))*sum(np.abs(velocities[i])))

    print(E)

def convert_state(positions,velocities):
    list_out = []

    for position in positions:
        for coord in position:
            list_out.append(int(coord))

    for velocity in velocities:
        for coord in velocity:
            list_out.append(int(coord))

    return convert(list_out)

def convert(list):
    return tuple(i for i in list)

def find_period_coord(positions,velocities,i):
    positions = np.array(positions)
    velocities = np.array(velocities)

    num_moons = len(positions)

    for j in range(3):
        if j!=i:
            for k in range(num_moons):
                positions[k][j]=0
                velocities[k][j]=0

    state_dict = {}
    count = 0
    while True:
        key = convert_state(positions,velocities)
        if key in state_dict:
            break
        else:
            state_dict[key]=None

        update_system(positions,velocities)
        count+=1

    return count


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    positions = parse_input01(fname)
    num_moons = len(positions)

    velocities = np.zeros([num_moons,3])


    q0 = find_period_coord(positions,velocities,0)
    q1 = find_period_coord(positions,velocities,1)
    q2 = find_period_coord(positions,velocities,2)


    v = lcm(lcm(q0,q1),q2)
    print(v)

if __name__ == '__main__':
    solution01()
    solution02()
    

