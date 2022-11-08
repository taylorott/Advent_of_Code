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
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    P1 = []
    P2 = []

    for i in range(1,len(data[0])):
        P1.append(int(data[0][i]))

    for i in range(1,len(data[1])):
        P2.append(int(data[1][i]))

    return P1,P2

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    P1,P2 = parse_input01(fname)

    while len(P1)>0 and len(P2)>0:
        if P1[0]>P2[0]:
            P1.append(P1.pop(0))
            P1.append(P2.pop(0))
        else:
            P2.append(P2.pop(0))
            P2.append(P1.pop(0))

    total = 0

    for i in range(len(P1)):
        total+=P1[i]*(len(P1)-i)

    for i in range(len(P2)):
        total+=P2[i]*(len(P2)-i)

    print(total)


def convert(list_in):
    return tuple(i for i in list_in)

def recursive_combat(L1,L2):
    game_state_dict = {}

    while len(L1)>0 and len(L2)>0:

        v1 = L1.pop(0)
        v2 = L2.pop(0)
        if v1<=len(L1) and v2<=len(L2):
            win_bool,dummy1,dummy_2 = recursive_combat(list(L1[0:v1]),list(L2[0:v2]))

            if win_bool:
                L1.append(v1)
                L1.append(v2)
            else: 
                L2.append(v2)
                L2.append(v1)
        else:
            if v1>v2:
                L1.append(v1)
                L1.append(v2)
            else: 
                L2.append(v2)
                L2.append(v1)
        game_state = (convert(L1),convert(L2))

        if game_state in game_state_dict:
            return True,L1,L2
        else:
            game_state_dict[game_state]=None

    if len(L1)>0:
        return True,L1,L2
    else:
        return False,L1,L2


def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    P1,P2 = parse_input01(fname)

    win_bool, L1,L2 = recursive_combat(P1,P2)

    total = 0

    for i in range(len(L1)):
        total+=L1[i]*(len(L1)-i)

    for i in range(len(L2)):
        total+=L2[i]*(len(L2)-i)

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    