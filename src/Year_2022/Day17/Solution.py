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
    data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data[0]

direction_dict = {'>':np.array([1,0]),'<':np.array([-1,0]),'d':np.array([0,-1]),'u':np.array([0,1])}

class TetrisSim(object):
    def __init__(self,width,offset_vector = None):
        self.width = width
        self.occupied_dict = {}
        self.max_rock_height = -1
        self.floor_height = 0
        self.floor_str = '+'+'-'*self.width+'+'
        self.define_shapes()

        self.current_shape = None
        self.current_coords = None
        self.current_shape_boundary = None
        self.current_shape_occupied_dict = None
        self.current_shape_id = None

        self.max_height_list = np.array([-1]*self.width)

        if offset_vector is None:
            self.offset_vector = np.array([2,3])
        else:
            self.offset_vector = np.array(offset_vector)

    def define_shapes(self):
        shape_list = []
        shape_list.append([np.array([0,0]),np.array([1,0]),np.array([2,0]),np.array([3,0])])
        shape_list.append([np.array([0,0]),np.array([1,0]),np.array([-1,0]),np.array([0,1]),np.array([0,-1])])
        shape_list.append([np.array([0,0]),np.array([1,0]),np.array([2,0]),np.array([2,1]),np.array([2,2])])
        shape_list.append([np.array([0,0]),np.array([0,1]),np.array([0,2]),np.array([0,3])])
        shape_list.append([np.array([0,0]),np.array([1,0]),np.array([1,1]),np.array([0,1])])

        boundary_list = []
        for shape in shape_list:
            boundary_list.append(self.compute_bottom_left_boundary(shape))

        self.shape_list = shape_list
        self.boundary_list = boundary_list


    def insert_new_shape(self,shape_id):
        self.current_shape_id = shape_id
        self.current_shape = self.shape_list[shape_id]
        self.current_shape_boundary = self.boundary_list[shape_id]
        self.current_coords = self.offset_vector + np.array([0,max(0,self.max_rock_height)])-self.current_shape_boundary

    def add_current_shape_to_grid(self):
        for shape_coords in self.current_shape:
            grid_coords = shape_coords+self.current_coords

            self.occupied_dict[(grid_coords[0],grid_coords[1])]=True

    def erase_current_shape_from_grid(self):
        for shape_coords in self.current_shape:
            grid_coords = shape_coords+self.current_coords

            self.occupied_dict[(grid_coords[0],grid_coords[1])]=False


    def update_max_height_list(self):
        for shape_coords in self.current_shape:
            grid_coords = shape_coords+self.current_coords
            self.max_height_list[grid_coords[0]]=max(self.max_height_list[grid_coords[0]],grid_coords[1])

    def compute_current_shape_occupied_dict(self):
        self.current_shape_occupied_dict = {}

        if self.current_shape is not None:
            for shape_coords in self.current_shape:
                grid_coords = shape_coords+self.current_coords
                grid_tuple = (grid_coords[0],grid_coords[1])
                self.current_shape_occupied_dict[grid_tuple]=True

    def compute_max_height_shape(self):
        max_height = -1

        for shape_coords in self.current_shape:
            grid_coords = shape_coords+self.current_coords 
            max_height = max(max_height,grid_coords[1])

        return max_height+1

    def can_move_in_direction(self,dir_key):
        direction = direction_dict[dir_key]

        can_move = True

        for shape_coords in self.current_shape:
            grid_coords = shape_coords+self.current_coords+direction
            grid_tuple = (grid_coords[0],grid_coords[1])

            condition1 = grid_tuple not in self.occupied_dict or not self.occupied_dict[grid_tuple]
            condition2 = grid_coords[1]>=0 and grid_coords[0]>=0 and grid_coords[0]<self.width


            can_move = can_move and condition1 and condition2

        return can_move

    def move_shape(self,dir_key):
        can_move = self.can_move_in_direction(dir_key)

        direction = direction_dict[dir_key]

        if can_move:
            self.current_coords+=direction

        return can_move

    def evaluate_time_step(self,command_in,print_at_new_shape=False):
        touched_down = False

        self.move_shape(command_in)
        can_move_down = self.move_shape('d')

        if not can_move_down:
            touched_down = True
            self.update_max_height_list()
            self.add_current_shape_to_grid()
            self.max_rock_height = max(self.max_rock_height,self.compute_max_height_shape())
            # print(self.max_rock_height)
            self.insert_new_shape((self.current_shape_id+1)%len(self.shape_list))

            if print_at_new_shape:
                self.print_system_state()

        return touched_down, self.max_rock_height

    def compute_bottom_left_boundary(self,list_in):
        bottom_boundary = np.inf
        left_boundary = np.inf

        for item in list_in:
            left_boundary = min(left_boundary,item[0])
            bottom_boundary = min(bottom_boundary,item[1])

        return np.array([left_boundary,bottom_boundary])

    def print_motion_tests(self):
        if self.current_shape is not None:
            print('can move right: ', self.can_move_in_direction('>'))
            print('can move left: ', self.can_move_in_direction('<'))
            print('can move down: ', self.can_move_in_direction('d'))
            print()

    def print_system_state(self):
        height = max(self.max_rock_height,self.compute_max_height_shape())

        self.compute_current_shape_occupied_dict()        

        for j in range(height-1,-1,-1):
            str_out = '|'
            for i in range(self.width):
                if (i,j) in self.occupied_dict and self.occupied_dict[(i,j)]:
                    str_out+='#'
                elif self.current_shape_occupied_dict is not None and (i,j) in self.current_shape_occupied_dict and self.current_shape_occupied_dict[(i,j)]:
                    str_out+='@'
                else:
                    str_out+='.'
            str_out+='|'

            print(str_out)

        print(self.floor_str)
        print()
      
