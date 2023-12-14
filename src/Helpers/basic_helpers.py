#!/usr/bin/env python
import os,sys,inspect

import numpy as np
from re import split
from copy import deepcopy

#parses a file that is just a single column of numbers
#returns as a list
def parse_num_column(path,fname,isInt=True):
    list_out = []
    load_name = os.path.join(path,fname)
    with open(load_name) as f:
        for line in f.readlines():
            if isInt:
                list_out.append(int(line.strip('\n')))
            else:       
                list_out.append(line.strip('\n'))
        f.close()
        return list_out
    return None

#parses a file that is a matrix of digits (not comma seperated)
def parse_digit_grid(path,fname):
    return parse_grid(path,fname,allInt=True)

#parses a file that is a matrix of characters (not comma seperated)
def parse_char_grid(path,fname):
    return parse_grid(path,fname,allInt=False)

def parse_grid(path,fname,allInt=False):
    load_name = os.path.join(path,fname)

    with open(load_name) as f:
        block = []
        for line in f.readlines():
            block.append(line.strip('\n'))

        return block_to_grid(block,allInt=allInt)
    return None

def block_to_grid(block_in,allInt=False):
    list_out = []
    for line in block_in:
        row = []
        for my_char in line:
            if allInt:
                row.append(int(my_char))
            else:
                row.append(my_char)
        list_out.append(row)
    return list_out


#parses a file that needs specific post-processing to interpret
def parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False):
    load_name = os.path.join(path,fname)

    with open(load_name) as f:
        block = []
        for line in f.readlines():
            block.append(line.strip('\n'))

        return parse_block(block,delimiters,type_lookup, allInt, allFloat)

    return None

#parses a file that is just a single column of items that are sometimes separated by empty lines
#returns as a list of lists where the outer list corresponds to a list of blocks 
#where each block is separated by an empty line
#and the inner list corresponds to a list of each item in a given block
def parse_split_by_emptylines(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False):
    load_name = os.path.join(path,fname)

    list_out = []
    with open(load_name) as f:
        new_item = []
        for line in f.readlines():
            temp = line.strip('\n')

            if temp == '' and len(new_item)>0:
                list_out.append(parse_block(new_item,delimiters,type_lookup, allInt, allFloat))
                new_item = []

            elif temp!= '':
                new_item.append(temp)

        if len(new_item)>0:
            list_out.append(parse_block(new_item,delimiters,type_lookup, allInt, allFloat))

        return list_out
    return None

def parse_block(block,delimiters = None,type_lookup = None, allInt = False, allFloat = False):
    list_out = []

    pattern = None
    if delimiters is not None and len(delimiters)>0:
        if type(delimiters) is str:
            pattern = r'|'.join([delimiters])

        elif type(delimiters) is list:
            pattern = r'|'.join(delimiters)

    for line in block:
        temp = line.strip('\n')
        if delimiters is None or len(delimiters)==0:
            list_out.append(temp)
        else:
            new_item = []
            split_list = split(pattern, temp)

            for string in split_list:
                if string != '':
                    new_item.append(string)

            for i in range(len(new_item)):
                if allInt:
                    new_item[i] = int(new_item[i])
                elif allFloat:
                    new_item[i] = float(new_item[i])
                elif type_lookup is not None:
                    if type(type_lookup) is list:
                        if type_lookup[i]=='int':
                            new_item[i] = int(new_item[i])
                        elif type_lookup[i]=='float':
                            new_item[i] = float(new_item[i])
                    elif type(type_lookup) is dict:
                        if i in type_lookup:
                            if type_lookup[i]=='int':
                                new_item[i] = int(new_item[i])
                            elif type_lookup[i]=='float':
                                new_item[i] = float(new_item[i])
            list_out.append(new_item)

    return list_out

#converts a list of dictionary formatted strings into a dictionary
#best to just give an example:
#the following list:
#['pid:937877382 eyr:2029','ecl:amb hgt:187cm iyr:2019','byr:1933 hcl:#888785']
#becomes the following dictionary:
#{'pid':'937877382' , 'eyr':'2029' , 'ecl':'amb' , 'hgt':'187cm' , 'iyr':'2019' , 'byr':'1933' , 'hcl':'#888785'}
def convert_strings_to_dict(data):
    data_dict = {}

    for line in data:
        #split items by empty space or commas
        str_list = split(r'[ ,]',line)

        for key_val_str in str_list:
            if key_val_str!='':
                key_val_pair = key_val_str.split(':')
                data_dict[key_val_pair[0]]=key_val_pair[1]

    return data_dict


def build_char_freq_table(str_in):
    dict_out = {}

    for my_char in str_in:
        if my_char in dict_out:
            dict_out[my_char]+=1
        else:
            dict_out[my_char]=1

    return dict_out

def build_freq_table(list_in):
    dict_out = {}

    for item in list_in:
        if item in dict_out:
            dict_out[item]+=1
        else:
            dict_out[item]=1

    return dict_out

def print_char_matrix(mat_in,transpose = False,reverse_vert=False,reverse_horz=False):
    i_list = []
    j_list = []

    l0 = len(mat_in)
    l1 = len(mat_in[0])

    if not reverse_vert:
        for i in range(l0):
            i_list.append(i)
    else:
        for i in range(l0-1,-1,-1):
            i_list.append(i)

    if not reverse_horz:
        for j in range(l1):
            j_list.append(j)
    else:
        for j in range(l1-1,-1,-1):
            j_list.append(j)

    if not transpose:
        for i in i_list:
            line = ''
            for j in j_list:
                line+=mat_in[i][j]
            print(line)
    else:
        for j in j_list:
            line = ''
            for i in i_list:
                line+=mat_in[i][j]
            print(line)

def lexicographic_comparison(key1,key2):
    for i in range(min(len(key1),len(key2))):
        if key1[i]>key2[i]:
            return 1
        if key1[i]<key2[i]:
            return -1

    if len(key1)>len(key2):
        return 1
    if len(key1)<len(key2):
        return -1

    return 0

def rotate_grid(grid_in,rotation_num):
    if rotation_num%4==0:
        return deepcopy(grid_in)

    if rotation_num%4==1:
        return deepcopy(reversed(list(map(list, zip(*grid_in)))))

    if rotation_num%4==2:
        temp = list(map(list, zip(*reversed(grid_in))))
        return deepcopy(list(map(list, zip(*reversed(temp)))))

    if rotation_num%4==3:
        return deepcopy(list(map(list, zip(*reversed(grid_in)))))