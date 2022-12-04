#!/usr/bin/env python
import os,sys,inspect

import numpy as np
from re import split

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

#parses a file that needs specific post-processing to interpret
def parse_strings(path,fname,delimiters = None,type_lookup = None, allInt = False, allFloat = False):
    list_out = []
    load_name = os.path.join(path,fname)

    pattern = None
    if delimiters is not None:
        if type(delimiters) is str:
            pattern = r'|'.join([delimiters])

        elif type(delimiters) is list:
            pattern = r'|'.join(delimiters)

    with open(load_name) as f:
        for line in f.readlines():

            temp = line.strip('\n')
            if delimiters is None:
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
    return None

#parses a file that is just a single column of items that are sometimes separated by empty lines
#returns as a list of lists where the outer list corresponds to a list of blocks 
#where each block is separated by an empty line
#and the inner list corresponds to a list of each item in a given block
def parse_split_by_emptylines(path,fname,allInt = False, allFloat = False):
    list_out = []
    load_name = os.path.join(path,fname)

    with open(load_name) as f:
        new_item = []
        for line in f.readlines():
            temp = line.strip('\n')

            if temp == '' and len(new_item)>0:
                list_out.append(new_item)
                new_item = []

            elif temp!= '':
                if allInt:
                    new_item.append(int(temp))
                elif allFloat:
                    new_item.append(float(temp))
                else:
                    new_item.append(temp)

        if len(new_item)>0:
            list_out.append(new_item)

        return list_out
    return None

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
