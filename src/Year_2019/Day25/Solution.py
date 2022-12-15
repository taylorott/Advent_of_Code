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


def list_to_string(list_in):
    str_out = ''
    for item in list_in:
        if item<=255:
            str_out+=chr(item)
        else:
            str_out+=str(item)
    return str_out

def command_to_list(str_in):
    list_out = []
    for item in str_in:
        list_out.append(ord(item))
    list_out.append(10)
    return list_out

def parse_description(output_tape,print_messages=True):
    output_str = list_to_string(output_tape).split('\n')

    dict_out = {}
    count = 0
    while count<len(output_str):

        line = output_str[count]
        if print_messages:
            print(line)

        if len(line)>0 and line[0]=='=':
            dict_out['location'] = line
            count+=1
        elif line=='Doors here lead:':
            doors_list = []
            count+=1
            while len(output_str[count])>0:
                if print_messages:
                    print(output_str[count])
                doors_list.append(output_str[count][2:])
                count+=1

            dict_out['doors']=doors_list
        elif line=='Items here:':
            items_list = []
            count+=1
            while len(output_str[count])>0:
                if print_messages:
                    print(output_str[count])
                items_list.append(output_str[count][2:])
                count+=1

            dict_out['items']=items_list
        else:
            count+=1

    if 'items' not in dict_out:
        dict_out['items']=[]

    return dict_out

def generate_drops(drop_list,num):
    drop_list_out = []
    bin_str = bin(num)

    i = 0

    while i<len(bin_str)-2 and i<len(drop_list):
        if bin_str[len(bin_str)-1-i]=='1':
            drop_list_out.append(drop_list[i])
        i+=1 
    return drop_list_out

def attempt_to_pass_security(myComp,command_list,drop_list,num):

    myComp.reset()
    new_drop_list = generate_drops(drop_list,num)

    new_command_list = list(command_list)+new_drop_list
    new_command_list.append('north')

    output_tape = myComp.run_code([],silence_errors=True)
    # print(list_to_string(output_tape))

    for command in new_command_list:
        # print(command)
        command_code = command_to_list(command)
        output_tape = myComp.run_code(command_code,silence_errors=True)
        dict_out = parse_description(output_tape,False)
    if dict_out['location']!='== Security Checkpoint ==':
        
        parse_description(output_tape,False)
        print(new_drop_list)

def solution01():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    data = parse_input01(fname)
    myComp = IntcodeComputer(data)

    # observatory
    command_list = ['north','north','west','take mug',
                    'east','north','east','east','take loom',
                    'west','west','south','south','south',
                    'east','take food ration','east','take manifold',
                    'east','east','take jam','west','north',
                    'east','take spool of cat6','west','north',
                    'take fuel cell','south','south','west',
                    'south','north','west','south','take prime number',
                    'north','west','north','west','north','south',
                    'east','north','west','east','north','east','east',
                    'west','west','south','south','west','north','west']

    drop_list  =  [ 'drop jam',
                    'drop prime number',
                    'drop food ration',
                    'drop manifold',
                    'drop loom',
                    'drop spool of cat6',
                    'drop mug',
                    'drop fuel cell',]

    # for i in range(2**8):
    #     attempt_to_pass_security(myComp,command_list,drop_list,i)  

    correct_drop_list = ['drop jam', 'drop manifold', 'drop loom', 'drop spool of cat6']

    command_list+=correct_drop_list
    command_list+=['north']

    output_tape = myComp.run_code([],silence_errors=True)
    # print(list_to_string(output_tape))

    for command in command_list:
        # print(command)
        command_code = command_to_list(command)
        output_tape = myComp.run_code(command_code,silence_errors=True)
        dict_out = parse_description(output_tape,True)


def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # data = parse_input01(fname)

   

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

