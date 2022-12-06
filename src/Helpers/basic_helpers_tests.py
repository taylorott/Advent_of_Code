#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import numpy as np
import re
import basic_helpers as bh
from DSA_helpers import Digraph, frequency_table

def print_test_result(test_type,test_number,result):
	if result:
		print(test_type+' test #'+str(test_number)+' passed')
	else:
		print(test_type+' test #'+str(test_number)+' failed')

def freq_table_tests():
	str1 = 'abbaca'
	str2 = 'aaabbc'
	str3 = 'defgh'

	freq_table1 = frequency_table(str1)
	freq_table2 = frequency_table(str2)
	freq_table3 = frequency_table(str3)

	print(freq_table1)

	test_count = 0
	test_type = 'freq_table'

	test = freq_table1 == freq_table2
	test_count+=1
	print_test_result(test_type,test_count,test)

	test = not(freq_table2 == freq_table3)
	test_count+=1
	print_test_result(test_type,test_count,test)

	test = 'a' in freq_table1
	test_count+=1
	print_test_result(test_type,test_count,test)

	test = 'e' not in freq_table1
	test_count+=1
	print_test_result(test_type,test_count,test)

	freq_table1.remove_item('c')
	test = freq_table1['c']==0
	test_count+=1
	print_test_result(test_type,test_count,test)

	freq_table1.remove_item('c')
	test = freq_table1['c']==0
	test_count+=1
	print_test_result(test_type,test_count,test)

	freq_table1.remove_item('c',True)
	test = freq_table1['c']==-1
	test_count+=1
	print_test_result(test_type,test_count,test)

	freq_table1.add_item('e')
	test = freq_table1['e']==1
	test_count+=1
	print_test_result(test_type,test_count,test)

	freq_table1.add_item('a')
	test = freq_table1['a']==4
	test_count+=1
	print_test_result(test_type,test_count,test)

	test = freq_table1.max_frequency()==4
	test_count+=1
	print_test_result(test_type,test_count,test)

if __name__ == '__main__':
	freq_table_tests()