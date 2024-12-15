#!/usr/bin/env python
import os,sys,inspect

import numpy as np
from re import split
from copy import deepcopy
from functools import cmp_to_key

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

def pad_list(list_in,n=1,item=None):
    return (n*[item])+list_in+(n*[item])

def pad_str(str_in,n=1,item=' '):
    return (n*item)+str_in+(n*item)

def pad_str_grid(grid_in,n=1,item=' '):
    w = len(grid_in[0])

    grid_out = []

    for i in range(n):
        grid_out.append((2*n+w)*item)

    for my_str in grid_in:
        grid_out.append(pad_str(my_str,n=n,item=item))

    for i in range(n):
        grid_out.append((2*n+w)*item)

    return grid_out

def pad_grid(grid_in,n=1,item=None):
    w = len(grid_in[0])

    grid_out = []

    for i in range(n):
        grid_out.append((2*n+w)*[item])

    for my_list in grid_in:
        grid_out.append(pad_list(my_list,n=n,item=item))

    for i in range(n):
        grid_out.append((2*n+w)*[item])

    return grid_out

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

#extracts integers from a file (list of lists)
def parse_extract_ints(path,fname):
    load_name = os.path.join(path,fname)

    with open(load_name) as f:
        block = []
        for line in f.readlines():
            block.append(extract_ints_from_string(line.strip('\n')))

        return block

    return None

#extracts integers from a file, with additional separation when there is a blank line
def parse_extract_ints_split_by_emptylines(path,fname):
    load_name = os.path.join(path,fname)

    list_out = []
    with open(load_name) as f:
        new_item = []
        for line in f.readlines():
            temp = line.strip('\n')

            if temp == '' and len(new_item)>0:
                list_out.append(new_item)
                new_item = []

            elif temp!= '':
                new_item.append(extract_ints_from_string(temp))

        if len(new_item)>0:
            list_out.append(new_item)

        return list_out
    return None

#extracts a list of integers from a string
def extract_ints_from_string(str_in):
    list_out = []

    count1 = 0
    while count1<len(str_in):
        test1 = '0'<=str_in[count1] and str_in[count1]<='9'
        test2 = count1+1<len(str_in) and str_in[count1]=='-' and '0'<=str_in[count1+1] and str_in[count1+1]<='9' 
        if test1 or test2:
            count2 = count1+1
            while count2<len(str_in) and ('0'<=str_in[count2] and str_in[count2]<='9'):
                count2+=1
            list_out.append(int(str_in[count1:count2]))
            count1 = count2
        else:
            count1+=1

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

def grid_diagonals_down_right(mat_in):
    h = len(mat_in)
    w = len(mat_in[0])

    grid_out = []

    for i in range(w-1,0,-1):
        temp = []
        y = 0
        x = i

        while x<w and y<h:
            temp.append(mat_in[y][x])
            x+=1
            y+=1

        grid_out.append(temp)

    for j in range(0,h):
        temp = []
        y = j
        x = 0

        while x<w and y<h:
            temp.append(mat_in[y][x])
            x+=1
            y+=1

        grid_out.append(temp)

    return grid_out

def grid_diagonals_down_left(mat_in):
    h = len(mat_in)
    w = len(mat_in[0])

    grid_out = []

    for i in range(0,w):
        temp = []
        y = 0
        x = i

        while x>=0 and y<h:
            temp.append(mat_in[y][x])
            x-=1
            y+=1

        grid_out.append(temp)

    for j in range(1,h):
        temp = []
        y=j
        x=w-1

        while x>=0 and y<h:
            temp.append(mat_in[y][x])
            x-=1
            y+=1

        grid_out.append(temp)

    return grid_out

def digit_list_to_str(list_in):
    temp_list = list(map(str,list_in))
    return list_to_str(temp_list)

def list_to_str(list_in):
    return ''.join(list_in)

def listlist_to_str_list(list_in):
    list_out = []
    for item in list_in:
        list_out.append(''.join(item))

    return list_out


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

def lexicographic_sort(list_in):
    return sorted(list_in, key=cmp_to_key(lambda x,y: lexicographic_comparison(x,y)))

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

def manhattan_distance(coord1,coord2):
    dist = 0
    for i in range(min(len(coord1),len(coord2))):
        dist+=abs(coord2[i]-coord1[i])
    return dist

#Rotates grid counterclockwise rotation_num number of times
#assuming the grid is a list of lists
#first index goes from top to bottom
#second index goes from left to right
#
#From python documentation
#zip()
#Make an iterator that aggregates elements from each of the iterables.
# zip('ABCD', 'xy') --> Ax By
#
#Very Useful Explanation I found on Stack Overflow
#https://stackoverflow.com/questions/6473679/transpose-list-of-lists
#There are two important things to understand here:
#The signature of zip: zip(*iterables) This means zip expects an arbitrary 
#number of arguments each of which must be iterable. 
#E.g. zip([1, 2], [3, 4], [5, 6])
#
#Unpacked argument lists: Given a sequence of arguments args, 
#f(*args) will call f such that each element in args is a 
#separate positional argument of f. 
#Given l = [[1, 2, 3], [4, 5, 6], [7, 8, 9]], 
#zip(*l) would be equivalent to zip([1, 2, 3], [4, 5, 6], [7, 8, 9]).
def rotate_grid(grid_in,rotation_num):

    result = deepcopy(grid_in)

    if rotation_num%4==1:
        #transpose
        result = list(map(list, zip(*result)))

        #then reverse (from top to bottom)
        result.reverse()

    if rotation_num%4==2:
        #reverse horizontally
        for item in result:
            item.reverse()

        #then reverse vertically
        result.reverse()

    if rotation_num%4==3:
        #reverse (from top to bottom)
        result.reverse()

        #then transpose
        result = list(map(list, zip(*result)))
        

    return result

def int_to_digit_list(n):
    
    if n == 0: return [0]
        
    list_out = []

    while n>0:
        list_out.append(n%10)
        n//=10

    list_out.reverse()
    return list_out

def digit_list_to_int(list_in):
    n = 0

    for item in list_in: n = 10*n+item

    return n