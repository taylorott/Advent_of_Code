#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Digraph

path = currentdir

def update_system_state01(mat_in):
    height = len(mat_in)
    width = len(mat_in[0])

    mat_out = []
    for i in range(height):
        mat_out.append(list(mat_in[i]))

    did_change = False
    num_occ_total = 0
    for i in range(height):
        for j in range(width):
            if mat_in[i][j]!='.':
                num_occ_adj = 0
                for i_adj in range(i-1,i+2):
                    for j_adj in range(j-1,j+2):
                        if (0 <= i_adj and i_adj < height and 0 <= j_adj and j_adj < width) and (i_adj!=i or j_adj!=j) and mat_in[i_adj][j_adj]=='#':
                            num_occ_adj+=1
                if mat_in[i][j]=='L' and num_occ_adj==0:
                    mat_out[i][j] = '#'
                    did_change = True
                if mat_in[i][j]=='#' and num_occ_adj>=4:
                    mat_out[i][j] = 'L'
                    did_change = True

                if mat_out[i][j] == '#':
                    num_occ_total+=1

    return mat_out,did_change,num_occ_total

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    did_change = True
    num_occ_total = 0
    while did_change:
        data,did_change,num_occ_total = update_system_state01(data)

    # for line in data:
        # print(''.join(line))
    print(num_occ_total)

def update_system_state02(mat_in,adj_dict):
    height = len(mat_in)
    width = len(mat_in[0])

    mat_out = []
    for i in range(height):
        mat_out.append(list(mat_in[i]))

    did_change = False
    num_occ_total = 0
    for i in range(height):
        for j in range(width):
            if mat_in[i][j]!='.':
                num_occ_adj = 0
                for coord_pair in adj_dict[(i,j)]:
                    if mat_in[coord_pair[0]][coord_pair[1]]=='#':
                        num_occ_adj+=1

                if mat_in[i][j]=='L' and num_occ_adj==0:
                    mat_out[i][j] = '#'
                    did_change = True
                if mat_in[i][j]=='#' and num_occ_adj>=5:
                    mat_out[i][j] = 'L'
                    did_change = True

                if mat_out[i][j] == '#':
                    num_occ_total+=1

    return mat_out,did_change,num_occ_total

def build_adj_dict(mat_in):
    adj_dict = {}

    height = len(mat_in)
    width = len(mat_in[0])

    for i in range(height):
        for j in range(width):
            if mat_in[i][j]!='.':
                adj_dict[(i,j)]=[]

                for delta_i in range(-1,2):
                    for delta_j in range(-1,2):
                        if delta_i!=0 or delta_j!=0:
                            i_adj = i+delta_i
                            j_adj = j+delta_j

                            while 0 <= i_adj and i_adj < height and 0 <= j_adj and j_adj < width:
                                if mat_in[i_adj][j_adj]=='L':
                                    adj_dict[(i,j)].append((i_adj,j_adj))
                                    break

                                i_adj+=delta_i
                                j_adj+=delta_j

    return adj_dict

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = bh.parse_strings(path,fname)
    adj_dict = build_adj_dict(data)

    did_change = True
    num_occ_total = 0
    while did_change:
        data,did_change,num_occ_total = update_system_state02(data,adj_dict)

    # for line in data:
        # print(''.join(line))
    print(num_occ_total)

if __name__ == '__main__':
    solution01()
    solution02()
    

