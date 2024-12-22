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
from Year_2024.Day09 import Solution as Day09
from Year_2024.Day10 import Solution as Day10
from Year_2024.Day11 import Solution as Day11
from Year_2024.Day12 import Solution as Day12
from Year_2024.Day13 import Solution as Day13
from Year_2024.Day14 import Solution as Day14
from Year_2024.Day15 import Solution as Day15
from Year_2024.Day16 import Solution as Day16
# from Year_2024.Day17 import Solution as Day17
from Year_2024.Day18 import Solution as Day18
from Year_2024.Day19 import Solution as Day19
from Year_2024.Day20 import Solution as Day20
from Year_2024.Day21 import Solution as Day21
from Year_2024.Day22 import Solution as Day22
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

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==143, day_label+", Part 1 Failed, Input: "+fname
    assert v2==123, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==4774, day_label+", Part 1 Failed, Input: "+fname
    assert v2==6004, day_label+", Part 2 Failed, Input: "+fname

def Day06_test():
    current_day = Day06
    day_label = 'Day06'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==41, day_label+", Part 1 Failed, Input: "+fname
    assert v2==6, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==5177, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1686, day_label+", Part 2 Failed, Input: "+fname

def Day07_test():
    current_day = Day07
    day_label = 'Day07'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==3749, day_label+", Part 1 Failed, Input: "+fname
    assert v2==11387, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==1038838357795, day_label+", Part 1 Failed, Input: "+fname
    assert v2==254136560217241, day_label+", Part 2 Failed, Input: "+fname

def Day08_test():
    current_day = Day08
    day_label = 'Day08'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==14, day_label+", Part 1 Failed, Input: "+fname
    assert v2==34, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==265, day_label+", Part 1 Failed, Input: "+fname
    assert v2==962, day_label+", Part 2 Failed, Input: "+fname

def Day09_test():
    current_day = Day09
    day_label = 'Day09'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==1928, day_label+", Part 1 Failed, Input: "+fname
    assert v2==2858, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==6323641412437, day_label+", Part 1 Failed, Input: "+fname
    assert v2==6351801932670, day_label+", Part 2 Failed, Input: "+fname

def Day10_test():
    current_day = Day10
    day_label = 'Day10'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==36, day_label+", Part 1 Failed, Input: "+fname
    assert v2==81, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==611, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1380, day_label+", Part 2 Failed, Input: "+fname


def Day11_test():
    current_day = Day11
    day_label = 'Day11'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==55312, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==189092, day_label+", Part 1 Failed, Input: "+fname
    assert v2==224869647102559, day_label+", Part 2 Failed, Input: "+fname


def Day12_test():
    current_day = Day12
    day_label = 'Day12'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==1930, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1206, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==1446042, day_label+", Part 1 Failed, Input: "+fname
    assert v2==902742, day_label+", Part 2 Failed, Input: "+fname


def Day13_test():
    current_day = Day13
    day_label = 'Day13'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==480, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==32041, day_label+", Part 1 Failed, Input: "+fname
    assert v2==95843948914827, day_label+", Part 2 Failed, Input: "+fname

def Day14_test():
    current_day = Day14
    day_label = 'Day14'

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==225810288, day_label+", Part 1 Failed, Input: "+fname
    assert v2==6752, day_label+", Part 2 Failed, Input: "+fname

def Day15_test():
    current_day = Day15
    day_label = 'Day15'
    
    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==10092, day_label+", Part 1 Failed, Input: "+fname
    assert v2==9021, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==1538871, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1543338, day_label+", Part 2 Failed, Input: "+fname

def Day16_test():
    current_day = Day16
    day_label = 'Day16'
    
    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==7036, day_label+", Part 1 Failed, Input: "+fname
    assert v2==45, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==143564, day_label+", Part 1 Failed, Input: "+fname
    assert v2==593, day_label+", Part 2 Failed, Input: "+fname

# def Day17_test():
#     current_day = Day17
#     day_label = 'Day17'

def Day18_test():
    current_day = Day18
    day_label = 'Day18'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==22, day_label+", Part 1 Failed, Input: "+fname
    assert v2=='6,1', day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==340, day_label+", Part 1 Failed, Input: "+fname
    assert v2=='34,32', day_label+", Part 2 Failed, Input: "+fname

def Day19_test():
    current_day = Day19
    day_label = 'Day19'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==6, day_label+", Part 1 Failed, Input: "+fname
    assert v2==16, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==287, day_label+", Part 1 Failed, Input: "+fname
    assert v2==571894474468161, day_label+", Part 2 Failed, Input: "+fname

def Day20_test():
    current_day = Day20
    day_label = 'Day20'

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==1286, day_label+", Part 1 Failed, Input: "+fname
    assert v2==989316, day_label+", Part 2 Failed, Input: "+fname

def Day21_test():
    current_day = Day21
    day_label = 'Day21'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==126384, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==246990, day_label+", Part 1 Failed, Input: "+fname
    assert v2==306335137543664, day_label+", Part 2 Failed, Input: "+fname

def Day22_test():
    current_day = Day22
    day_label = 'Day22'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==37327623, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==17965282217, day_label+", Part 1 Failed, Input: "+fname
    assert v2==2152, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input03.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v2==23, day_label+", Part 2 Failed, Input: "+fname

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

    t0 = time.time()
    print('Day10 Test:')
    Day10_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day11 Test:')
    Day11_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')
    
    t0 = time.time()
    print('Day12 Test:')
    Day12_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')
    
    t0 = time.time()
    print('Day13 Test:')
    Day13_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day14 Test:')
    Day14_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day15 Test:')
    Day15_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day16 Test:')
    Day16_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    # t0 = time.time()
    # print('Day17 Test:')
    # Day17_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')

    t0 = time.time()
    print('Day18 Test:')
    Day18_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day19 Test:')
    Day19_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day20 Test:')
    Day20_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day21 Test:')
    Day21_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day22 Test:')
    Day22_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    # t0 = time.time()
    # print('Day23 Test:')
    # Day23_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')

    # t0 = time.time()
    # print('Day24 Test:')
    # Day24_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')

    # t0 = time.time()
    # print('Day25 Test:')
    # Day25_test()
    # print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    # print('')

if __name__ == '__main__':
    t0 = time.time()
    print('Running Year 2024 Tests:')
    run_all_tests()
    print('total runtime in seconds: ','%.3f' % (time.time()-t0))
    
    