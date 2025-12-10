#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import heapq as hq
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap, LinkedList, UnionFind
from math import gcd, lcm
from collections import deque
from functools import cmp_to_key

path = currentdir

def str_to_list(str_in):
    temp_list = str_in[1:len(str_in)-1].split(',')
    int_list = []

    for item in temp_list:
        int_list.append(int(item))

    return int_list

def parse_indicators(str_in):
    bool_val = 0

    for i in range(1,len(str_in)-1):
        bool_val+=(str_in[i]=='#')<<(i-1)

    return bool_val

def parse_button1(list_in):
    button_val = 0

    for i in list_in:
        button_val+=1<<i

    return button_val

def parse_button2(list_in,joltage):
    button_list = [0]*len(joltage)

    for i in list_in:
        button_list[i] = 1

    return button_list

def compute_num_presses1(target, wiring):
    dist_dict = {0:0}

    todo_queue = deque()
    todo_queue.append([0,0])


    while len(todo_queue)>0:
        current_item = todo_queue.popleft()

        current_state = current_item[0]
        current_steps = current_item[1]

        for button in wiring:
            next_state = current_state^button
            next_steps = current_steps+1

            if next_state==target:
                return next_steps

            if next_state not in dist_dict:
                dist_dict[next_state] = next_steps
                todo_queue.append([next_state,next_steps])

    return np.inf

def solve_constraints(target,press_list,wiring1,wiring2):
    diff = target-np.dot(wiring2,press_list)
    temp1 = np.linalg.solve(wiring1,diff)

    temp2 = []
    for item in temp1:
        temp2.append(int(round(item)))

    q = np.array(temp2)

    diff = diff-np.dot(wiring1,q)

    if np.sum(abs(diff))==0 and min(q)>=0:
        return sum(q)+sum(press_list)

    return np.inf

def compute_num_presses_recursive(target,press_list,wiring1,wiring2,i=0):

    diff = target
    if len(wiring2)>0:
        diff=target-np.dot(wiring2,press_list)

    if min(diff)<0:
        return True, np.inf

    if i==len(press_list):
        return False, solve_constraints(target,press_list,wiring1,wiring2)

    min_val = np.inf

    press_list[i] = 0

    while True:
        temp_bool, temp_min = compute_num_presses_recursive(target,press_list,wiring1,wiring2,i+1)

        min_val = min(min_val,temp_min)

        if temp_bool:
            break

        press_list[i]+=1

    press_list[i]=0

    return False, min_val

#Given arbitrary linear system A*X=B (where A only contains integers)
#extracts simplified system A1*X1 + A2*X2 = B_simple
#by doing the following two things
#1. Removing any linearly dependent rows of A (i.e. linearly dependent equations in the system)
#2. Permuting columns of A so that A1 consists of the largest set of linearly indendendent columns
#   and A2 consists of the remaining columns
def simplify_linear_system(A, B):
    #extract dimensions of A
    num_rows, num_cols = len(A), len(A[0])
    
    #used to store intermediate values of A
    #as we work through the row reduction
    A_echelon = np.array(A)

    #keep track of which rows and columns of A
    #are linearly independent
    independent_row_index_set = set() 
    independent_col_index_set = set()

    #iterate through each column of A
    for i in range(num_cols):
        #we begin by identifying a row (k) with the following properties:
        #1. row k has not yet been added to the set of linearly independent rows
        #2. A_echelon[k][i]! = 0 (the pivot of row k is in column i)
        k = None
        for j in range(num_rows):
            if j not in independent_row_index_set and A_echelon[j][i]!=0:
                k = j
                break

        #if we can't find a row that satisfies these two properties
        #it means that column i is not linearly independent with columns currently
        #in the indendpendent column set, so we will skip this column
        if k is None:
            continue

        #if we successfully found a row, that means that row k and column i
        #are linearly independent with the rows/columns already in the sets
        #so we can add them to the set
        independent_col_index_set.add(i)
        independent_row_index_set.add(k)

        #the final step is to reduce the remaining rows of A
        #since our goal is just to identify the linearly independent rows/columns
        #we will perform our reduction in a way that perserves the integrality
        #of the elements of A_echelon (keep them all integers)
        for j in range(num_rows):
            if j not in independent_row_index_set and A_echelon[j][i]!=0:
                A_echelon[j] = (A_echelon[j]*A_echelon[k][i]
                               -A_echelon[k]*A_echelon[j][i])


    #now that we have identified which rows/columns are linearly independent
    #we can simplify A and B

    #we start by eliminating any rows of A 
    #that are not in the linearly independent set
    #as well as the corresponding elements of B
    independent_rows = []
    B_simplified = []

    for i in independent_row_index_set:
        independent_rows.append(A[i])
        B_simplified.append(B[i])

    A_temp = np.vstack(independent_rows).transpose()
    B_simplified = np.array(B_simplified)

    #the final step is to split A into two matrices,
    #A1, which contains the linearly independent columns, and
    #A2, which contains the other columns
    independent_cols, extra_cols = [], []

    for i in range(num_cols):
        if i in independent_col_index_set:
            independent_cols.append(A_temp[i])
        else:
            extra_cols.append(A_temp[i])

    A1_simplified = np.vstack(independent_cols).transpose()

    A2_simplified = []
    if len(extra_cols)>0:
        A2_simplified = np.vstack(extra_cols).transpose()

    return A1_simplified, A2_simplified, B_simplified


def compute_num_presses2(target, wiring):
    target = np.array(target)
    wiring = np.array(wiring)
    wiring = np.transpose(wiring)
    wiring1, wiring2, target = simplify_linear_system(wiring, target)

    press_list = []

    if len(wiring2)>0:
        press_list = np.array([0]*len(wiring2[1]))

    temp_bool, temp_min = compute_num_presses_recursive(target,press_list,wiring1,wiring2,i=0)
    
    return temp_min


def parse_input01(fname):
    data = bh.parse_strings(path,fname,delimiters = [' '],type_lookup = None, allInt = False, allFloat = False)

    indicator_mat = []
    joltage_mat = []
    wiring_basic = []
    wiring_joltage = []
    for item in data:
        indicator_mat.append(parse_indicators(item[0]))
        joltage_mat.append(str_to_list(item[-1]))

        wiring_temp1 = []
        wiring_temp2 = []
        for i in range(1,len(item)-1):
            button_list = str_to_list(item[i])
            wiring_temp1.append(parse_button1(button_list))
            wiring_temp2.append(parse_button2(button_list,joltage_mat[-1]))

        wiring_basic.append(wiring_temp1)
        wiring_joltage.append(wiring_temp2)

    return indicator_mat, wiring_basic, wiring_joltage, joltage_mat

def solution01(show_result=True, fname='Input02.txt'):
    indicator_mat, wiring_basic, wiring_joltage, joltage_mat = parse_input01(fname)
    
    total = 0

    for i in range(len(indicator_mat)):
        total+=compute_num_presses1(indicator_mat[i],wiring_basic[i])

    if show_result:
        print(total)
    return total


def solution02(show_result=True, fname='Input02.txt'):
    indicator_mat, wiring_basic, wiring_joltage, joltage_mat = parse_input01(fname)

    total = 0
    for i in range(len(indicator_mat)):
        total+=compute_num_presses2(joltage_mat[i],wiring_joltage[i])

    if show_result:
        print(total)
    return total

if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    # print('runtime in seconds: ','%.3f' % (time.time()-t0))
    

