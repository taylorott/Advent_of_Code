#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.abspath(inspect.getfile(inspect.currentframe()))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import Helpers.basic_helpers as bh
from functools import cmp_to_key

path = currentdir

def example01():
	l1 = [['cool',3],['googa',1],['snozzle',2]]

	print('unsorted list')
	print(l1)

	l2 = sorted(l1, key=lambda item: item[1])

	print('sorted list')
	print(l2)

def example_compare_function(x,y):
	if x[1]>y[1]:
		return 1
	if x[1]<y[1]:
		return -1
	if x[1]==y[1]:
		return 0

def example02():

	l1 = [['cool',3],['googa',1],['snozzle',2]]

	print('unsorted list')
	print(l1)

	l2 = sorted(l1, key=cmp_to_key(example_compare_function))
	

	print('sorted list')
	print(l2)



	l1 = [['cool',3],['googa',1],['snozzle',2]]

	print('unsorted list')
	print(l1)

	l2 = sorted(l1, key=cmp_to_key(lambda x,y: example_compare_function(x,y)))

	print('sorted list')
	print(l2)

if __name__ == '__main__':
    example01()
    example02()