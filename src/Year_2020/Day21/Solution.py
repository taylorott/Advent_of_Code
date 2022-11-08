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
    data = bh.parse_strings(path,fname,[' ',',',r'\(',r'\)'])


    ingredients_out = []
    allergies_out = []
    for line in data:
        list1 = []
        list2 = []
        contain_bool = False
        for item in line:
            if item=='contains':
                contain_bool=True
            elif contain_bool:
                list2.append(item)
            else:
                list1.append(item)

        ingredients_out.append(list1)
        allergies_out.append(list2)

    return ingredients_out,allergies_out

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    ingredients_out,allergies_out = parse_input01(fname)

    ingredient_freq_table = {}

    for ing_list in ingredients_out:
        for item in ing_list:
            if item in ingredient_freq_table:
                ingredient_freq_table[item]+=1
            else:
                ingredient_freq_table[item]=1

    allergy_dict = {}
    
    a_list_key = []
    a_list_val = []
    a_list_size = []

    ingredient_union = set([])

    for i in range(len(allergies_out)):
        for allergy in allergies_out[i]:
            my_set = set(ingredients_out[i])
            ingredient_union|=my_set
            if allergy in allergy_dict:
                allergy_dict[allergy]&=my_set
            else:
                allergy_dict[allergy]=my_set

    possible_ingredient_union = set([])

    for allergy in allergy_dict.keys():
        possible_ingredient_union|=allergy_dict[allergy]

    non_harmful_indgredients = ingredient_union-possible_ingredient_union

    # print(non_harmful_indgredients)

    total = 0
    for item in non_harmful_indgredients:
        total+=ingredient_freq_table[item]
    print(total)



    for allergy in allergy_dict.keys():
        a_list_key.append(allergy)
        a_list_val.append(allergy_dict[allergy])
        a_list_size.append(len(allergy_dict[allergy]))

    while max(a_list_size)>1:
        for i in range(len(a_list_key)):
            if a_list_size[i]==1:
                for j in range(len(a_list_key)):
                    if j!=i:
                        a_list_val[j]-=a_list_val[i]
                        a_list_size[j]=len(a_list_val[j])

    for i in range(len(a_list_key)):
        allergy_dict[a_list_key[i]]=list(a_list_val[i])[0]

    sorted_keys = list(a_list_key)
    sorted_keys.sort()

    canonical_out = ''

    for key in sorted_keys:
        canonical_out+=','+allergy_dict[key]

    canonical_out = canonical_out[1:]
    print(canonical_out)

def solution02():
    fname = 'Input01.txt'
    # fname = 'Input02.txt'

    # parse_input01(fname)

if __name__ == '__main__':
    solution01()
    solution02()
    

