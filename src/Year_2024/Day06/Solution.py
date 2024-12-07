#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

#current direction to next direction for right turn
r_turn_dict = {'^':'>','>':'v','v':'<','<':'^'} 

#maps current direction to coordinate change on char grid
move_dict = {'^':(-1,0),'>':(0,1),'v':(1,0),'<':(0,-1)}

#parses the input file
#OUTPUTS
#guard_coord are the (i,j) coords of the guard (tuple)
#obs_set is a set of the (i,j) coords of all obstacles in input
#grid_dim are the dimensions of the character grid (height,width)
def parse_input01(fname):
    data = bh.parse_char_grid(path,fname)

    guard_coord = None
    obs_set = set()
    for i in range(len(data)):
        for j in range(len(data[0])):
            if data[i][j]=='^':
                guard_coord = (i,j)
            if data[i][j]=='#':
                obs_set.add((i,j))

    grid_dim = (len(data),len(data[0]))

    return obs_set,guard_coord, grid_dim

#check if the guard coordinates are inside the grid bounds 
#returns true if in bounds and false if out of bounds
def check_in_bounds(guard_coord,grid_dim):
    return 0<=guard_coord[0] and guard_coord[0]<grid_dim[0] and 0<=guard_coord[1] and guard_coord[1]<grid_dim[1]

#updates the guards position and direction
def update_state(guard_coord,guard_dir,obs_set):
    #the velocity vector describing how the guard_coord changes
    velocity = move_dict[guard_dir]

    #compute a candidate coordinate for the guard using current_velocity
    next_coord = (guard_coord[0]+velocity[0],guard_coord[1]+velocity[1])

    #while the candidate coordinate would run us into an obstacle...
    while next_coord in obs_set:
        #rotate the guard right by 90 degrees
        guard_dir = r_turn_dict[guard_dir]

        #compute a new velocity and candidate coord
        velocity = move_dict[guard_dir]
        next_coord = (guard_coord[0]+velocity[0],guard_coord[1]+velocity[1])

    #return the next position and velocity of the guard
    return next_coord,guard_dir

#checks to see if the guard would run into the additional obstacle (from current position and direction)
#before leaving the grid or running into one of the other obstacles
#INPUTS:
#guard_coord: current position of the guard
#guard_dir: current direction of the guard
#target coord: the predicted next location of the guard if it had gone in a straight line and then either
#                               hit another obstacle or gone out of bounds
#extra_obs: position of the extra obstacle
#OUTPUTS:
#blocking_coord: predicted position of guard after hitting extra obstacle
#blocking_dir: prediction direction of guard after hitting extra obstacle
#blocking_coord and blocking_dir are None if guard will collide with another obstacle (or leave bounds)
def is_blocking(guard_coord,guard_dir,target_coord,extra_obs):
    blocking_coord, blocking_dir = None, None

    if guard_dir == '>' and guard_coord[0]==extra_obs[0] and guard_coord[1]<extra_obs[1] and extra_obs[1]<=target_coord[1]:
        blocking_coord = (extra_obs[0],extra_obs[1]-1)
    if guard_dir == '<' and guard_coord[0]==extra_obs[0] and guard_coord[1]>extra_obs[1] and extra_obs[1]>=target_coord[1]:
        blocking_coord = (extra_obs[0],extra_obs[1]+1)
    if guard_dir == '^' and guard_coord[1]==extra_obs[1] and guard_coord[0]>extra_obs[0] and extra_obs[0]>=target_coord[0]:
        blocking_coord = (extra_obs[0]+1,extra_obs[1])
    if guard_dir == 'v' and guard_coord[1]==extra_obs[1] and guard_coord[0]<extra_obs[0] and extra_obs[0]<=target_coord[0]:
        blocking_coord = (extra_obs[0]-1,extra_obs[1])

    if blocking_coord is not None:
        blocking_dir = r_turn_dict[guard_dir]

    return blocking_coord, blocking_dir

#update the skipping dictionary
#given initial position and direction (pos1,dir1)
#the skip_dict is the map:
#skip_dict[(pos1,dir1)]=(pos2,dir2)
#where (pos2,dir2) is the final position and direction right after hitting
#the next obstacle in the grid (or leaving the grid) 
#INPUTS:
#guard_coord: starting position of the guard
#guard_dir: starting direction of the guard
#obs_set: set of obstacle positions from original grid
#skip_dict: a memoization table that allows skipping motion steps
#           by exploiting that guard mostly moves in a straight line
#grid_dim: dimensions of the grid
#OUTPUTS:
#no outputs, just updates the table for (guard_coord,guard_dir)
def update_skip_dict(guard_coord,guard_dir,obs_set,skip_dict,grid_dim):
    current_key = (guard_coord,guard_dir) #current (position,direction) of guard
    key_list = [current_key] #list of visited (position,direction) pairs
    final_key = None #value to store at location (guard_coord,guard_dir)

    #iterate until we have either collided with something or left the grid bounds
    while current_key[1]== guard_dir and check_in_bounds(current_key[0],grid_dim):

        #update (position,direction) of guard and append result to key_list
        current_key = update_state(key_list[-1][0],key_list[-1][1],obs_set)
        key_list.append(current_key)

        #if we are still traveling along the same straight line
        #but the current_key is in skip_dict
        if current_key[1]== guard_dir and current_key in skip_dict:
            #then, skip_dict[current_key] is our final state after collision/leaving bounds
            final_key = skip_dict[current_key]

            #in which case, we can just end the loop early
            break

    #if we terminated loop because of leaving grid bounds
    if not check_in_bounds(key_list[-1][0],grid_dim):
        #then the final state is just the last (position,direction) state
        final_key = key_list[-1]
    #if we terminated loop because of hitting an obstacle
    if key_list[-1][1] != guard_dir:
        #then use last direction, but previous position before collision
        #(because update_state turns and THEN moves, which isn't quite what we want)
        #i.e. we need position right before we hit obstacle, but direction of after we hit the obstacle
        final_key = (key_list[-2][0],key_list[-1][1])

    #get rid of last (position,direction) pair from our list
    key_list.pop(-1)

    #update the skip dict for all other visited (position,direction) pairs
    while len(key_list)>0:
        skip_dict[key_list.pop(-1)]=final_key

