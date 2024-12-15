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
    current_day = Day01
    day_label = 'Day01'

    fname = 'Input03.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v1_true = 142

    assert v1==v1_true, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v2==281, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==53974, day_label+", Part 1 Failed, Input: "+fname
    assert v2==52840, day_label+", Part 2 Failed, Input: "+fname

def Day02_test():
    current_day = Day02
    day_label = 'Day02'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==8, day_label+", Part 1 Failed, Input: "+fname
    assert v2==2286, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==2545, day_label+", Part 1 Failed, Input: "+fname
    assert v2==78111, day_label+", Part 2 Failed, Input: "+fname

def Day03_test():
    current_day = Day03
    day_label = 'Day03'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==4361, day_label+", Part 1 Failed, Input: "+fname
    assert v2==467835, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==512794, day_label+", Part 1 Failed, Input: "+fname
    assert v2==67779080, day_label+", Part 2 Failed, Input: "+fname

def Day04_test():
    current_day = Day04
    day_label = 'Day04'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==13, day_label+", Part 1 Failed, Input: "+fname
    assert v2==30, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==21138, day_label+", Part 1 Failed, Input: "+fname
    assert v2==7185540, day_label+", Part 2 Failed, Input: "+fname

def Day05_test():
    current_day = Day05
    day_label = 'Day05'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==35, day_label+", Part 1 Failed, Input: "+fname
    assert v2==46, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==318728750, day_label+", Part 1 Failed, Input: "+fname
    assert v2==37384986, day_label+", Part 2 Failed, Input: "+fname

def Day06_test():
    current_day = Day06
    day_label = 'Day06'
    
    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==288, day_label+", Part 1 Failed, Input: "+fname
    assert v2==71503, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==4403592, day_label+", Part 1 Failed, Input: "+fname
    assert v2==38017587, day_label+", Part 2 Failed, Input: "+fname

def Day07_test():
    current_day = Day07
    day_label = 'Day07'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==6440, day_label+", Part 1 Failed, Input: "+fname
    assert v2==5905, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==250602641, day_label+", Part 1 Failed, Input: "+fname
    assert v2==251037509, day_label+", Part 2 Failed, Input: "+fname


def Day08_test():
    current_day = Day08
    day_label = 'Day08'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)

    assert v1==2, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input03.txt'
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v2==6, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==13301, day_label+", Part 1 Failed, Input: "+fname
    assert v2==7309459565207, day_label+", Part 2 Failed, Input: "+fname

def Day09_test():
    current_day = Day09
    day_label = 'Day09'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==114, day_label+", Part 1 Failed, Input: "+fname
    assert v2==2, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==1974913025, day_label+", Part 1 Failed, Input: "+fname
    assert v2==884, day_label+", Part 2 Failed, Input: "+fname

def Day10_test():
    current_day = Day10
    day_label = 'Day10'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)

    assert v1==8, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input03.txt'
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v2==8, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input04.txt'
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v2==10, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==7086, day_label+", Part 1 Failed, Input: "+fname
    assert v2==317, day_label+", Part 2 Failed, Input: "+fname

def Day11_test():
    current_day = Day11
    day_label = 'Day11'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname, mult_val = 10)
    v3 = current_day.solution02(show_result=False, fname=fname, mult_val = 100)

    assert v1==374, day_label+", Part 1 Failed, Input: "+fname
    assert v2==1030, day_label+", Part 2 Failed, Input: "+fname
    assert v3==8410, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==10289334, day_label+", Part 1 Failed, Input: "+fname
    assert v2==649862989626, day_label+", Part 2 Failed, Input: "+fname

def Day12_test():
    current_day = Day12
    day_label = 'Day12'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==21, day_label+", Part 1 Failed, Input: "+fname
    assert v2==525152, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==6981, day_label+", Part 1 Failed, Input: "+fname
    assert v2==4546215031609, day_label+", Part 2 Failed, Input: "+fname

def Day13_test():
    current_day = Day13
    day_label = 'Day13'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==405, day_label+", Part 1 Failed, Input: "+fname
    assert v2==400, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==30487, day_label+", Part 1 Failed, Input: "+fname
    assert v2==31954, day_label+", Part 2 Failed, Input: "+fname

