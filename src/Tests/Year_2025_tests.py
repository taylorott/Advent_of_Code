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


from Year_2025.Day01 import Solution as Day01
from Year_2025.Day02 import Solution as Day02
from Year_2025.Day03 import Solution as Day03
from Year_2025.Day04 import Solution as Day04
from Year_2025.Day05 import Solution as Day05
from Year_2025.Day06 import Solution as Day06
from Year_2025.Day07 import Solution as Day07
from Year_2025.Day08 import Solution as Day08
from Year_2025.Day09 import Solution as Day09
# from Year_2025.Day10 import Solution as Day10
# from Year_2025.Day11 import Solution as Day11
# from Year_2025.Day12 import Solution as Day12

path = currentdir

def Day01_test():
    current_day = Day01
    day_label = 'Day01'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 3, 6

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 1055, 6386

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname


def Day02_test():
    current_day = Day02
    day_label = 'Day02'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 1227775554, 4174379265

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 30323879646, 43872163557

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day03_test():
    current_day = Day03
    day_label = 'Day03'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 357, 3121910778619

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 17427, 173161749617495

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day04_test():
    current_day = Day04
    day_label = 'Day04'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 13, 43

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 1428, 8936

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day05_test():
    current_day = Day05
    day_label = 'Day05'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 3, 14

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 567, 354149806372909

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day06_test():
    current_day = Day06
    day_label = 'Day06'
    
    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 4277556, 3263827

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 4951502530386, 8486156119946

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname


def Day07_test():
    current_day = Day07
    day_label = 'Day07'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 21, 40

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)
    v1_true, v2_true = 1539, 6479180385864

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day08_test():
    current_day = Day08
    day_label = 'Day08'

    fname = 'Input01.txt'
    num_connections = 10

    v1, v2 = current_day.solution(show_result=False, fname=fname, num_connections=num_connections)
    v1_true, v2_true = 40, 25272

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    num_connections = 1000

    v1, v2 = current_day.solution(show_result=False, fname=fname, num_connections=num_connections)
    v1_true, v2_true = 79056, 4639477

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day09_test():
    current_day = Day09
    day_label = 'Day09'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 50, 24

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)
    v1_true, v2_true = 4750297200, 1578115935

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname
    assert v2==v2_true, day_label+", Part 2 Failed, Input: "+fname

def Day10_test():
    current_day = Day10
    day_label = 'Day10'

def Day11_test():
    current_day = Day11
    day_label = 'Day11'

def Day12_test():
    current_day = Day12
    day_label = 'Day12'


def run_all_tests():
    t0 = time.time()
    print('Day01 Test:')
    Day01_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')
    
    t0 = time.time()
    print('Day02 Test:')
    Day02_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day03 Test:')
    Day03_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day04 Test:')
    Day04_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day05 Test:')
    Day05_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day06 Test:')
    Day06_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day07 Test:')
    Day07_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day08 Test:')
    Day08_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day09 Test:')
    Day09_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    # t0 = time.time()
    # print('Day10 Test:')
    # Day10_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')

    # t0 = time.time()
    # print('Day11 Test:')
    # Day11_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')
    
    # t0 = time.time()
    # print('Day12 Test:')
    # Day12_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')


if __name__ == '__main__':
    t0 = time.time()
    print('Running Year 2025 Tests:')
    run_all_tests()
    print('total runtime in seconds: ','%.3f' % (time.time()-t0))
    
    