#find the next guard position and direction, while saving time by using a memoization table
#that allows the guard to skip forward until it hits the next obstacle or runs out of bounds
#INPUTS:
#guard_coord: starting position of the guard
#guard_dir: starting direction of the guard
#obs_set: set of obstacle positions from original grid
#extra_obs: position of the additional obstacle
#skip_dict: a memoization table that allows skipping motion steps
#           by exploiting that guard mostly moves in a straight line
#grid_dim: dimensions of the grid
def update_state_with_skip(guard_coord,guard_dir,obs_set,extra_obs,skip_dict,grid_dim):
    #lookup key for the memoization table
    current_key = (guard_coord,guard_dir)

    #if current (position,direction) is not in table, update the table so that it's in the table
    if current_key not in skip_dict: update_skip_dict(guard_coord,guard_dir,obs_set,skip_dict,grid_dim)

    #find the candidate position and direction using the lookup table
    next_key = skip_dict[current_key]

    #check to see if you would run into the extra obstacle instead
    blocking_coord, blocking_dir = is_blocking(guard_coord,guard_dir,next_key[0],extra_obs)

    #if you would run into the extra obstacle instead, return corresponding position and direction
    if blocking_coord is not None: return blocking_coord, blocking_dir

    #otherwise, retur the candidate position and direction (from lookup table)
    else: return next_key[0], next_key[1]


#check to see if placing an additional obstacle will result in a loop
#INPUTS:
#guard_coord: starting position of the guard
#guard_dir: starting direction of the guard
#obs_set: set of obstacle positions from original grid
#extra_obs: position of the additional obstacle
#skip_dict: a memoization table that allows skipping motion steps
#           by exploiting that guard mostly moves in a straight line
#grid_dim: dimensions of the grid
#OUTPUTS:
#returns True if placement results in a loop, False otherwise
def test_obs_placement(guard_coord,guard_dir,obs_set,extra_obs,skip_dict,grid_dim):
    #set of (coordinate,direction) pairs visited
    #if we ever visit the same pair twice, then we are in a loop
    visited_set = set()

    #loop until we get a repeat or leave bounds
    while True:
        #if a loop has been detected, return True
        if (guard_coord,guard_dir) in visited_set: return True
        
        #otherwise, add the current (position,direction) pair to the set
        visited_set.add((guard_coord,guard_dir))

        #if the guard has left the grid, loop is impossible, so return False
        if not check_in_bounds(guard_coord,grid_dim): return False

        #update the current position and direction (exploiting the skip table)
        guard_coord, guard_dir = update_state_with_skip(guard_coord,guard_dir,obs_set,extra_obs,skip_dict,grid_dim)
        


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    #guard_coord are the (i,j) coords of the guard (tuple)
    #obs_set is a set of the (i,j) coords of all obstacles in input
    #grid_dim are the dimensions of the character grid (height,width)
    obs_set,guard_coord, grid_dim = parse_input01(fname)
    guard_dir = '^' #starting direction of guard


    #set current position and direction to the starting position and direction
    current_coord, current_dir = guard_coord, guard_dir 
  
    basic_path_set = set() #set of guard positions when on regular path (no extra obstacles)
    
    #run the regular simulation (no extra obstacles)
    #while the guard is still in bounds
    while check_in_bounds(current_coord,grid_dim):

        #add the current coordinate to the basic path set
        basic_path_set.add(current_coord)

        #update the guard's position and direction
        current_coord, current_dir = update_state(current_coord,current_dir,obs_set)

    total1 = 1 #number of occupied tiles in basic path (no extra obstacles)
    total2 = 0 #number of coords where an additional obstacle would cause a loop

    skip_dict = dict() #memoization table to allow skipping forward multiple steps in a path

    #remove the guard_coord from the basic path set
    #because we don't need to test whether placing an obstacle there will cause a loop
    basic_path_set.discard(guard_coord) 

    #for every coordinate in the basic path
    for path_coord in basic_path_set:
        total1+=1 #tally number of occupied tiles

        #test if placing an obstacle at this location will cause loop
        #and increment the second tally if it does
        if test_obs_placement(guard_coord,guard_dir,obs_set,path_coord,skip_dict,grid_dim): total2+=1

    #print results
    print(total1)
    print(total2)

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

