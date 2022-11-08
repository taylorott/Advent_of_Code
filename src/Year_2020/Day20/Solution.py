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

    tile_list = []
    tile_ids = []
    for full_tile in data:
        tile_num = int(full_tile[0].split(' ')[1][0:-1])
        tile_map = full_tile[1:]
        tile_ids.append(tile_num)
        tile_list.append(tile_map)
    return tile_list,tile_ids

class TileClass(object):
    def __init__(self,tile_matrix,tile_id):
        self.tile_matrix=[]
        for item in tile_matrix:
            self.tile_matrix.append(list(item))
        self.tile_id = tile_id
        self.coords = [0,0]
        self.l = len(tile_matrix)
        self.extract_border_codes()

        self.left_neighbor = None
        self.right_neighbor = None
        self.top_neighbor = None
        self.bottom_neighbor = None

    def extract_border_codes(self):
        top_str = ''
        bot_str = ''
        left_str = ''
        right_str = ''

        for i in range(len(self.tile_matrix[0])):        
            top_str += self.tile_matrix[0][i]
            bot_str += self.tile_matrix[-1][i]

        for tile_str in self.tile_matrix:
            left_str+=tile_str[0]
            right_str+=tile_str[-1]

        left_str = left_str[::-1]
        bot_str = bot_str[::-1]    

        self.fwd_dict = {top_str:(1,1),bot_str:(3,1),left_str:(2,1),right_str:(0,1),
                    top_str[::-1]:(1,-1),bot_str[::-1]:(3,-1),left_str[::-1]:(2,-1),right_str[::-1]:(0,-1)}

        self.rev_dict = {(1,1):top_str,(3,1):bot_str,(2,1):left_str,(0,1):right_str,
                         (1,-1):top_str[::-1] ,(3,-1):bot_str[::-1] ,(2,-1):left_str[::-1] ,(0,-1):right_str[::-1]}

    def rotate90(self):
        new_tile_matrix = []

        l = len(self.tile_matrix)
        for i in range(l):
            new_tile_matrix.append([None]*l)

        for i in range(l):
            for j in range(l):
                new_tile_matrix[l-j-1][i] = self.tile_matrix[i][j]
        
        self.tile_matrix = new_tile_matrix

        self.extract_border_codes()

    def print_tile_matrix(self):
        for line in self.tile_matrix:
            print(line)

    def flip_vert_axis(self):
        new_tile_matrix = []

        l = len(self.tile_matrix)
        for i in range(l):
            new_tile_matrix.append([None]*l)

        for i in range(l):
            for j in range(l):
                new_tile_matrix[l-i-1][j] = self.tile_matrix[i][j]

        self.tile_matrix = new_tile_matrix
        self.extract_border_codes()

    def flip_horz_axis(self):
        new_tile_matrix = []

        l = len(self.tile_matrix)
        for i in range(l):
            new_tile_matrix.append([None]*l)

        for i in range(l):
            for j in range(l):
                new_tile_matrix[i][l-j-1] = self.tile_matrix[i][j]

        self.tile_matrix = new_tile_matrix
        self.extract_border_codes()

    def find_shared_border(self,tile_in):
        for key in self.fwd_dict:
            if key in tile_in.fwd_dict:
                return key
        return None
                



    def place_adjacent_tile(self,tile_in):
        compare_key = self.find_shared_border(tile_in)

        codeA = self.fwd_dict[compare_key]
        codeB = tile_in.fwd_dict[compare_key]

        if codeA[1]==codeB[1]:
            tile_in.flip_vert_axis()
            codeB = tile_in.fwd_dict[compare_key]

        while (codeA[0]-codeB[0])%4!=2:
            tile_in.rotate90()
            codeB = tile_in.fwd_dict[compare_key]

        if codeA[0]==0:
            self.right_neighbor = tile_in
            tile_in.coords = [self.coords[0],self.coords[1]+1]
        if codeA[0]==1:
            self.top_neighbor = tile_in
            tile_in.coords = [self.coords[0]-1,self.coords[1]]
        if codeA[0]==2:
            self.left_neighbor = tile_in
            tile_in.coords = [self.coords[0],self.coords[1]-1]
        if codeA[0]==3: 
            self.bottom_neighbor = tile_in
            tile_in.coords = [self.coords[0]+1,self.coords[1]]



def build_adjacency(tile_dict):
    border_map = {}

    for tile_id in tile_dict.keys():
        tile = tile_dict[tile_id]
        for border in tile.fwd_dict.keys():
            if border not in border_map:
                border_map[border] = [tile_id]
            else:
                border_map[border].append(tile_id)

    adj_mat = {}
    adj_list = {}

    for border in border_map.keys():
        if len(border_map[border])==2:
            tileA = border_map[border][0]
            tileB = border_map[border][1]

            if tileA not in adj_mat:
                adj_mat[tileA] = {}
                adj_list[tileA] = []
            if tileB not in adj_mat:
                adj_mat[tileB] = {}
                adj_list[tileB] = []

            if tileB not in adj_mat[tileA]:
                adj_mat[tileA][tileB] = None
                adj_list[tileA].append(tileB)
            if tileA not in adj_mat[tileB]:
                adj_mat[tileB][tileA] = None
                adj_list[tileB].append(tileA)

    return adj_list

