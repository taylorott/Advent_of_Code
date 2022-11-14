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


def generate_permutation_list(list_in,list_out=None,current_index = 0):
    if list_out is None:
        list_out = []


    if current_index == len(list_in)-1:
        list_out.append(list(list_in))
        return list_out

    for i in range(current_index,len(list_in)):
        temp = list_in[i]
        list_in[i]=list_in[current_index]
        list_in[current_index]=temp

        generate_permutation_list(list_in,list_out,current_index+1)

        temp = list_in[i]
        list_in[i]=list_in[current_index]
        list_in[current_index]=temp

    return list_out


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

def run_code(instruction_list,input_tape,silence_errors=False,make_copy=True,current_index = 0):
    if make_copy:
        instruction_list = list(instruction_list)

    input_index = 0
    while current_index<len(instruction_list):
        op_code,p_list = parse_op_code(instruction_list[current_index])

        if op_code is None:
            if not silence_errors:
                print('invalid op code')
            return None,current_index

        num_params = num_params_dict[op_code]

        param_val_list = []
        address_list = []
        for i in range(num_params):
            if p_list[i]==0:
                memory_address = instruction_list[current_index+1+i]
                if memory_address <0 or memory_address>=len(instruction_list):
                    if not silence_errors:
                        print('invalid memory location')
                    return None,current_index
                param_val_list.append(instruction_list[memory_address])
            elif p_list[i]==1:
                param_val = instruction_list[current_index+1+i]
                param_val_list.append(param_val)
            address_list.append(instruction_list[current_index+1+i])

        if op_code==1:
            instruction_list[address_list[2]]=param_val_list[0]+param_val_list[1]
            current_index+=num_params+1
        elif op_code==2:
            instruction_list[address_list[2]]=param_val_list[0]*param_val_list[1]
            current_index+=num_params+1
        elif op_code==3:
            if input_index>=len(input_tape):
                if not silence_errors:
                    print('ran out of inputs!')
                return None,current_index
            instruction_list[address_list[0]]=input_tape[input_index]
            input_index+=1

            current_index+=num_params+1
        elif op_code==4:
            # print('print command: '+str(param_val_list[0]))
            current_index+=num_params+1
            return param_val_list[0],current_index
            
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
                instruction_list[address_list[2]]=1
            else:
                instruction_list[address_list[2]]=0
            current_index+=num_params+1
        elif op_code==8:
            if param_val_list[0]==param_val_list[1]:
                instruction_list[address_list[2]]=1
            else:
                instruction_list[address_list[2]]=0
            current_index+=num_params+1
        elif op_code==99:
            if not silence_errors:
                print('terminate program')
            return 'terminated',current_index
    return None
    
class Amplifier(object):
    def __init__(self,instructions):
        self.has_run_once = False
        self.setting = None
        self.base_instructions = list(instructions)
        self.current_instructions = list(instructions)
        self.current_index = 0
    def reset_amplifier(self):
        self.current_instructions=list(self.base_instructions)
        self.has_run_once = False
        self.current_index = 0
    def change_settings(self,setting_in):
        self.setting = setting_in
        self.reset_amplifier()
    def run_with_input(self,my_input):
        q = None
        if self.has_run_once:
            q,current_index = run_code(self.current_instructions,[my_input],make_copy=False,silence_errors=True, current_index = self.current_index)
        else:
            q,current_index = run_code(self.current_instructions,[self.setting,my_input],make_copy=False,silence_errors=True, current_index = self.current_index)
            self.has_run_once = True
        self.current_index = current_index
        return q

class AmplifierChain(object):
    def __init__(self,instructions):
        self.amplifier_list = []
        for i in range(5):
            self.amplifier_list.append(Amplifier(instructions))

    def reset_amplifiers(self):
        for i in range(5):
            self.amplifer_list[i].reset_amplifier()

    def change_settings(self,settings_list):
        for i in range(5):
            self.amplifier_list[i].change_settings(settings_list[i])

    def run_amplifiers_loop(self):
        current_val = 0
        val_list = [None]*5
        while True:
            for i in range(5):
                current_val = self.amplifier_list[i].run_with_input(current_val)
                if current_val is None:
                    print('error occured! terminating!')
                    return None
                elif current_val == 'terminated':
                    return val_list[-1]
                else:
                    val_list[i]=current_val

    def run_amplifiers(self):
        current_val = 0

        val_list = [None]*5
        for i in range(5):
            current_val = self.amplifier_list[i].run_with_input(current_val)
            if current_val is None:
                print('error occured! terminating!')
                return None
            elif current_val == 'terminated':
                return val_list[-1]
            else:
                val_list[i]=current_val

        return val_list[-1]



def solution01():
    # fname = 'Input01.txt'
    # fname = 'Input03.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    max_val = None

    myChain = AmplifierChain(data)
    permutation_list = generate_permutation_list([0,1,2,3,4])

    for settings_list in permutation_list:
        myChain.change_settings(settings_list)
        val_out = myChain.run_amplifiers()
        if val_out is not None:
            if max_val is None:
                max_val = val_out
            else:
                max_val = max(max_val,val_out)

    print(max_val)
def solution02():
    # fname = 'Input04.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    max_val = None

    myChain = AmplifierChain(data)

    permutation_list = generate_permutation_list([5,6,7,8,9])
    for settings_list in permutation_list:
        myChain.change_settings(settings_list)
        val_out = myChain.run_amplifiers_loop()
        if val_out is not None:
            if max_val is None:
                max_val = val_out
            else:
                max_val = max(max_val,val_out)
    print(max_val)


if __name__ == '__main__':
    solution01()
    solution02()
    