def Day14_test():
    current_day = Day14
    day_label = 'Day14'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==136, day_label+", Part 1 Failed, Input: "+fname
    assert v2==64, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==106186, day_label+", Part 1 Failed, Input: "+fname
    assert v2==106390, day_label+", Part 2 Failed, Input: "+fname

def Day15_test():
    current_day = Day15
    day_label = 'Day15'
            
    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==1320, day_label+", Part 1 Failed, Input: "+fname
    assert v2==145, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==495972, day_label+", Part 1 Failed, Input: "+fname
    assert v2==245223, day_label+", Part 2 Failed, Input: "+fname

def Day16_test():
    current_day = Day16
    day_label = 'Day16'
            
    fname = 'Input01.txt'
    v1, v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==46, day_label+", Part 1 Failed, Input: "+fname
    assert v2==51, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==8125, day_label+", Part 1 Failed, Input: "+fname
    assert v2==8489, day_label+", Part 2 Failed, Input: "+fname

def Day17_test():
    current_day = Day17
    day_label = 'Day17'
            
    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==102, day_label+", Part 1 Failed, Input: "+fname
    assert v2==94, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==851, day_label+", Part 1 Failed, Input: "+fname
    assert v2==982, day_label+", Part 2 Failed, Input: "+fname

def Day18_test():
    current_day = Day18
    day_label = 'Day18'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==62, day_label+", Part 1 Failed, Input: "+fname
    assert v2==952408144115, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==76387, day_label+", Part 1 Failed, Input: "+fname
    assert v2==250022188522074, day_label+", Part 2 Failed, Input: "+fname

def Day19_test():
    current_day = Day19
    day_label = 'Day19'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==19114, day_label+", Part 1 Failed, Input: "+fname
    assert v2==167409079868000, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==353046, day_label+", Part 1 Failed, Input: "+fname
    assert v2==125355665599537, day_label+", Part 2 Failed, Input: "+fname

def Day20_test():
    current_day = Day20
    day_label = 'Day20'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)

    assert v1==11687500, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==825167435, day_label+", Part 1 Failed, Input: "+fname
    assert v2==225514321828633, day_label+", Part 2 Failed, Input: "+fname

def Day21_test():
    current_day = Day21
    day_label = 'Day21'
    
    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==3743, day_label+", Part 1 Failed, Input: "+fname
    assert v2==618261433219147, day_label+", Part 2 Failed, Input: "+fname

def Day22_test():
    current_day = Day22
    day_label = 'Day22'

    fname = 'Input01.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==5, day_label+", Part 1 Failed, Input: "+fname
    assert v2==7, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1, v2 = current_day.solution(show_result=False, fname=fname)

    assert v1==509, day_label+", Part 1 Failed, Input: "+fname
    assert v2==102770, day_label+", Part 2 Failed, Input: "+fname

def Day23_test():
    current_day = Day23
    day_label = 'Day23'

    fname = 'Input01.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==94, day_label+", Part 1 Failed, Input: "+fname
    assert v2==154, day_label+", Part 2 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02(show_result=False, fname=fname)

    assert v1==2362, day_label+", Part 1 Failed, Input: "+fname
    assert v2==6538, day_label+", Part 2 Failed, Input: "+fname

def Day24_test():
    current_day = Day24
    day_label = 'Day24'

    fname = 'Input02.txt'
    v1 = current_day.solution01(show_result=False, fname=fname)
    v2 = current_day.solution02a(show_result=False, fname=fname)
    v3 = current_day.solution02b(show_result=False, fname=fname)

    assert v1==16727, day_label+", Part 1 Failed, Input: "+fname
    assert v2==606772018765659, day_label+", Part 2 Failed, Input: "+fname
    assert v3==606772018765659, day_label+", Part 2 Failed, Input: "+fname

def Day25_test():
    current_day = Day25
    day_label = 'Day25'

    fname = 'Input01.txt'
    v1 = current_day.solution(show_result=False, fname=fname)

    assert v1==54, day_label+", Part 1 Failed, Input: "+fname

    fname = 'Input02.txt'
    v1 = current_day.solution(show_result=False, fname=fname)

    assert v1==591890, day_label+", Part 1 Failed, Input: "+fname

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
    t0 = time.time()
    print('Running Year 2023 Tests:')
    run_all_tests()
    print('total runtime in seconds: ','%.3f' % (time.time()-t0))
    
    