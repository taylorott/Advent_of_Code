#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    return data

def test_strat1(matches):
    rps_map = {'A':1,'B':2,'C':3}
    score_map = {0:3,1:6,2:0}
    strat_map = {'X':'A','Y':'B','Z':'C'}

    score = 0

    for match in matches:
        opp_rps = rps_map[match[0]]
        my_rps = rps_map[strat_map[match[1]]]

        match_result = (my_rps-opp_rps)%3

        score+=score_map[match_result]+my_rps

    return score

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    score = test_strat1(data)
    print(score)


def test_strat2(matches):
    rps_map = {'A':1,'B':2,'C':3}
    score_map = {0:3,1:6,2:0}
    strat_map = {'X':-1,'Y':0,'Z':1}

    score = 0
    for match in matches:
        opp_rps = rps_map[match[0]]
        my_rps = opp_rps+strat_map[match[1]]
        my_rps = ((my_rps-1)%3)+1

        match_result = (my_rps-opp_rps)%3

        score+=score_map[match_result]+my_rps

    return score

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    score = test_strat2(data)
    print(score)


if __name__ == '__main__':
    solution01()
    solution02()
    

