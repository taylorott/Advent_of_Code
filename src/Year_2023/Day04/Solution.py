#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque 

path = currentdir

def parse_input01(fname):
    data = None
    
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_digit_grid(path,fname)
    # data = bh.parse_char_grid(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)
    data = bh.parse_strings(path,fname,delimiters = [' ',':','Card'],type_lookup = None, allInt = False, allFloat = False)

    num_cards = len(data)

    card_dict = {}
    card_dict['num_cards']=num_cards

    for card in data:
        card_num = int(card[0])

        winning_numbers = set()
        my_numbers = set()

        count = 1

        while count<len(card) and card[count]!='|':
            winning_numbers.add(int(card[count]))
            count+=1

        count+=1
        while count<len(card):
            my_numbers.add(int(card[count]))
            count+=1

        card_dict[card_num]=[winning_numbers,my_numbers]


    return card_dict

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    card_dict = parse_input01(fname)
    num_cards = card_dict['num_cards']

    total = 0
    for card in range(1,num_cards+1):
        
        winning_numbers = card_dict[card][0]
        my_numbers = card_dict[card][1]
        num_matches = 0

        for candidate in my_numbers:
            if candidate in winning_numbers:
                num_matches+=1

        if num_matches>0:
            total+=1<<(num_matches-1)

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    
    card_dict = parse_input01(fname)
    num_cards = card_dict['num_cards']

    card_quantity_list = [1]*(num_cards+1)
    card_quantity_list[0] = 0

    total = 0
    for card in range(1,num_cards+1):
        
        winning_numbers = card_dict[card][0]
        my_numbers = card_dict[card][1]
        num_matches = 0

        for candidate in my_numbers:
            if candidate in winning_numbers:
                num_matches+=1

        for i in range(card+1,min(num_cards+1,card+1+num_matches)):
            card_quantity_list[i]+=card_quantity_list[card]
        total+=card_quantity_list[card]

    print(total)


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

