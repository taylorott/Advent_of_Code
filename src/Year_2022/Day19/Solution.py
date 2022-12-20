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
    data = bh.parse_strings(path,fname,delimiters = [' ',':','\.','costs','robot','and','Blueprint'],type_lookup = None, allInt = False, allFloat = False)

    resource_lookup = {'ore':0,'clay':1,'obsidian':2,'geode':3}

    blueprint_dict = {}

    for blueprint in data:
        recipe_id = int(blueprint[0])
        blueprint_mat = []
        current_vector = None

        count = 1

        while count<len(blueprint):
            if blueprint[count]=='Each':
                if current_vector is not None:
                    blueprint_mat.append(current_vector.tolist())
                count+=2
                current_vector = np.array([0,0,0,0])
            else:
                current_vector[resource_lookup[blueprint[count+1]]]=int(blueprint[count])
                count+=2

        blueprint_mat.append(current_vector.tolist())
        blueprint_dict[recipe_id] = np.array(blueprint_mat)


    return blueprint_dict


def serialize_state(robots,resources,t):
    return (tuple(robots.tolist()),tuple(resources.tolist()),t)

def deserialize_state(state_in):
    return np.array(list(state_in[0])),np.array(list(state_in[1])),state_in[2]

def compute_next_posssible_states(robots,resources,t,blueprint,max_consumption_rate,max_val,tmax):
    list_out = []

    #Pruning Step #1: 
    #Compute the maximum ideal score from this current state
    #If that score is less than the current maximum score, don't bother, and terminate the branch
    #ideal max is current score + whatever extra can be produced by making a geode robot on every step forward
    current_score = resources[3]
    num_steps_remaining = (tmax-t)
    max_possible_score = current_score+(num_steps_remaining*(num_steps_remaining-1))/2

    if max_possible_score<=max_val:
        return []

    #compute the adjusted consumption rate
    #specifically how an upper bound on how much you can reduce the number of resources of each type per time step
    #taking into account that your robots are producing resources, and that you can eat a certain number of resources
    #by making a robot at each time step
    #this will be used to compute an upper bound on the number of resources to keep track of
    adjusted_consumption_rate = max_consumption_rate-robots

    for i in range(4):
        adjusted_consumption_rate[i]=max(adjusted_consumption_rate[i],0)

    #Iterate through possible choices for the next robot to build
    for i in range(4):
        build_order = np.array([0,0,0,0])
        build_order[i]=1

        can_build_next = True

        #is building this robot even worthwhile?
        #don't build a robot of a given resource type if the number of robots that you already
        #have of that type is greater than or equal to the max consumption rate of that resource type
        #the exception is geode robots, where you want as many as possible 
        can_build_next = can_build_next and (robots[i]<max_consumption_rate[i] or i==3)

        #can you even build this robot in the future from your current state?
        #if building a robot of type X requires a nonzero amount of resource type Y
        #and you don't have any robots of resource type Y, then you can't just sit and wait 
        #for resources of type Y to accumulate, since it will never happen.
        #Instead, you'll need to build a robot of a different type first, so don't choose type X
        #as the next robot to build
        for j in range(4):
            can_build_next = can_build_next and not (blueprint[i][j]>0 and robots[j]==0)

        if can_build_next:
            #Compute dt=resource_accumulation_time + (robot_build_time=1)
            #i.e. at time t+dt is the soonest time you will have added another robot of type X
            #to your fleet
            dt = 1
            while min(resources+robots*(dt-1)-blueprint[i])<0:
                dt+=1

            t_next = t+dt

            #compute robot fleet size after build order has been executed
            robots_next = robots+build_order

            #given your choice of build order and the number of time steps needed to do so
            #compute what your resources will be at that time
            resources_next = resources+robots*dt-blueprint[i]

            #compute the maximum number of resources you could ever need in your inventory at time t_next
            resource_limit = max_consumption_rate + adjusted_consumption_rate*(tmax-1-t_next)

            if t_next == tmax-1:
                resource_limit = np.array([0,0,0,0])

            #jettison all extra resources that you could never consume
            #the exception is geodes of course. keep all geodes
            for j in range(3):
                resources_next[j]=min(resources_next[j],resource_limit[j])

            if t_next<tmax:

                #if we made a geode robot, just compute how many geodes that robot will produce
                #and at it to the resource pool, then remove that geode robot from the fleet
                #since its work has been accounted for
                if i==3:
                    robots_next[3]=0
                    resources_next[3]+=(tmax-t_next)

                #append this state to the output list
                next_state = serialize_state(robots_next,resources_next,t_next)
                list_out.append(next_state)

    return list_out

#performs DFS with pruning to compute max number of geodes that can be produced by given blueprint
def compute_blueprint_score(blueprint,tmax):
    max_val = 0

    max_consumption_rate = np.array([0,0,0,0])

    for i in range(4):
        max_consumption_rate[i] = max(blueprint[:,i])

    t = 0
    robots = np.array([1,0,0,0])
    resources = np.array([0,0,0,0])

    current_state = serialize_state(robots,resources,t)

    myStack = []
    myStack.append(current_state)

    visited_dict = {current_state:None}

    while len(myStack)>0:
        current_state = myStack.pop()
        robots,resources,t = deserialize_state(current_state)

        if t<tmax:
            adjacent_state_list = compute_next_posssible_states(robots,resources,t,blueprint,max_consumption_rate,max_val,tmax)

            for next_state in adjacent_state_list:
                if next_state not in visited_dict:
                    max_val = max(max_val,next_state[1][3])
                    visited_dict[next_state]=None
                    myStack.append(next_state)

    return max_val

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    blueprint_dict = parse_input01(fname)
    
    total = 0
    for key in blueprint_dict:
        val_out = compute_blueprint_score(blueprint_dict[key],24)
        total += val_out*key

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    blueprint_dict = parse_input01(fname)
    
    total = 1
    for key in range(1,4):
        val_out = compute_blueprint_score(blueprint_dict[key],32)
        total*=val_out

    print(total)

    

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

