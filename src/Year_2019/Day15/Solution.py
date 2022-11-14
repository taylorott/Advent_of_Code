#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd
from collections import deque

path = currentdir

num_params_dict = {1:3,2:3,99:0,3:1,4:1,5:2,6:2,7:3,8:3,9:1}

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,[','],allInt=True)

    return data[0]

def parse_op_code(code_in):
    if code_in<0:
        return None,None

    op_code = code_in%100
    code_in//=100
    p1 = code_in%10
    code_in//=10
    p2 = code_in%10
    code_in//=10
    p3 = code_in%10

    #check to make sure code is valid
    if (not (op_code==99 or (1<=op_code and op_code<=9)) or
        not (0<=p1 and p1<=2) or not (0<=p2 and p2<=2) or not (0<=p3 and p3<=2)):
        return None,None

    return op_code,[p1,p2,p3]


class IntcodeComputer(object):
    def __init__(self,instructions):
        self.base_instructions = list(instructions)
        self.reset()

    def reset(self):
        self.generate_instruction_dict()
        self.instruction_pointer = 0
        self.relative_base = 0
        self.status = None

    def generate_instruction_dict(self):
        self.current_instructions = {}
        for i in range(len(self.base_instructions)):
            self.current_instructions[i] = self.base_instructions[i]

    def run_code(self,input_tape,silence_errors=False):
        output_tape = []
        input_index = 0
        while self.instruction_pointer<len(self.current_instructions):
            op_code,p_list = parse_op_code(self.current_instructions[self.instruction_pointer])

            if op_code is None:
                if not silence_errors:
                    print('invalid op code')
                self.status = 'invalid op code'
                return None

            num_params = num_params_dict[op_code]

            param_val_list = []
            address_list = []
            for i in range(num_params):
                if p_list[i]==0:
                    memory_address = self.current_instructions[self.instruction_pointer+1+i]
                    if memory_address<0:
                        if not silence_errors:
                            print('invalid memory location')
                        self.status = 'invalid memory location'
                        return None
                    elif memory_address not in self.current_instructions:
                        param_val_list.append(0)
                    else:
                        param_val_list.append(self.current_instructions[memory_address])
                    address_list.append(memory_address)
                elif p_list[i]==1:
                    memory_address = self.current_instructions[self.instruction_pointer+1+i]
                    param_val = self.current_instructions[self.instruction_pointer+1+i]
                    param_val_list.append(param_val)
                    address_list.append(memory_address)
                elif p_list[i]==2:
                    memory_address = self.current_instructions[self.instruction_pointer+1+i]+self.relative_base
                    if memory_address<0:
                        if not silence_errors:
                            print('invalid memory location')
                        self.status = 'invalid memory location'
                        return None
                    elif memory_address not in self.current_instructions:
                        param_val_list.append(0)
                    else:
                        param_val_list.append(self.current_instructions[memory_address])
                    address_list.append(memory_address)
                

            if op_code==1:
                if address_list[2]<0:
                    if not silence_errors:
                        print('invalid memory location')
                    self.status = 'invalid memory location'
                    return None
                self.current_instructions[address_list[2]]=param_val_list[0]+param_val_list[1]
                self.instruction_pointer+=num_params+1
            elif op_code==2:
                if address_list[2]<0:
                    if not silence_errors:
                        print('invalid memory location')
                    self.status = 'invalid memory location'
                    return None
                self.current_instructions[address_list[2]]=param_val_list[0]*param_val_list[1]
                self.instruction_pointer+=num_params+1
            elif op_code==3:
                if input_index>=len(input_tape):
                    if not silence_errors:
                        print('waiting for input')
                    self.status = 'waiting for input'
                    return output_tape
                self.current_instructions[address_list[0]]=input_tape[input_index]
                input_index+=1

                self.instruction_pointer+=num_params+1
            elif op_code==4:
                # print('print command: '+str(param_val_list[0]))
                output_tape.append(param_val_list[0])
                self.instruction_pointer+=num_params+1
            elif op_code==5:
                if param_val_list[0]!=0:
                    self.instruction_pointer=param_val_list[1]
                else:
                    self.instruction_pointer+=num_params+1
            elif op_code==6:
                if param_val_list[0]==0:
                    self.instruction_pointer=param_val_list[1]
                else:
                    self.instruction_pointer+=num_params+1

            elif op_code==7:
                if param_val_list[0]<param_val_list[1]:
                    self.current_instructions[address_list[2]]=1
                else:
                    self.current_instructions[address_list[2]]=0
                self.instruction_pointer+=num_params+1
            elif op_code==8:
                if param_val_list[0]==param_val_list[1]:
                    self.current_instructions[address_list[2]]=1
                else:
                    self.current_instructions[address_list[2]]=0
                self.instruction_pointer+=num_params+1
            elif op_code==9:
                self.relative_base+=param_val_list[0]
                self.instruction_pointer+=num_params+1
            elif op_code==99:
                if not silence_errors:
                    print('program completed')
                self.status = 'program completed'
                return output_tape

