#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph
from math import gcd

path = currentdir


def solution01():
    # my_list = [3,2,4,1,5]
    # my_list = [3,8,9,1,2,5,4,6,7]
    my_list = [8,5,3,1,9,2,6,4,7]


    val_dict = {}
    for item in my_list:
        val_dict[item]=None

    max_val = max(my_list)
    min_val = min(my_list)

    l = len(my_list)

    num_moves = 100
    current_num = my_list[0]
    start_index = 0

    for count in range(num_moves):
        # print(my_list)
        # print(current_num)
   
        selected_nums = []

        while len(selected_nums)<3:
            start_index+=1
            start_index%=l
            selected_nums.append(my_list[start_index])

        # print(selected_nums)
        destination_num = current_num-1

        while destination_num not in val_dict or destination_num in selected_nums:
            if destination_num<min_val:
                destination_num=max_val
            else:
                destination_num-=1

        new_list = []

        for item in my_list:
            if item==destination_num:
                new_list.append(item)
                new_list+=selected_nums
            elif item not in selected_nums:
                new_list.append(item)

        my_list = new_list

        start_index = my_list.index(current_num)
        start_index+=1
        start_index%=l
        current_num = my_list[start_index]

    str_out = ''

    indexA = my_list.index(1)

    for i in range(l-1):
        indexA+=1
        indexA%=l

        str_out+=str(my_list[indexA])

    print(str_out)
    

def solution02():
    
    # my_list = [3,2,4,1,5]
    # my_list = [3,8,9,1,2,5,4,6,7]
    my_list = [8,5,3,1,9,2,6,4,7]

    numel = 10**6
    num_moves = 10**7
    # num_moves = 10

    right_neighbor_dict = {}
    left_neighbor_dict = {}

    fill_num = max(my_list)+1

    for i in range(0,len(my_list)-1):
        right_neighbor_dict[my_list[i]]=my_list[i+1]
    right_neighbor_dict[my_list[-1]]=fill_num
    right_neighbor_dict[numel] = my_list[0]
    right_neighbor_dict[fill_num] = fill_num+1

    for i in range(1,len(my_list)):
        left_neighbor_dict[my_list[i]]=my_list[i-1]
    left_neighbor_dict[my_list[0]]=numel
    left_neighbor_dict[fill_num] = my_list[-1]
    left_neighbor_dict[numel] = numel-1

    for i in range(fill_num+1,numel):
        right_neighbor_dict[i]=i+1
        left_neighbor_dict[i]=i-1

    max_val = numel
    min_val = 1
        
    current_num = my_list[0]

    for count in range(num_moves):
        selected_nums = []

        left_num = current_num
        right_num = right_neighbor_dict[current_num]

        while len(selected_nums)<3:
            selected_nums.append(right_num)
            right_num = right_neighbor_dict[right_num]

        right_neighbor_dict[left_num]=right_num
        left_neighbor_dict[right_num]=left_num

        destination_num = current_num-1

        while destination_num<min_val or max_val<destination_num or destination_num in selected_nums:
            if destination_num<min_val:
                destination_num=max_val
            else:
                destination_num-=1

        left_num = destination_num
        right_num = right_neighbor_dict[left_num]

        right_neighbor_dict[left_num]=selected_nums[0]
        left_neighbor_dict[right_num]=selected_nums[-1]

        left_neighbor_dict[selected_nums[0]]=left_num
        right_neighbor_dict[selected_nums[-1]]=right_num

        current_num = right_neighbor_dict[current_num]

    r1 = right_neighbor_dict[1]
    r2 = right_neighbor_dict[r1]

    print(r1*r2)




if __name__ == '__main__':
    solution01()
    solution02()
    

