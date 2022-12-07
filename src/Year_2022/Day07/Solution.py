#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph, frequency_table
from math import gcd, lcm
from collections import deque 

path = currentdir

class MyFolder(object):
    def __init__(self,name,parent_folder=None):
        self.name = name
        self.child_folders = {}
        self.parent_folder = parent_folder
        self.child_files = {}
        self.total_size_files = 0
        self.total_size = 0

    def add_child_folder(self,name):
        if name not in self.child_folders:
            self.child_folders[name] = MyFolder(name,self)

    def add_child_file(self,name,file_size):
        if name not in self.child_files:
            self.child_files[name]=file_size
            self.total_size_files+=file_size

    def eval_total_size(self):
        self.total_size = self.total_size_files

        for dir_name in self.child_folders:
            self.total_size+=self.child_folders[dir_name].eval_total_size()

        return self.total_size

def eval_total_size1(dir_in,total_out = 0):
    if dir_in.total_size<=100000:
        total_out+=dir_in.total_size

    for dir_name in dir_in.child_folders:
        total_out = eval_total_size1(dir_in.child_folders[dir_name],total_out)

    return total_out

def eval_total_size2(dir_in,size_dict = None):
    if size_dict is None:
        size_dict = {}

    size_dict[dir_in.name]=dir_in.total_size
    for dir_name in dir_in.child_folders:
        total_out = eval_total_size2(dir_in.child_folders[dir_name],size_dict)

    return size_dict


def parse_input01(fname):
    # data = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    return data

def build_directory(data):
    root_dir = None
    current_dir = None

    count = 0

    while count<len(data):
        if data[count][0]=='$' and data[count][1]=='cd':
            if data[count][2]=='/':
                if root_dir is None:
                    root_dir = MyFolder('/')

                current_dir = root_dir

            elif data[count][2]=='..':
                if current_dir.parent_folder is not None:
                    current_dir = current_dir.parent_folder
            else:
                dir_name = data[count][2]
                if dir_name not in current_dir.child_folders:
                    current_dir.add_child_folder(dir_name)
                current_dir = current_dir.child_folders[dir_name]
            count+=1

        elif data[count][0]=='$' and data[count][1]=='ls':
            count+=1
            while count<len(data) and data[count][0]!='$':
                if data[count][0]=='dir':
                    current_dir.add_child_folder(data[count][1])
                else:
                    current_dir.add_child_file(data[count][1],int(data[count][0]))
                count+=1

    return root_dir

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    root_dir = build_directory(data)
    

    root_dir.eval_total_size()

    print(eval_total_size1(root_dir))

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    root_dir = build_directory(data)
    
    root_dir.eval_total_size()

    size_dict = eval_total_size2(root_dir)

    min_size = None

    max_space = 70000000
    space_remaining = max_space-size_dict['/']
    need_to_free = 30000000-space_remaining

    for key in size_dict:
        folder_size = size_dict[key]
        if folder_size>=need_to_free:
            if min_size is None or folder_size<min_size:
                min_size=folder_size

    print(min_size)

if __name__ == '__main__':
    solution01()
    solution02()
    

