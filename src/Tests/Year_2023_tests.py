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


from Year_2023.Day01 import Solution as Day01
from Year_2023.Day02 import Solution as Day02
from Year_2023.Day03 import Solution as Day03
from Year_2023.Day04 import Solution as Day04
from Year_2023.Day05 import Solution as Day05
from Year_2023.Day06 import Solution as Day06
from Year_2023.Day07 import Solution as Day07
from Year_2023.Day08 import Solution as Day08
from Year_2023.Day09 import Solution as Day09
from Year_2023.Day10 import Solution as Day10
from Year_2023.Day11 import Solution as Day11
from Year_2023.Day12 import Solution as Day12
from Year_2023.Day13 import Solution as Day13
from Year_2023.Day14 import Solution as Day14
from Year_2023.Day15 import Solution as Day15
from Year_2023.Day16 import Solution as Day16
from Year_2023.Day17 import Solution as Day17
from Year_2023.Day18 import Solution as Day18
from Year_2023.Day19 import Solution as Day19
from Year_2023.Day20 import Solution as Day20
from Year_2023.Day21 import Solution as Day21
from Year_2023.Day22 import Solution as Day22
from Year_2023.Day23 import Solution as Day23
from Year_2023.Day24 import Solution as Day24
from Year_2023.Day25 import Solution as Day25

path = currentdir

def Day01_test():

    fname = 'Input03.txt'
    v1 = Day01.solution01(show_result=False, fname=fname)
    v1_true = 142
    assert v1==v1_true, "Day01, Part 1 Failed, Input: "+fname+'\n Output: '+str(v1)+'\n Correct Output'+str(v1_true)

    fname = 'Input02.txt'
    v2 = Day01.solution02(show_result=False, fname=fname)
    assert v2==281, "Day01, Part 2 Failed, Input: "+fname

    fname = 'Input01.txt'
    v1 = Day01.solution01(show_result=False, fname=fname)
    v2 = Day01.solution02(show_result=False, fname=fname)

    assert v1==53974, "Day01, Part 1 Failed, Input: "+fname
    assert v2==52840, "Day01, Part 2 Failed, Input: "+fname

def Day02_test():
    fname = 'Input01.txt'
    v1 = Day02.solution01(show_result=False, fname=fname)
    v2 = Day02.solution02(show_result=False, fname=fname)
    assert v1==8, "Day02, Part 1 Failed, Input: "+fname
    assert v2==2286, "Day02, Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = Day02.solution01(show_result=False, fname=fname)
    v2 = Day02.solution02(show_result=False, fname=fname)

    assert v1==2545, "Day02, Part 1 Failed, Input: "+fname
    assert v2==78111, "Day02, Part 2 Failed, Input: "+fname


def Day03_test():
    return None

def Day04_test():
    return None

def Day05_test():
    return None

def Day06_test():
    return None

def Day07_test():
    return None

def Day08_test():
    return None

def Day09_test():
    return None

def Day10_test():
    return None

def Day11_test():
    return None

def Day12_test():
    return None

def Day13_test():
    return None

def Day14_test():
    return None

def Day15_test():
    return None

def Day16_test():
    return None

def Day17_test():
    return None

def Day18_test():
    return None

def Day19_test():
    return None

def Day20_test():
    return None

def Day21_test():
    return None

def Day22_test():
    return None

def Day23_test():
    return None

def Day24_test():
    return None

def Day25_test():
    return None

def run_all_tests():
    Day01_test()
    Day02_test()
    Day03_test()
    Day04_test()
    Day05_test()
    Day06_test()
    Day07_test()
    Day08_test()
    Day09_test()
    Day10_test()
    Day11_test()
    Day12_test()
    Day13_test()
    Day14_test()
    Day15_test()
    Day16_test()
    Day17_test()
    Day18_test()
    Day19_test()
    Day20_test()
    Day21_test()
    Day22_test()
    Day23_test()
    Day24_test()
    Day25_test()

if __name__ == '__main__':
    # Day01.solution01('Input03.txt')

    print('Running Year 2023 Tests:')
    run_all_tests()
    
    