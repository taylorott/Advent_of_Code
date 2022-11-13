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

def is_valid(q):
    digit_list = []

    for i in range(6):
        digit_list.append(q%10)
        q//=10

    for i in range(5):
        if digit_list[i]<digit_list[i+1]:
            return 0

    for i in range(5):
        if digit_list[i]==digit_list[i+1]:
            return 1
    return 0



def solution01():
    total = 0
    for i in range(264360,746325+1):
        total+=is_valid(i)
    print(total)

def is_valid2(q):
    digit_list = []
    freq_table = {}
    for i in range(6):
        digit = q%10
        digit_list.append(digit)
        q//=10

        if digit in freq_table:
            freq_table[digit]+=1
        else:
            freq_table[digit]=1

    for i in range(5):
        if digit_list[i]<digit_list[i+1]:
            return 0

    for key in freq_table:
        if freq_table[key]==2:
            return 1
    return 0

def solution02():
    total = 0
    for i in range(264360,746325+1):
        total+=is_valid2(i)
    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

