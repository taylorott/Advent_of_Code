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

def printState(screen_dict):
    max_i = 0
    max_j = 0

    for key in screen_dict.keys():
        max_i = max(max_i,key[0])
        max_j = max(max_j,key[1])

    for j in range(max_j+1):
        str_out = ''
        for i in range(max_i+1):
            key = (i,j)
            if key in screen_dict:
                val = screen_dict[key]
                if val==0:
                    str_out+=' '
                elif val==1:
                    str_out+='W'
                elif val==2:
                    str_out+='B'
                elif val==3:
                    str_out+='P'
                elif val==4:
                    str_out+='O'
            else:
                str_out+=' '
        print(str_out)


def solution01():
    fname = 'Input01.txt'
    data = parse_input01(fname)
    myComp = IntcodeComputer(data)

    output_tape = myComp.run_code([])

    screen_dict = {}

    i = 0
    while i < len(output_tape):
        key = (output_tape[i],output_tape[i+1])
        screen_dict[key] = output_tape[i+2]
        i+=3

    total = 0
    for key in screen_dict:
        if screen_dict[key]==2:
            total+=1
    print(total)
    # printState(screen_dict)

def get_state(screen_dict):
    ball_x = None
    paddle_x = None
    num_blocks = 0
    score = 0
    for key in screen_dict.keys():
        if key[0]==-1:
            score = screen_dict[key]
        else:
            val = screen_dict[key]

            if val==2:
                num_blocks+=1

            elif val==4:
                ball_x = key[0]

            elif val==3:
                paddle_x = key[0]

    return ball_x,paddle_x,num_blocks,score

def solution02():
    fname = 'Input01.txt'
    data = parse_input01(fname)
    data[0] = 2

    screen_dict = {}

    myComp = IntcodeComputer(data)

    num_blocks = None
    input_tape = []

    score = None

    while num_blocks!=0:
        output_tape = myComp.run_code(input_tape,silence_errors=True)

        i = 0
        while i < len(output_tape):
            key = (output_tape[i],output_tape[i+1])
            screen_dict[key] = output_tape[i+2]
            i+=3

        # printState(screen_dict)
        ball_x,paddle_x,num_blocks,score = get_state(screen_dict)
        if ball_x>paddle_x:
            input_tape = [1]
        elif ball_x==paddle_x:
            input_tape = [0]
        elif ball_x<paddle_x:
            input_tape = [-1]


    print(score)



if __name__ == '__main__':
    solution01()
    solution02()
    

