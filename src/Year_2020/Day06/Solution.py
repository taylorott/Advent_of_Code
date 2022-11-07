#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh

path = currentdir

def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    total = 0
    for item in data:
        question_dict = {}
        for person in item:
            for question in person:
                question_dict[question] = True

        num_questions = len(question_dict.keys())
        total += num_questions

    print(total)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    # num_list = bh.parse_num_column(path,fname)
    data = bh.parse_split_by_emptylines(path,fname)
    # data = bh.parse_strings(path,fname)

    total = 0
    for item in data:
        question_dict = {}
        num_persons = len(item)
        for person in item:
            for question in person:
                if question in question_dict:
                    question_dict[question] += 1
                else:
                    question_dict[question] = 1

                if question_dict[question] == num_persons:
                    total+=1
    print(total)


if __name__ == '__main__':
    solution01()
    solution02()
    

