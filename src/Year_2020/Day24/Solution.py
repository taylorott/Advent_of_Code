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
    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    parsed_data = []
    for line in data:
        temp = line.replace('e','e ')
        temp = temp.replace('w','w ')
        temp = temp.replace('n',' n')
        temp = temp.replace('s',' s')
        commands = temp.split(' ')

        command_list = []

        for command in commands:
            if command!='':
                command_list.append(command)

        parsed_data.append(command_list)

    return parsed_data

def solution01():
    #Use coordinates for vertices of grid of equilateral triangles
    #which is same as hexagon centers
    #one coordinate for horizontal (E) and other for diagonal (NE)
    #the rest is linear algebra using this different choice of basis vectors
    #E x NE coordinates guide:
    #E = [1,0]
    #W = [-1,0]
    #NE = [0,1]
    #SW = [0,-1]
    #NW = [-1,1]
    #SE = [1,-1]

    dir_dict = {'e' : np.array([ 1, 0]),
                'w' : np.array([-1, 0]),
                'ne': np.array([ 0, 1]),
                'sw': np.array([ 0,-1]),
                'nw': np.array([-1, 1]),
                'se': np.array([ 1,-1])}
    flip_dict = {}

    np.array([])

    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)


    for line in data:
        coords = np.array([0,0])
        for move in line:
            coords+=dir_dict[move]
        flip_coords = (int(coords[0]),int(coords[1]))

        if flip_coords in flip_dict:
            flip_dict[flip_coords]=1-flip_dict[flip_coords]
        else:
            flip_dict[flip_coords]=1

    total = 0

    for key in flip_dict:
        total+=flip_dict[key]

    print(total)

dir_list = [np.array([ 1, 0]),np.array([-1, 0]),np.array([ 1,-1]),np.array([-1, 1]),np.array([ 0, 1]),np.array([ 0,-1])]

def array_to_tuple(coords):
    return (int(coords[0]),int(coords[1]))

def tuple_to_array(coords):
    return np.array([coords[0],coords[1]])

def enumerate_neighbors(coords):
    neighbor_list = []
    for direction in dir_list:
        neighbor_list.append(array_to_tuple(coords+direction))
    return neighbor_list

def count_adjacent(coords,flip_dict):
    neighbor_list = enumerate_neighbors(coords)

    total = 0

    for neighbor in neighbor_list:
        if neighbor in flip_dict and flip_dict[neighbor]==1:
            total+=1

    return total

def update_flip_dict(flip_dict):
    new_flip_dict = {}

    for key in flip_dict.keys():
        coords = tuple_to_array(key)

        num_on = count_adjacent(coords,flip_dict)

        if flip_dict[key]==1:
            if not(num_on>2 or num_on==0):
                new_flip_dict[key]=1
        if flip_dict[key]==0 and num_on==2:
            new_flip_dict[key]=1

        neighbor_list = enumerate_neighbors(coords)

        for neighbor in neighbor_list:
            neighbor_coords = tuple_to_array(neighbor)
            num_on = count_adjacent(neighbor_coords,flip_dict)

            if neighbor not in flip_dict or flip_dict[neighbor]==0:
                if num_on==2:
                    new_flip_dict[neighbor]=1
            else:
                if not(num_on>2 or num_on==0):
                    new_flip_dict[neighbor]=1

    return new_flip_dict


def solution02():
    #Use coordinates for vertices of grid of equilateral triangles
    #which is same as hexagon centers
    #one coordinate for horizontal (E) and other for diagonal (NE)
    #the rest is linear algebra using this different choice of basis vectors
    #E x NE coordinates guide:
    #E = [1,0]
    #W = [-1,0]
    #NE = [0,1]
    #SW = [0,-1]
    #NW = [-1,1]
    #SE = [1,-1]

    dir_dict = {'e' : np.array([ 1, 0]),
                'w' : np.array([-1, 0]),
                'ne': np.array([ 0, 1]),
                'sw': np.array([ 0,-1]),
                'nw': np.array([-1, 1]),
                'se': np.array([ 1,-1])}
    flip_dict = {}

    np.array([])

    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)


    for line in data:
        coords = np.array([0,0])
        for move in line:
            coords+=dir_dict[move]
        flip_coords = (int(coords[0]),int(coords[1]))

        if flip_coords in flip_dict:
            flip_dict[flip_coords]=1-flip_dict[flip_coords]
        else:
            flip_dict[flip_coords]=1


    for count in range(100):
        flip_dict = update_flip_dict(flip_dict)


    total = 0

    for key in flip_dict:
        total+=flip_dict[key]

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

