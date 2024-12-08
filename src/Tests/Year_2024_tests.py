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


from Year_2024.Day01 import Solution as Day01
from Year_2024.Day02 import Solution as Day02
from Year_2024.Day03 import Solution as Day03
from Year_2024.Day04 import Solution as Day04
from Year_2024.Day05 import Solution as Day05
from Year_2024.Day06 import Solution as Day06
from Year_2024.Day07 import Solution as Day07
from Year_2024.Day08 import Solution as Day08
# from Year_2024.Day09 import Solution as Day09
# from Year_2024.Day10 import Solution as Day10
# from Year_2024.Day11 import Solution as Day11
# from Year_2024.Day12 import Solution as Day12
# from Year_2024.Day13 import Solution as Day13
# from Year_2024.Day14 import Solution as Day14
# from Year_2024.Day15 import Solution as Day15
# from Year_2024.Day16 import Solution as Day16
# from Year_2024.Day17 import Solution as Day17
# from Year_2024.Day18 import Solution as Day18
# from Year_2024.Day19 import Solution as Day19
# from Year_2024.Day20 import Solution as Day20
# from Year_2024.Day21 import Solution as Day21
# from Year_2024.Day22 import Solution as Day22
# from Year_2024.Day23 import Solution as Day23
# from Year_2024.Day24 import Solution as Day24
# from Year_2024.Day25 import Solution as Day25

path = currentdir

def Day01_test():
    current_day = Day01
    day_label = 'Day01'

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==11, day_label+", Part 1 Failed, Input: "+fname
    assert v2==31, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==2367773, day_label+", Part 1 Failed, Input: "+fname
    assert v2==21271939, day_label+", Part 2 Failed, Input: "+fname

def Day02_test():
    current_day = Day02
    day_label = 'Day02'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==2, day_label+", Part 1 Failed, Input: "+fname
    assert v2==4, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==463, day_label+", Part 1 Failed, Input: "+fname
    assert v2==514, day_label+", Part 2 Failed, Input: "+fname

def Day03_test():
    current_day = Day03
    day_label = 'Day03'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    assert v1==161, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input03.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    assert v2==48, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==189527826, day_label+", Part 1 Failed, Input: "+fname
    assert v2==63013756, day_label+", Part 2 Failed, Input: "+fname

def Day04_test():
    current_day = Day04
    day_label = 'Day04'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==18, day_label+", Part 1 Failed, Input: "+fname
    assert v2==9, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==2500, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1933, day_label+", Part 2 Failed, Input: "+fname

def Day05_test():
    current_day = Day05
    day_label = 'Day05'

def Day06_test():
    current_day = Day06
    day_label = 'Day06'

def Day07_test():
    current_day = Day07
    day_label = 'Day07'

def Day08_test():
    current_day = Day08
    day_label = 'Day08'

# def Day09_test():
#     current_day = Day09
#     day_label = 'Day09'

# def Day10_test():
#     current_day = Day10
#     day_label = 'Day10'

# def Day11_test():
#     current_day = Day11
#     day_label = 'Day11'

# def Day12_test():
#     current_day = Day12
#     day_label = 'Day12'

# def Day13_test():
#     current_day = Day13
#     day_label = 'Day13'

# def Day14_test():
#     current_day = Day14
#     day_label = 'Day14'

# def Day15_test():
#     current_day = Day15
#     day_label = 'Day15'

# def Day16_test():
#     current_day = Day16
#     day_label = 'Day16'

# def Day17_test():
#     current_day = Day17
#     day_label = 'Day17'

# def Day18_test():
#     current_day = Day18
#     day_label = 'Day18'

# def Day19_test():
#     current_day = Day19
#     day_label = 'Day19'

# def Day20_test():
#     current_day = Day20
#     day_label = 'Day20'

# def Day21_test():
#     current_day = Day21
#     day_label = 'Day21'

# def Day22_test():
#     current_day = Day22
#     day_label = 'Day22'

# def Day23_test():
#     current_day = Day23
#     day_label = 'Day23'

# def Day24_test():
#     current_day = Day24
#     day_label = 'Day24'

# def Day25_test():
#     current_day = Day25
#     day_label = 'Day25'

def run_all_tests():
    Day01_test()
    Day02_test()
    Day03_test()
    Day04_test()
    Day05_test()
    Day06_test()
    Day07_test()
    Day08_test()
    # Day09_test()
    # Day10_test()
    # Day11_test()
    # Day12_test()
    # Day13_test()
    # Day14_test()
    # Day15_test()
    # Day16_test()
    # Day17_test()
    # Day18_test()
    # Day19_test()
    # Day20_test()
    # Day21_test()
    # Day22_test()
    # Day23_test()
    # Day24_test()
    # Day25_test()

if __name__ == '__main__':
    print('Running Year 2024 Tests:')
    run_all_tests()
    
    