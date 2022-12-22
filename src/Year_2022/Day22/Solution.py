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
    data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    board = data[0]
    instructions = data[1][0]

    height = len(board)
    width = 0

    for i in range(height):
        board[i]=list(board[i])
        width = max(width,len(board[i]))

    for i in range(height):
        board[i]=board[i]+[' ']*(width-len(board[i]))

    instructions = instructions.replace('R',' R ')
    instructions = instructions.replace('L',' L ')
    instructions = instructions.split(' ')

    command_list = []

    for item in instructions:
        if item!='':
            command_list.append(item)

    return board, command_list

direction_dict = {0:np.array([0,1]),1:np.array([1,0]),2:np.array([0,-1]),3:np.array([-1,0])}
diagonal_dict = {0:np.array([1,1]),1:np.array([1,-1]),2:np.array([-1,-1]),3:np.array([-1,1])}
rotation_dict = {'L':-1,'R':1}
direction_character_dict = {0:'>',1:'v',2:'<',3:'^'}


def on_exterior(coords,board):
    return coords[0]<0 or coords[1]<0 or coords[0]>=len(board) or coords[1]>=len(board[0]) or board[coords[0]][coords[1]]==' '

def on_interior(coords,board):
    return not on_exterior(coords,board)

def execute_step(coords,direction,board,adjacency_dict):
    next_coords = coords+direction_dict[direction]
    next_direction = direction

    if on_exterior(next_coords,board):
        key_in = (tuple(coords.tolist()),direction)

        next_coords = np.array(list(adjacency_dict[key_in][0]))
        next_direction = adjacency_dict[key_in][1]

    if board[next_coords[0]][next_coords[1]]=='#':
        return coords, direction

    else:
        return next_coords, next_direction

def execute_command(coords,direction,command,board,boundary_dict):

    board[coords[0]][coords[1]]=direction_character_dict[direction]

    if command=='L' or command=='R':
        direction+=rotation_dict[command]
        direction%=4
    else:
        num_steps = int(command)

        for i in range(num_steps):
            board[coords[0]][coords[1]]=direction_character_dict[direction]
            coords, direction = execute_step(coords,direction,board,boundary_dict)

    return coords,direction


def perimeter_step(coords,direction,board):
    next_coords = coords+direction_dict[direction]

    if on_exterior(next_coords,board):
        directionL = (direction-1)%4
        next_coordsL = coords+direction_dict[directionL]

        directionR = (direction+1)%4
        next_coordsR = coords+direction_dict[directionR]

        if on_interior(next_coordsL,board):
            return coords, directionL

        if on_interior(next_coordsR,board):
            return coords, directionR

    return next_coords, direction

def check_if_inner_corner(coords,board):
    if on_exterior(coords,board):
        return False, None

    diag_list = []

    for i in range(4):
        if on_exterior(coords+diagonal_dict[i],board):
            diag_list.append(i)

    dir_list = []
    for i in range(4):
        if on_exterior(coords+direction_dict[i],board):
            dir_list.append(i)

    if len(diag_list)!=1 or len(dir_list)!=0:
        return False, None

    d0 = diag_list[0]
    d1 = (diag_list[0]+1)%4

    return True, [d0,d1]

def zip_up_edges_from_corner(coords,direction_pair,board,dict_in):
    direction0 = direction_pair[0]
    direction1 = direction_pair[1]

    direction0_prev = direction0
    direction1_prev = direction1

    coords0 = coords+direction_dict[direction0]
    coords1 = coords+direction_dict[direction1]

    while direction0 == direction0_prev or direction1_prev == direction1:
        direction0_prev = direction0
        direction1_prev = direction1

        normal_direction_outer0 = (direction0+1)%4
        if on_interior(coords0+direction_dict[normal_direction_outer0],board):
            normal_direction_outer0 = (direction0-1)%4

        normal_direction_outer1 = (direction1+1)%4
        if on_interior(coords1+direction_dict[normal_direction_outer1],board):
            normal_direction_outer1 = (direction1-1)%4

        normal_direction_inner0 = (normal_direction_outer0+2)%4
        normal_direction_inner1 = (normal_direction_outer1+2)%4


        dict_in[(tuple(coords0.tolist()),normal_direction_outer0)]=(tuple(coords1.tolist()),normal_direction_inner1)
        dict_in[(tuple(coords1.tolist()),normal_direction_outer1)]=(tuple(coords0.tolist()),normal_direction_inner0)

        coords0, direction0 = perimeter_step(coords0,direction0,board)
        coords1, direction1 = perimeter_step(coords1,direction1,board)


def generate_off_grid_adjacency_cube(board):
    dict_out = {}

    for i in range(len(board)):
        for j in range(len(board[0])):
            coords = np.array([i,j])
            corner_bool, direction_pair = check_if_inner_corner(coords,board)

            if corner_bool:
                zip_up_edges_from_corner(coords,direction_pair,board,dict_out)

    return dict_out


def generate_off_grid_adjacency_wrap(board):
    dict_out = {}

    for i in range(len(board)):
        left = 0
        while board[i][left]==' ':
            left+=1


        right = len(board[0])-1
        while board[i][right]==' ':
            right-=1

        dict_out[((i,left),2)]=((i,right),2)
        dict_out[((i,right),0)]=((i,left),0)

    for i in range(len(board[0])):
        top = 0
        while board[top][i]==' ':
            top+=1

        bottom = len(board)-1
        while board[bottom][i]==' ':
            bottom-=1

        dict_out[((top,i),3)]=((bottom,i),3)
        dict_out[((bottom,i),1)]=((top,i),1)

    return dict_out


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    board, command_list = parse_input01(fname)

    adjacency_dict = generate_off_grid_adjacency_wrap(board)

    coords = np.array([0,0])
    while board[coords[0]][coords[1]]==' ':
        coords[1]+=1
    
    direction = 0

    for command in command_list:
        coords,direction = execute_command(coords,direction,command,board,adjacency_dict)

    code = 1000*(coords[0]+1)+4*(coords[1]+1)+direction
    print(code)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    board, command_list = parse_input01(fname)

    adjacency_dict = generate_off_grid_adjacency_cube(board)

    coords = np.array([0,0])
    while board[coords[0]][coords[1]]==' ':
        coords[1]+=1

    direction = 0

    for command in command_list:
        coords,direction = execute_command(coords,direction,command,board,adjacency_dict)

    code = 1000*(coords[0]+1)+4*(coords[1]+1)+direction
    print(code)



if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

