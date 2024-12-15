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


from Year_2018.Day01 import Solution as Day01
from Year_2018.Day02 import Solution as Day02
from Year_2018.Day03 import Solution as Day03
from Year_2018.Day04 import Solution as Day04
from Year_2018.Day05 import Solution as Day05
from Year_2018.Day06 import Solution as Day06
from Year_2018.Day07 import Solution as Day07
from Year_2018.Day08 import Solution as Day08
from Year_2018.Day09 import Solution as Day09
from Year_2018.Day10 import Solution as Day10
from Year_2018.Day11 import Solution as Day11
from Year_2018.Day12 import Solution as Day12
# from Year_2018.Day13 import Solution as Day13
# from Year_2018.Day14 import Solution as Day14
# from Year_2018.Day15 import Solution as Day15
# from Year_2018.Day16 import Solution as Day16
# from Year_2018.Day17 import Solution as Day17
# from Year_2018.Day18 import Solution as Day18
# from Year_2018.Day19 import Solution as Day19
# from Year_2018.Day20 import Solution as Day20
# from Year_2018.Day21 import Solution as Day21
# from Year_2018.Day22 import Solution as Day22
# from Year_2018.Day23 import Solution as Day23
# from Year_2018.Day24 import Solution as Day24
# from Year_2018.Day25 import Solution as Day25

path = currentdir

def Day01_test():
    current_day = Day01
    day_label = 'Day01'

def Day02_test():
    current_day = Day02
    day_label = 'Day02'

def Day03_test():
    current_day = Day03
    day_label = 'Day03'

def Day04_test():
    current_day = Day04
    day_label = 'Day04'

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

def Day09_test():
    current_day = Day09
    day_label = 'Day09'

def Day10_test():
    current_day = Day10
    day_label = 'Day10'

def Day11_test():
    current_day = Day11
    day_label = 'Day11'

def Day12_test():
    current_day = Day12
    day_label = 'Day12'

def Day13_test():
    current_day = Day13
    day_label = 'Day13'

def Day14_test():
    current_day = Day14
    day_label = 'Day14'

def Day15_test():
    current_day = Day15
    day_label = 'Day15'

def Day16_test():
    current_day = Day16
    day_label = 'Day16'

def Day17_test():
    current_day = Day17
    day_label = 'Day17'

def Day18_test():
    current_day = Day18
    day_label = 'Day18'

def Day19_test():
    current_day = Day19
    day_label = 'Day19'

def Day20_test():
    current_day = Day20
    day_label = 'Day20'

def Day21_test():
    current_day = Day21
    day_label = 'Day21'

def Day22_test():
    current_day = Day22
    day_label = 'Day22'

def Day23_test():
    current_day = Day23
    day_label = 'Day23'

def Day24_test():
    current_day = Day24
    day_label = 'Day24'

def Day25_test():
    current_day = Day25
    day_label = 'Day25'

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

    t0 = time.time()
    print('Day17 Test:')
    Day17_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

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

    t0 = time.time()
    print('Day23 Test:')
    Day23_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day24 Test:')
    Day24_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')

    t0 = time.time()
    print('Day25 Test:')
    Day25_test()
    print('test runtime in seconds: ','%.3f' % (time.time()-t0))
    print('')
    

if __name__ == '__main__':
    print('Running Year 2018 Tests:')
    run_all_tests()
    
    