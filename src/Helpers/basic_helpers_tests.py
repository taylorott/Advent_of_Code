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

def padding_tests():
	print('Padding Tests:')
	print('')

	str1 = 'abdefg'
	item1 = 'z'
	n1 = 3
	print('Original String:')
	print(str1)
	print('n = '+str(n1)+', padding with: \''+item1+'\'')
	print(bh.pad_str(str1,n1,item1))
	print('')

	list2 = [1,2,3,5]
	item2 = 0
	n2 = 2
	print('Original List:')
	print(list2)
	print('n = '+str(n2)+', padding with: '+str(item2))
	print(bh.pad_list(list2,n2,item2))
	print('')

	grid3 = [[1,2,3],[4,5,6]]
	item3 = 0
	n3 = 2
	print('Original Grid')
	for temp in grid3:
		print(temp)
	print('n = '+str(n3)+', padding with: '+str(item3))
	temp_grid = bh.pad_grid(grid3,n3,item3)
	for temp in temp_grid:
		print(temp)
	print('')

	list4 = ['abc','def']
	item4 = '.'
	n4 = 4

	print('Original str grid')
	for temp in list4:
		print(temp)
	print('n = '+str(n4)+', padding with: \''+item4+'\'')
	temp_list = bh.pad_str_grid(list4,n4,item4)
	for temp in temp_list:
		print(temp)

def rotate_grid_test():
	my_grid0 = [[1,2,3],[4,5,6]]
	my_grid1 = bh.rotate_grid(my_grid0,1)
	my_grid2 = bh.rotate_grid(my_grid0,2)
	my_grid3 = bh.rotate_grid(my_grid0,3)


	print('Rotate Grid Test:')
	print('')

	print('Original Grid:')
	for item in my_grid0:
		print(item)

	print('')
	print('Rotated 90 deg counter-clockwise')
	for item in my_grid1:
		print(item)

	print('')
	print('Rotated 180 deg')
	for item in my_grid2:
		print(item)

	print('')
	print('Rotated 90 deg clockwise')
	for item in my_grid3:
		print(item)

if __name__ == '__main__':
	# freq_table_tests()
	# rotate_grid_test()
	padding_tests()