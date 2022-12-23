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
    data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    # data = bh.parse_strings(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

    return data

direction_dict = {'E':np.array([0,1]),'S':np.array([1,0]),'W':np.array([0,-1]),'N':np.array([-1,0]),
                       'SE':np.array([1,1]),'SW':np.array([1,-1]),'NW':np.array([-1,-1]),'NE':np.array([-1,1])}

def get_grid_bounds(current_state):
    has_initialized = False
    i_min = None
    i_max = None
    j_min = None
    j_max = None

    for key in current_state.keys():
        if not has_initialized:
            has_initialized = True
            i_min = key[0]
            i_max = key[0]
            j_min = key[1]
            j_max = key[1]

        i_min = min(i_min,key[0])
        i_max = max(i_max,key[0])
        j_min = min(j_min,key[1])
        j_max = max(j_max,key[1])

    return i_min,i_max,j_min,j_max

def compute_score(current_state):
    i_min,i_max,j_min,j_max = get_grid_bounds(current_state)
    area = (i_max+1-i_min)*(j_max+1-j_min)

    for key in current_state.keys():
        area-=1

    print(area)

def print_state(current_state):
    i_min,i_max,j_min,j_max = get_grid_bounds(current_state)

    i_min-=1
    j_min-=1
    i_max+=1
    j_max+=1

    l0 = (i_max-i_min)+1
    l1 = (j_max-j_min)+1

    char_mat = []

    for i in range(l0):
        char_mat.append(['.']*l1)

    for key in current_state.keys():
        char_mat[key[0]-i_min][key[1]-j_min]='#'

    print()
    bh.print_char_matrix(char_mat)
    print()

def check_neighbors(key,current_state):
    coords = np.array(list(key))

    neighbors = {}
    has_neighbors = False

    for direction in direction_dict:
        neighbor_coords = coords + direction_dict[direction]
        neighbor_key = tuple(neighbor_coords.tolist())

        if neighbor_key in current_state and current_state[neighbor_key]==1:
            neighbors[direction]=True
            has_neighbors = True
        else:
            neighbors[direction]=False

    return has_neighbors,neighbors

def propose_move(key,current_state,ordering,proposal_dict,new_location_tally):
    coords = np.array(list(key))
    has_neighbors,neighbors = check_neighbors(key,current_state)

    if not has_neighbors:
        proposal_dict[key]=None
        return None

    for v in ordering:
        test = False
        v_out = None
        if v == 0:
            test = not (neighbors['N'] or neighbors['NE'] or neighbors['NW'])
            v_out = 'N'
        elif v == 1:
            test = not (neighbors['S'] or neighbors['SE'] or neighbors['SW'])
            v_out = 'S'
        elif v == 2:
            test = not (neighbors['W'] or neighbors['NW'] or neighbors['SW'])
            v_out = 'W'
        elif v == 3:
            test = not (neighbors['E'] or neighbors['NE'] or neighbors['SE'])
            v_out = 'E'

        if test:
            proposal_coords = coords+direction_dict[v_out]
            proposal_key = tuple(proposal_coords.tolist())
            proposal_dict[key] = proposal_key

            if proposal_key in new_location_tally:
                new_location_tally[proposal_key]+=1
            else:
                new_location_tally[proposal_key]=1

            return None

    proposal_dict[key]=None
    return None

def execute_step(current_state,ordering):
    proposal_dict = {}
    new_location_tally = {}

    for key in current_state:
        propose_move(key,current_state,ordering,proposal_dict,new_location_tally)

    next_state = {}

    for key in current_state:
        if proposal_dict[key] is None:
            next_state[key]=1
        elif new_location_tally[proposal_dict[key]]==1:
            next_state[proposal_dict[key]]=1
        else:
            next_state[key]=1

    ordering.append(ordering.popleft())

    return next_state

def check_termination_condition(current_state):
    can_terminate = True

    for key in current_state.keys():
        has_neighbors,neighbors = check_neighbors(key,current_state)
        can_terminate = can_terminate and not has_neighbors

    return can_terminate

def grid_to_state(grid_in):

    current_state = {}

    for i in range(len(grid_in)):
        for j in range(len(grid_in[0])):
            if grid_in[i][j]=='#':
                current_state[(i,j)]=1

    return current_state

def run_simulation01(current_state,display=False):
    count = 0

    if display:
        print('Round: '+str(count))
        print_state(current_state)

    ordering = deque()
    for i in range(4):
        ordering.append(i)

    for i in range(10):
        current_state = execute_step(current_state,ordering)
        count+=1

        if display:
            print('Round: '+str(count))
            print_state(current_state)
        
    return current_state,count

def run_simulation02(current_state,display=False):
    count = 0

    if display:
        print('Round: '+str(count))
        print_state(current_state)

    ordering = deque()
    for i in range(4):
        ordering.append(i)

    while not check_termination_condition(current_state):
        current_state = execute_step(current_state,ordering)
        count+=1

        if display:
            print('Round: '+str(count))
            print_state(current_state)
        
    return current_state,count

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    current_state = grid_to_state(data)
    current_state, num_iterations = run_simulation01(current_state,False)
    compute_score(current_state)
    
    
def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)

    current_state = grid_to_state(data)
    current_state, num_iterations = run_simulation02(current_state,False)
    
    print(num_iterations+1)
    


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

