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

def parse_input01(fname):
    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)


    
    data_out = []
    for line in data:
        line_out = []
        temp = line.replace('(',' ( ')
        temp = temp.replace(')',' ) ')
        splitstr = temp.split(' ')

        for item in splitstr:
            if item!='':
                line_out.append(item)
        data_out.append(line_out)
    return data_out


def eval_expression01(line):
    register_stack = [None]
    operator_stack = [None]

    for item in line:
        if item=='(':
            register_stack.append(None)
            operator_stack.append(None)
        elif item==')':
            temp_result = register_stack.pop(-1)
            operator_stack.pop(-1)

            if operator_stack[-1] is None:
                register_stack[-1] = temp_result
            elif operator_stack[-1] == '+':
                register_stack[-1] += temp_result
            elif operator_stack[-1] == '*':
                register_stack[-1] *= temp_result

        elif item=='*' or item=='+':
            operator_stack[-1] = item
        else:
            temp_result = int(item)

            if operator_stack[-1] is None:
                register_stack[-1] = temp_result
            elif operator_stack[-1] == '+':
                register_stack[-1] += temp_result
            elif operator_stack[-1] == '*':
                register_stack[-1] *= temp_result

    return register_stack[-1]

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    total = 0 
    for line in data:
        val = eval_expression01(line)
        # print(val)
        total+=val

    print(total)

def build_paren_dict(line):
    p_dict = {}
    my_stack = []

    for i in range(len(line)):
        if line[i]=='(':
            my_stack.append(i)
        elif line[i]==')':
            p_dict[my_stack.pop(-1)]=i

    return p_dict


def eval_expression02(line,indexA,indexB,paren_dict):

    index_current = indexA

    register = None

    while index_current<=indexB:
        if line[index_current]=='(':
            index_right = paren_dict[index_current]
            temp_result = eval_expression02(line,index_current+1,index_right-1,paren_dict)

            if register is None:
                register = temp_result
            else:
                register+= temp_result

            index_current = index_right+1

        elif line[index_current]==')':
            return register

        elif line[index_current]=='*':
            left_val = register
            right_val = eval_expression02(line,index_current+1,indexB,paren_dict)
            return left_val*right_val

        elif line[index_current]=='+':
            index_current+=1

        else:
            temp_result = int(line[index_current])

            if register is None:
                register = temp_result
            else:
                register+= temp_result
            index_current+=1
    return register



def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    parse_input01(fname)

    data = parse_input01(fname)
    total = 0 
    for line in data:
        p_dict = build_paren_dict(line)
        val = eval_expression02(line,0,len(line)-1,p_dict)
        # print(val)
        total+=val

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

