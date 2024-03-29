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

def parse_input01(fname):
    # num_list = bh.parse_num_column(path,fname)
    # data = bh.parse_split_by_emptylines(path,fname)
    data = bh.parse_strings(path,fname)

    mat_out = []

    for line in data:
        temp = line.replace('#','1')
        temp = temp.replace('.','0')
        split_list = list(temp)

        row = []
        for item in split_list:
            row.append(int(item))

        mat_out.append(row)

    return [mat_out]

def update_mat01(mat_in):
    h = len(mat_in)
    v = len(mat_in[0])
    l = len(mat_in[0][0])

    h_new = h+2
    v_new = v+2
    l_new = l+2

    mat_out = []

    for i in range(h_new):
        mat_out.append([])
        for j in range(v_new):
            mat_out[i].append([0]*l_new)

    num_active = 0
    for i in range(h_new):
        for j in range(v_new):
            for k in range(l_new):
                num_adj = 0
                for i_adj in range(i-2,i+1):
                    for j_adj in range(j-2,j+1):
                        for k_adj in range(k-2,k+1):
                            if (0<=i_adj and i_adj<h and 
                                0<=j_adj and j_adj<v and
                                0<=k_adj and k_adj<l and
                                (i_adj!=i-1 or j_adj!=j-1 or k_adj!=k-1) and
                                mat_in[i_adj][j_adj][k_adj]==1):
                                num_adj +=1

                in_bounds = 0<=i-1 and i-1<h and 0<=j-1 and j-1<v and 0<=k-1 and k-1<l
                if (not in_bounds or mat_in[i-1][j-1][k-1]==0) and num_adj == 3:
                    mat_out[i][j][k] = 1
                    num_active+=1
                elif (in_bounds and mat_in[i-1][j-1][k-1]==1) and (num_adj == 2 or num_adj == 3):
                    mat_out[i][j][k] = 1
                    num_active+=1

    #         print(mat_out[i][j])
    #     print(' ')

    # print('new mat!')
    # print(' ')
    return mat_out,num_active

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    current_mat = parse_input01(fname)

    for i in range(6):
        current_mat,num_active = update_mat01(current_mat)

    print(num_active)


def update_mat02(mat_in):
    h = len(mat_in)
    v = len(mat_in[0])
    l = len(mat_in[0][0])
    q = len(mat_in[0][0][0])

    h_new = h+2
    v_new = v+2
    l_new = l+2
    q_new = q+2

    mat_out = []

    for i in range(h_new):
        mat_out.append([])
        for j in range(v_new):
            mat_out[i].append([])
            for k in range(l_new):
                mat_out[i][j].append([0]*q_new)

    num_active = 0
    for i in range(h_new):
        for j in range(v_new):
            for k in range(l_new):
                for n in range(q_new):
                    num_adj = 0
                    for i_adj in range(i-2,i+1):
                        for j_adj in range(j-2,j+1):
                            for k_adj in range(k-2,k+1):
                                for n_adj in range(n-2,n+1):
                                    if (0<=i_adj and i_adj<h and 
                                        0<=j_adj and j_adj<v and
                                        0<=k_adj and k_adj<l and
                                        0<=n_adj and n_adj<q and
                                        (i_adj!=i-1 or j_adj!=j-1 or k_adj!=k-1 or n_adj!=n-1) and
                                        mat_in[i_adj][j_adj][k_adj][n_adj]==1):
                                        num_adj +=1

                    in_bounds = 0<=i-1 and i-1<h and 0<=j-1 and j-1<v and 0<=k-1 and k-1<l and 0<=n-1 and n-1<q
                    if (not in_bounds or mat_in[i-1][j-1][k-1][n-1]==0) and num_adj == 3:
                        mat_out[i][j][k][n] = 1
                        num_active+=1
                    elif (in_bounds and mat_in[i-1][j-1][k-1][n-1]==1) and (num_adj == 2 or num_adj == 3):
                        mat_out[i][j][k][n] = 1
                        num_active+=1


    return mat_out,num_active

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    current_mat = [parse_input01(fname)]

    for i in range(6):
        current_mat,num_active = update_mat02(current_mat)

    print(num_active)

if __name__ == '__main__':
    solution01()
    solution02()
    

