#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh

path = currentdir

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    # p_len = 5
    p_len = 25

    freq_table = {}

    for i in range(p_len):
        if num_list[i] in freq_table:
            freq_table[num_list[i]]+=1
        else:
            freq_table[num_list[i]]=1

    for i in range(p_len,len(num_list)):
        is_valid = False
        for j in range(i-p_len,i):
            diff_val = num_list[i]-num_list[j] 
            if ((diff_val!=num_list[j] and diff_val in freq_table and freq_table[diff_val]>0) or
                (diff_val==num_list[j] and diff_val in freq_table and freq_table[diff_val]>1)):
                is_valid = True
                break

        if not is_valid:
            print(num_list[i])
            break

        if num_list[i] in freq_table:
            freq_table[num_list[i]]+=1
        else:
            freq_table[num_list[i]]=1

        freq_table[num_list[i-p_len]]-=1

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    # p_len = 5
    p_len = 25

    freq_table = {}

    invalid_num = None

    for i in range(p_len):
        if num_list[i] in freq_table:
            freq_table[num_list[i]]+=1
        else:
            freq_table[num_list[i]]=1

    for i in range(p_len,len(num_list)):
        is_valid = False
        for j in range(i-p_len,i):
            diff_val = num_list[i]-num_list[j] 
            if ((diff_val!=num_list[j] and diff_val in freq_table and freq_table[diff_val]>0) or
                (diff_val==num_list[j] and diff_val in freq_table and freq_table[diff_val]>1)):
                is_valid = True
                break

        if not is_valid:
            invalid_num = num_list[i]
            break

        if num_list[i] in freq_table:
            freq_table[num_list[i]]+=1
        else:
            freq_table[num_list[i]]=1

        freq_table[num_list[i-p_len]]-=1

    cum_sum_dict = {0:0}
    total = 0
    for i in range(len(num_list)):
        total+=num_list[i]

        if total-invalid_num in cum_sum_dict:
            min_index = cum_sum_dict[total-invalid_num]
            max_index = i+1

            if min_index!=max_index:
                print(min(num_list[min_index:max_index])+max(num_list[min_index:max_index]))
                break

        cum_sum_dict[total]=i+1




if __name__ == '__main__':
    solution01()
    solution02()
    