heading_dict_fwd = {1:np.array([-1,0]),2:np.array([1,0]),3:np.array([0,-1]),4:np.array([0,1])}
heading_dict_rev = {(-1,0):1,(1,0):2,(0,-1):3,(0,1):4}

def DFS_repair(myComp,visited_dict,current_coords,prev_coords=None):
    
    for h in range(1,5):
        dp_forward = heading_dict_fwd[h]
        next_coords = current_coords+dp_forward
        if (next_coords[0],next_coords[1]) not in visited_dict:
            output_tape = myComp.run_code([h],silence_errors=True)
            visited_dict[(next_coords[0],next_coords[1])]=output_tape[0]

            if output_tape[0]!=0:
                DFS_repair(myComp,visited_dict,next_coords,current_coords)

    if prev_coords is not None:      
        dp_reverse = prev_coords-current_coords
        heading_reverse = heading_dict_rev[(dp_reverse[0],dp_reverse[1])]
        output_tape = myComp.run_code([heading_reverse],silence_errors=True)


def generate_map(visited_dict):
    min_i = None
    max_i = None
    min_j = None
    max_j = None

    for key in visited_dict.keys():
        if min_i is None:
            min_i = key[0]
        if max_i is None:
            max_i = key[0]
        if min_j is None:
            min_j = key[1]
        if max_j is None:
            max_j = key[1]

        min_i = min(min_i,key[0])
        max_i = max(max_i,key[0])
        min_j = min(min_j,key[1])
        max_j = max(max_j,key[1])

    w = 1+max_j-min_j
    h = 1+max_i-min_i

    for a in range(h):
        str_out = ''
        for b in range(w):
            i = a+min_i
            j = b+min_j

            if (i,j) in visited_dict:
                str_out+=str(visited_dict[(i,j)])
            else:
                str_out+=' '
        print(str_out)



def solution01():
    fname = 'Input02.txt'
    data = parse_input01(fname)
    myComp = IntcodeComputer(data)

    visited_dict = {}
    current_coords = np.array([0,0])
    DFS_repair(myComp,visited_dict,current_coords)

    distance_dict = {(0,0):0}
    queue = deque([np.array([0,0])])
    num_items = 1

    while num_items>0:
        current_vertex = queue.popleft()
        num_items-=1
        current_key = (current_vertex[0],current_vertex[1])
        for i in range(1,5):
            next_vertex = current_vertex+heading_dict_fwd[i]

            next_key = (next_vertex[0],next_vertex[1])

            if next_key in visited_dict and visited_dict[next_key]!=0 and next_key not in distance_dict:
                distance_dict[next_key]=distance_dict[current_key]+1
                queue.append(next_vertex)
                num_items+=1

    for key in visited_dict:
        if visited_dict[key]==2:
            print(distance_dict[key])


    # print(visited_dict)
    # output_tape = myComp.run_code([])
    # generate_map(visited_dict)

def solution02():
    fname = 'Input02.txt'
    data = parse_input01(fname)
    myComp = IntcodeComputer(data)

    visited_dict = {}
    current_coords = np.array([0,0])
    DFS_repair(myComp,visited_dict,current_coords)

    distance_dict = {}
    queue = deque([])

    for key in visited_dict:
        if visited_dict[key]==2:
            distance_dict[key]=0
            queue.append(np.array([key[0],key[1]]))
 
    num_items = 1

    while num_items>0:
        current_vertex = queue.popleft()
        num_items-=1
        current_key = (current_vertex[0],current_vertex[1])
        for i in range(1,5):
            next_vertex = current_vertex+heading_dict_fwd[i]

            next_key = (next_vertex[0],next_vertex[1])

            if next_key in visited_dict and visited_dict[next_key]!=0 and next_key not in distance_dict:
                distance_dict[next_key]=distance_dict[current_key]+1
                queue.append(next_vertex)
                num_items+=1

    max_val = 0

    for key in distance_dict:
        max_val = max(max_val,distance_dict[key])

    print(max_val)



if __name__ == '__main__':
    solution01()
    solution02()
    

