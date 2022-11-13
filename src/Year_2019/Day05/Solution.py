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

num_params_dict = {1:3,2:3,99:0,3:1,4:1,5:2,6:2,7:3,8:3}
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
    if (not (op_code==99 or (1<=op_code and op_code<=8)) or
        not (p1==0 or p1==1) or not (p2==0 or p2==1) or not (p3==0 or p3==1)):
        return None,None

    return op_code,[p1,p2,p3]

def run_code(instruction_list,input_tape,silence_errors=False):
    temp_list = list(instruction_list)

    input_index = 0
    current_index = 0
    while current_index<len(temp_list):
        op_code,p_list = parse_op_code(temp_list[current_index])

        if op_code is None:
            if not silence_errors:
                print('invalid op code')
            return None

        num_params = num_params_dict[op_code]

        param_val_list = []
        address_list = []
        for i in range(num_params):
            if p_list[i]==0:
                memory_address = temp_list[current_index+1+i]
                if memory_address <0 or memory_address>=len(temp_list):
                    if not silence_errors:
                        print('invalid memory location')
                    return None
                param_val_list.append(temp_list[memory_address])
            elif p_list[i]==1:
                param_val = temp_list[current_index+1+i]
                param_val_list.append(param_val)
            address_list.append(temp_list[current_index+1+i])

        if op_code==1:
            temp_list[address_list[2]]=param_val_list[0]+param_val_list[1]
            current_index+=num_params+1
        elif op_code==2:
            temp_list[address_list[2]]=param_val_list[0]*param_val_list[1]
            current_index+=num_params+1
        elif op_code==3:
            if input_index>=len(input_tape):
                if not silence_errors:
                    print('ran out of inputs!')
                return None
            temp_list[address_list[0]]=input_tape[input_index]
            input_index+=1

            current_index+=num_params+1
        elif op_code==4:
            print('print command: '+str(param_val_list[0]))
            current_index+=num_params+1
        elif op_code==5:
            if param_val_list[0]!=0:
                current_index=param_val_list[1]
            else:
                current_index+=num_params+1
        elif op_code==6:
            if param_val_list[0]==0:
                current_index=param_val_list[1]
            else:
                current_index+=num_params+1

        elif op_code==7:
            if param_val_list[0]<param_val_list[1]:
                temp_list[address_list[2]]=1
            else:
                temp_list[address_list[2]]=0
            current_index+=num_params+1
        elif op_code==8:
            if param_val_list[0]==param_val_list[1]:
                temp_list[address_list[2]]=1
            else:
                temp_list[address_list[2]]=0
            current_index+=num_params+1
        elif op_code==99:
            if not silence_errors:
                print('terminate program')
            return None

        

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    
    run_code(data,[1])

def solution02():
    # fname = 'Input01.txt'

    # data = parse_input01(fname)
    # run_code(data,[3])
    # run_code(data,[8])
    # run_code(data,[35])

    fname = 'Input02.txt'

    data = parse_input01(fname)
    run_code(data,[5])

if __name__ == '__main__':
    solution01()
    solution02()
    