def test01():
    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    coord_list = [np.array([0,0]),np.array([1,0]),np.array([2,-3]),np.array([-3,0])]

    for delta_position in coord_list:
        mySim.current_coords+=delta_position
        mySim.print_system_state()
        mySim.print_motion_tests()

def test02():
    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    move_sequence = ['d','d','d','d','>','>','<','<','<','<']

    mySim.print_system_state()
    mySim.print_motion_tests()
    for move in move_sequence:
        mySim.move_shape(move)
        print('command: '+move+'\n')
        mySim.print_system_state()
        mySim.print_motion_tests()

def test03():
    data = parse_input01('Input01.txt')

    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    mySim.print_system_state()
    for i in range(8):
        my_command = data[i]
        # print(my_command+'\n')
        mySim.evaluate_time_step(my_command)
        mySim.print_system_state()

def test04():
    data = parse_input01('Input01.txt')

    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    mySim.print_system_state()
    print(mySim.max_height_list)
    print()

    for my_command in data:
        touched_down, prev_rock_height = mySim.evaluate_time_step(my_command,True)

        if touched_down:
            print(mySim.max_height_list)
            print()


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    num_shapes = 2022

    count = 0
    num_touched_down = 0
    while True:
        my_command = data[count]
        touched_down, prev_rock_height = mySim.evaluate_time_step(my_command)

        if touched_down:
            num_touched_down+=1

        if num_touched_down == num_shapes:
            print(prev_rock_height)
            break

        count+=1
        count%=len(data)
    
def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    mySim = TetrisSim(7)
    mySim.insert_new_shape(0)

    num_shapes = 1000000000000

    count = 0
    num_touched_down = 0

    score_list = [None]
    state_dict = {}

    while True:
        my_command = data[count]
        touched_down, rock_height_out = mySim.evaluate_time_step(my_command)

        if touched_down:
            num_touched_down+=1

            height_array_out = np.array(mySim.max_height_list)
            height_array_out = height_array_out-min(height_array_out)
            height_tuple = tuple(height_array_out.tolist())

            key = (count,mySim.current_shape_id,height_tuple)
            val = [num_touched_down,rock_height_out] 

            score_list.append(rock_height_out)

            if key in state_dict:
                prev_state = state_dict[key]
                current_state = val

                period = current_state[0]-prev_state[0]
                delta_height = current_state[1]-prev_state[1]

                num_cycles = (num_shapes-current_state[0])//period
                iterations_to_go = num_shapes-(num_cycles*period+current_state[0])
                score_out = (score_list[prev_state[0]+iterations_to_go]-score_list[prev_state[0]])+ num_cycles*delta_height+current_state[1]

                print(score_out)
                break
            else:
                state_dict[key]=val

        count+=1
        count%=len(data)
    

if __name__ == '__main__':
    t0 = time.time()

    # test01()
    # test02()
    # test03()
    # test04()
    
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

