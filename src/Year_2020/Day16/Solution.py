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

def parse_ticket01(fname):
    data = bh.parse_split_by_emptylines(path,fname)

    range_dict = {}
    possible_values_dict = {}
    for line in data[0]:
        split_str0 = line.split(': ')
        temp = split_str0[1].replace('or',' ')
        temp = temp.replace('-',' ')

        split_str1 = temp.split(' ')
        range_dict[split_str0[0]]={}

        a = int(split_str1[0])
        b = int(split_str1[1])
        c = int(split_str1[4])
        d = int(split_str1[5])

        for i in range(a,b+1):
            range_dict[split_str0[0]][i] = None
            possible_values_dict[i]=None
        for i in range(c,d+1):
            range_dict[split_str0[0]][i] = None
            possible_values_dict[i]=None


    data[2]=data[2][1:]
    ticket_list = []
    for line in data[2]:
        item_str_list = line.split(',')
        ticket_items = []
        for item in item_str_list:
            ticket_items.append(int(item))
        ticket_list.append(ticket_items)

    return range_dict,possible_values_dict,ticket_list

def parse_ticket02(fname):
    data = bh.parse_split_by_emptylines(path,fname)
    
    item_str_list = data[1][1].split(',')
    my_ticket = []
    for item in item_str_list:
        my_ticket.append(int(item))
    
    return my_ticket


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    range_dict,possible_values_dict,ticket_list = parse_ticket01(fname)

    total = 0
    for ticket in ticket_list:
        for val in ticket:
            if val not in possible_values_dict:
                total+=val
    print(total)

def solution02():
    # fname = 'Input03.txt'
    fname = 'Input02.txt'


    range_dict,possible_values_dict,ticket_list = parse_ticket01(fname)

    valid_ticket_list = []
    for ticket in ticket_list:
        is_valid = True
        for val in ticket:
            if val not in possible_values_dict:
                is_valid = False
                break
        if is_valid:
            valid_ticket_list.append(ticket)

    ticket_list = valid_ticket_list

    my_ticket = parse_ticket02(fname)

    reverse_lookup = {}
    fields = range_dict.keys()

    for key in fields:
        for num in range_dict[key].keys():
            if num not in reverse_lookup:
                reverse_lookup[num] = []

            reverse_lookup[num].append(key)

    possible_fields = []
    num_possibilities = []
    for i in range(len(ticket_list[0])):
        current_set = set(reverse_lookup[ticket_list[0][i]])
        for j in range(len(ticket_list)):
            val = ticket_list[j][i]
            current_set = current_set&set(reverse_lookup[val])
        possible_fields.append(current_set)
        num_possibilities.append(len(current_set))
        
    while max(num_possibilities)>1:
        for i in range(len(possible_fields)):
            if num_possibilities[i]==1:
                for j in range(len(possible_fields)):
                    if i!=j:
                        possible_fields[j]-=possible_fields[i]
                        num_possibilities[j] = len(possible_fields[j])

    field_lookup = {}
    for i in range(len(possible_fields)):
        field_lookup[list(possible_fields[i])[0]]=i

    total = 1

    for key in field_lookup.keys():
        if key[0:9] =='departure':
            total*=my_ticket[field_lookup[key]]

    print(total)

if __name__ == '__main__':
    solution01()
    solution02()
    

