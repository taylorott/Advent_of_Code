#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(currentdir))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque 

path = currentdir

def test_lists():

    n = 100000


    list1 = []

    t0 = time.time()
    for i in range(n):
        list1.append(i)
    for i in range(n):
        list1.pop(-1)
    t1 = time.time()

    print('time append + pop right = '+'%.3f' % (t1-t0))

    list2 = []

    t0 = time.time()
    for i in range(n):
        list2.append(i)
    for i in range(n):
        list2.pop(0)
    t1 = time.time()

    print('time append + pop left = '+'%.3f' % (t1-t0))

if __name__ == '__main__':
    test_lists()
    

