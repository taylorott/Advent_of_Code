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
from functools import cmp_to_key

path = currentdir

def parse_input01(fname):
    return bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)


#converts a hand string to a sorted list of card frequencies
#if there are jokers, the frequency of jokers is combined with the highest frequency value in the list
def hand_to_freq_list(hand_str,with_jokers=False):

    #build a frequency table of card values in the hand
    freq_table = {}

    for card_char in hand_str:
        if card_char in freq_table:
            freq_table[card_char]+=1
        else:
            freq_table[card_char]=1

    NJ=0 #number of jokers

    #if we are playing with jokers and there are jokers in the hand
    if with_jokers and 'J' in freq_table:
        #set NJ to number of jokers
        NJ=freq_table['J']

        #set frequency of jokers in table to 0
        freq_table['J']=0

    #build a list of card frequencies, sorted in reverse order
    freq_list = []
    for item in freq_table:
        freq_list.append(freq_table[item])
    freq_list.sort(reverse=True)

    #add the number of jokers to the highest frequency in the sorted list
    freq_list[0]+=NJ

    while freq_list[-1]==0:
        freq_list.pop(-1)

    return freq_list

card_to_int = {'A':14,'K':13,'Q':12,'J':11,'T':10,'9':9,'8':8,'7':7,'6':6,'5':5,'4':4,'3':3,'2':2}

#compares hand1 to hand2
#hand1>hand2  : 1
#hand1==hand2 : 0
#hand1<hand2  :-1
def compare_hands(hand1,hand2,with_jokers=False):

    #compare hands by type of hand
    freq_list1 = hand_to_freq_list(hand1,with_jokers)
    freq_list2 = hand_to_freq_list(hand2,with_jokers)

    compare_out = bh.lexicographic_comparison(freq_list1,freq_list2)
    if compare_out!=0:
        return compare_out

    #apply the tiebreaker

    #compare the cards of each hand from left to right
    for i in range(len(hand1)):

        #evalue the value of the cards of each hand
        card_val1 = card_to_int[hand1[i]]
        card_val2 = card_to_int[hand2[i]]

        #if jokers are being applied, set value of joker to 0
        if with_jokers and hand1[i]=='J':
            card_val1=0

        if with_jokers and hand2[i]=='J':
            card_val2=0

        #compare cards
        if card_val1>card_val2:
            return 1
        if card_val1<card_val2:
            return -1

    #if hands are the same, return 0
    return 0

#once the hands have been sorted, evaluate the total score of the bids
def eval_score(sorted_hands):
    total = 0
    for i in range(len(sorted_hands)):
        total+=(i+1)*int(sorted_hands[i][1])
    return total

def solution01(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    sorted_hands = sorted(data, key=cmp_to_key(lambda x,y: compare_hands(x[0],y[0],with_jokers=False)))
    result = eval_score(sorted_hands)

    if show_result: print(result)

    return result

def solution02(show_result=True, fname='Input02.txt'):
    data = parse_input01(fname)
    sorted_hands = sorted(data, key=cmp_to_key(lambda x,y: compare_hands(x[0],y[0],with_jokers=True)))
    result = eval_score(sorted_hands)

    if show_result: print(result)

    return result


if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

