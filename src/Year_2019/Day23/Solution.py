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

num_params_dict = {1:3,2:3,99:0,3:1,4:1,5:2,6:2,7:3,8:3,9:1}

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [','],type_lookup = None, allInt = True, allFloat = False)

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

def update_system(comp_list,output_buffer,input_buffer):

    NAT_buffer = []

    num_computers = len(comp_list)
    is_idle = True 
    for i in range(num_computers):
        while len(output_buffer[i])>0:
            address = output_buffer[i].popleft()
            x = output_buffer[i].popleft()
            y = output_buffer[i].popleft()

            is_idle = False

            if address==255:
                NAT_buffer.append([x,y])
            else:
                input_buffer[address].append(x)
                input_buffer[address].append(y)

    for i in range(num_computers):
        if len(input_buffer[i])!=0:
            output_tape = comp_list[i].run_code(list(input_buffer[i]),silence_errors=True)

            is_idle = is_idle and len(output_tape)==0

            output_buffer[i] = deque(output_tape)
            input_buffer[i] = deque()
        else:
            output_tape = comp_list[i].run_code([-1],silence_errors=True)

            is_idle = is_idle and len(output_tape)==0

            output_buffer[i] = deque(output_tape)
            input_buffer[i] = deque()


    return NAT_buffer, is_idle



def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'


    data = parse_input01(fname)

    comp_list = []
    output_buffer = []
    input_buffer = []

    for i in range(50):
        comp_list.append(IntcodeComputer(data))

        output_buffer.append(deque())
        input_buffer.append(deque())

        output_tape = comp_list[i].run_code([i,-1],silence_errors=True)

        output_buffer[i] = deque(output_tape)

    result = []
    while len(result)==0:
        result,is_idle = update_system(comp_list,output_buffer,input_buffer)
    print(result[0][1])


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)

    comp_list = []
    output_buffer = []
    input_buffer = []

    for i in range(50):
        comp_list.append(IntcodeComputer(data))

        output_buffer.append(deque())
        input_buffer.append(deque())

        output_tape = comp_list[i].run_code([i,-1],silence_errors=True)

        output_buffer[i] = deque(output_tape)

    nat_val = None

    nat_sent_list = []

    while len(nat_sent_list)<2 or nat_sent_list[-1]!=nat_sent_list[-2]:
        is_idle = False
        while not is_idle:
            result,is_idle = update_system(comp_list,output_buffer,input_buffer)
            
            if len(result)>0:
                nat_val = result[-1]
                
        nat_sent_list.append(nat_val[1])
        input_buffer[0]=deque(nat_val)
        
    print(nat_sent_list[-1])


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