def assemble_picture(tile_dict,adj_list,current_key = None, visited_dict = None):
    if visited_dict is None:
        visited_dict = {}
    if current_key in visited_dict:
        return

    visited_dict[current_key]=True
    for adj_id in adj_list[current_key]:
        if adj_id not in visited_dict:
            tile_dict[current_key].place_adjacent_tile(tile_dict[adj_id])
            assemble_picture(tile_dict,adj_list,adj_id, visited_dict)

def staple_image(pic_mat):
    l = len(pic_mat[0][0])
    big_pic = []
    for i in range(l*len(pic_mat)):
        big_pic.append([])

        q1 = i//l
        q2 = i%l
        for j in range(len(pic_mat[0])):
            big_pic[i]+=pic_mat[q1][j][q2]

    return big_pic


def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    tile_list,tile_ids = parse_input01(fname)

    tile_dict = {}

    for i in range(len(tile_list)):
        tile_dict[tile_ids[i]] = TileClass(tile_list[i],tile_ids[i])

    adj_list = build_adjacency(tile_dict)
    assemble_picture(tile_dict,adj_list,tile_ids[0])

    min_i = 0
    min_j = 0
    max_i = 0
    max_j = 0
    for i in range(len(tile_list)):
        min_i = min(min_i,tile_dict[tile_ids[i]].coords[0])
        min_j = min(min_j,tile_dict[tile_ids[i]].coords[1])
        max_i = max(max_i,tile_dict[tile_ids[i]].coords[0])
        max_j = max(max_j,tile_dict[tile_ids[i]].coords[1])
   
    max_i-=min_i
    max_j-=min_j

    for i in range(len(tile_list)):
        tile_dict[tile_ids[i]].coords[0]-=min_i
        tile_dict[tile_ids[i]].coords[1]-=min_j

    width  = max_i+1
    height = max_j+1

    pic_mat = []
    for i in range(width):
        pic_mat.append([None]*height)
    
    for i in range(len(tile_list)):    
        pic_mat[tile_dict[tile_ids[i]].coords[0]][tile_dict[tile_ids[i]].coords[1]]=tile_ids[i]

    print(pic_mat[0][0]*pic_mat[0][-1]*pic_mat[-1][0]*pic_mat[-1][-1])

def find_monster(my_pic_array,monster_array):
    intersect_mat = 0.0*my_pic_array
    monster_size = sum(sum(monster_array))

    l_monster = len(monster_array)
    w_monster = len(monster_array[0])


    l_pic= len(my_pic_array)
    w_pic= len(my_pic_array[0])

    found_monster = False
    for i in range(1+l_pic-l_monster):
        for j in range(1+w_pic-w_monster):
            if int(monster_size) == int(sum(sum(np.multiply(my_pic_array[i:i+l_monster,j:j+w_monster],monster_array)))):
                intersect_mat[i:i+l_monster,j:j+w_monster]+=monster_array
                found_monster = True

    if found_monster:
        water = int(sum(sum(my_pic_array))-sum(sum(intersect_mat)))
        print(water)

def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'
    fname_monster = 'Input03.txt'

    tile_list,tile_ids = parse_input01(fname)

    tile_dict = {}

    for i in range(len(tile_list)):
        tile_dict[tile_ids[i]] = TileClass(tile_list[i],tile_ids[i])

    adj_list = build_adjacency(tile_dict)
    assemble_picture(tile_dict,adj_list,tile_ids[0])

    min_i = 0
    min_j = 0
    max_i = 0
    max_j = 0
    for i in range(len(tile_list)):
        min_i = min(min_i,tile_dict[tile_ids[i]].coords[0])
        min_j = min(min_j,tile_dict[tile_ids[i]].coords[1])
        max_i = max(max_i,tile_dict[tile_ids[i]].coords[0])
        max_j = max(max_j,tile_dict[tile_ids[i]].coords[1])
   
    max_i-=min_i
    max_j-=min_j

    for i in range(len(tile_list)):
        tile_dict[tile_ids[i]].coords[0]-=min_i
        tile_dict[tile_ids[i]].coords[1]-=min_j

    width  = max_i+1
    height = max_j+1

    pic_mat = []
    for i in range(width):
        pic_mat.append([None]*height)


    
    for i in range(len(tile_list)):
        temp_mat = np.array(tile_dict[tile_ids[i]].tile_matrix)
        temp_mat = temp_mat[1:-1,1:-1].tolist()

        pic_mat[tile_dict[tile_ids[i]].coords[0]][tile_dict[tile_ids[i]].coords[1]]=temp_mat
    big_pic = staple_image(pic_mat)
    my_pic_array = 1.0*(np.array(big_pic)=='#')
    # print(my_pic_array)

    monster_list = bh.parse_strings(path,fname_monster)

    for i in range(len(monster_list)):
        monster_list[i] = list(monster_list[i])

    monster_array = 1.0*(np.array(monster_list)=='#')
    # monster_size = sum(sum(monster_array))
    # print(monster_array)
    # print(np.flip(monster_array))

    my_pic_array = np.rot90(my_pic_array)
    my_pic_array = np.fliplr(my_pic_array)


    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)

    monster_array = np.fliplr(monster_array)
    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)
    monster_array = np.rot90(monster_array)
    find_monster(my_pic_array,monster_array)
if __name__ == '__main__':
    solution01()
    solution02()
    

