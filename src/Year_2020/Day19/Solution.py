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
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    ruleset = data[0]
    string_list = data[1]

    rule_dict = {}
    regex_type_dict = {}
    for rule in ruleset:
        splitstr1 = rule.split(': ')

        rule_id = int(splitstr1[0])
        splitstr2 = splitstr1[1].split(' ')

        regex_list = []
        current_regex = []
        regex_type = 'str'
        for item in splitstr2:
            if item=='|':
                regex_type = 'meta'
                regex_list.append(current_regex)
                current_regex = []
            elif item!='' and item.isdigit():
                regex_type = 'meta'
                current_regex.append(int(item))
            elif item!='':
                regex_list = item[1:-1]
                break
        if len(current_regex)!=0:
            regex_list.append(current_regex)

        
        rule_dict[rule_id] = regex_list    
        regex_type_dict[rule_id] = regex_type

    return rule_dict,regex_type_dict,string_list

def match_regex_helper(line,indexA,indexB,sequence,rule_dict,regex_type_dict,lookup_table):
    if len(sequence)>(indexB+1-indexA):
        return False

    # print(line[indexA:indexB+1])
    # print(sequence)
    if len(sequence)==1:
        return match_regex(line,indexA,indexB,rule_dict,regex_type_dict,sequence[0],lookup_table)
    for i in range(indexA,indexB):
        if (match_regex_helper(line,indexA,i,sequence[0:1],rule_dict,regex_type_dict,lookup_table) and
            match_regex_helper(line,i+1,indexB,sequence[1:],rule_dict,regex_type_dict,lookup_table)):
            return True
    return False

def match_regex(line,indexA,indexB,rule_dict,regex_type_dict,rule_num,lookup_table):
    if indexA not in lookup_table:
        lookup_table[indexA]={}
    if indexB not in lookup_table[indexA]:
        lookup_table[indexA][indexB]={}
    if rule_num not in lookup_table[indexA][indexB]:
        lookup_table[indexA][indexB][rule_num]=2

    if lookup_table[indexA][indexB][rule_num]==0:
        return False
    if lookup_table[indexA][indexB][rule_num]==1:
        return True

    # print(line[indexA:indexB+1])
    # print(rule_dict[rule_num])
    if regex_type_dict[rule_num] == 'str':
        result = rule_dict[rule_num] == line[indexA:indexB+1] 
        if result:
            lookup_table[indexA][indexB][rule_num] = 1
        else:
            lookup_table[indexA][indexB][rule_num] = 0
        return result

    for sequence in rule_dict[rule_num]:
        if match_regex_helper(line,indexA,indexB,sequence,rule_dict,regex_type_dict,lookup_table):
            lookup_table[indexA][indexB][rule_num] = 1
            return True

    lookup_table[indexA][indexB][rule_num] = 0
    return False


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    rule_dict,regex_type_dict,string_list = parse_input01(fname)

    count = 0
    for line in string_list:
        has_matched = match_regex(line,0,len(line)-1,rule_dict,regex_type_dict,0,{})
        # print(line)
        # print(has_matched)
        if has_matched:
            count+=1

    print(count)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    rule_dict,regex_type_dict,string_list = parse_input01(fname)

    rule_dict[8] = [[42],[42,8]]
    rule_dict[11] = [[42,31],[42,11,31]]

    count = 0
    for line in string_list:
        has_matched = match_regex(line,0,len(line)-1,rule_dict,regex_type_dict,0,{})
        print(line)
        print(has_matched)
        if has_matched:
            count+=1

    print(count)

if __name__ == '__main__':
    # solution01()
    solution02()
    

