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







def solution01():
    fname = 'Input02.txt'
    data = parse_input01(fname)
    myComp = IntcodeComputer(data)

    output_tape = myComp.run_code([],silence_errors=True)

    str_out = ''

    mat_out = []
    mat_out.append([])
    for item in output_tape:
        if item==10:
            mat_out.append([])
        else:
            mat_out[-1].append(chr(item))

    while len(mat_out[-1])==0:
        mat_out.pop(-1)

    total = 0
    direction_dict = {0:[1,0],1:[-1,0],2:[0,1],3:[0,-1],4:[0,0]}
    for i in range(1,len(mat_out)-1):
        for j in range(1,len(mat_out[0])-1):
            is_intersection = True
            for k in range(5):
                delta_p = direction_dict[k]
                i_temp = i+delta_p[0]
                j_temp = j+delta_p[1]
                is_intersection = is_intersection and mat_out[i_temp][j_temp] =='#'

            if is_intersection:
                total+=i*j
    print(total)

def solution02():
    fname = 'Input02.txt'
    data = parse_input01(fname)

    data[0]=2


    main_movement = 'A,B,A,C,A,B,C,A,B,C'
    move_A = 'R,8,R,10,R,10'
    move_B = 'R,4,R,8,R,10,R,12'
    move_C = 'R,12,R,4,L,12,L,12'
    feed_on = 'n'

    commands_in = [main_movement,move_A,move_B,move_C,feed_on]
    input_list = []

    for line in commands_in:
        for item in line:
            input_list.append(ord(item))
        input_list.append(10)

    myComp = IntcodeComputer(data)

    output_tape = myComp.run_code(input_list,silence_errors=True)

    # str_out = ''

    # for item in output_tape:
    #     str_out+=chr(item)

    # print(str_out)

    print(output_tape[-1])

if __name__ == '__main__':
    solution01()
    solution02()
    

