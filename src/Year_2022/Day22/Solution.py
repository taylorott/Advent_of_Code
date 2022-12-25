#!/usr/bin/env python 
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
sys.path.insert(0,os.path.dirname(os.path.dirname(currentdir)))

import time
import numpy as np
import re
import Helpers.basic_helpers as bh
from Helpers.DSA_helpers import Graph, Digraph, frequency_table, AugmentedHeap
from math import gcd, lcm
from collections import deque
import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle, Circle

path = currentdir

def parse_input01(fname):
    return bh.parse_split_by_emptylines(path,fname,delimiters = [],type_lookup = None, allInt = False, allFloat = False)

def parse_board(board):
    height = len(board)
    width = 0

    for i in range(height):
        board[i]=list(board[i])
        width = max(width,len(board[i]))

    for i in range(height):
        board[i]=board[i]+[' ']*(width-len(board[i]))

    return board

def parse_instructions(instructions):
    instructions = instructions.replace('R',' R ')
    instructions = instructions.replace('L',' L ')
    instructions = instructions.split(' ')

    command_list = []

    for item in instructions:
        if item!='':
            command_list.append(item)

    return command_list

#directions are coded as integers 0: Right, 1: Down 2: Left, 3: Up

#maps directions to vector representation
direction_dict_grid = {0:np.array([0,1]),1:np.array([1,0]),2:np.array([0,-1]),3:np.array([-1,0])}

direction_dict_plot = {0:np.array([1,0]),1:np.array([0,-1]),2:np.array([-1,0]),3:np.array([0,1])}

#maps left/right commands to corresponding increment in direction
rotation_dict = {'L':-1,'R':1}

#maps directions to corresponding symbols when printing on grid
direction_character_dict = {0:'>',1:'v',2:'<',3:'^'}

#diagonals are coded as 0: Down-Right, 1: Down-Left, 2: Up-Left, 3: Up-Right

#maps diagonals to corresponding vectors
diagonal_dict_grid = {0:np.array([1,1]),1:np.array([1,-1]),2:np.array([-1,-1]),3:np.array([-1,1])}

diagonal_dict_plot = {0:np.array([1,-1]),1:np.array([-1,-1]),2:np.array([-1,1]),3:np.array([1,1])}


#returns True if a grid coordinate is out of bounds of the grid we've been provided
def on_exterior(coords,board):
    return coords[0]<0 or coords[1]<0 or coords[0]>=len(board) or coords[1]>=len(board[0]) or board[coords[0]][coords[1]]==' '

#returns True if a grid coordinate is in-bounds for the grid we've been provided
def on_interior(coords,board):
    return not on_exterior(coords,board)

#move one step along grid
def execute_step(coords,direction,board,adjacency_dict):
    #compute nominal coordinates/direction after executing step
    next_coords = coords+direction_dict_grid[direction]
    next_direction = direction

    #if the naive motion would take us out of bounds of the map
    if on_exterior(next_coords,board):

        #use the adjacency matrix to find where on the map (and in what direction)
        #we would actually end up
        key_in = (tuple(coords.tolist()),direction)

        next_coords = np.array(list(adjacency_dict[key_in][0]))
        next_direction = adjacency_dict[key_in][1]

    #if the next location would cause us to run into a wall, do nothing
    if board[next_coords[0]][next_coords[1]]=='#':
        return coords, direction

    #otherwise, return updated coordinates/direction
    else:
        return next_coords, next_direction

#run a single command in the path that the monkeys gave us
def execute_command(coords,direction,command,board,boundary_dict):
    #update the grid for visualizaton purposes (showing our path)
    board[coords[0]][coords[1]]=direction_character_dict[direction]

    #if given a rotation command
    if command=='L' or command=='R':
        #update the direction accordingly
        direction+=rotation_dict[command]
        direction%=4
    #if given a forward motion command
    else:
        #move forward by the number of steps that have been commanded

        num_steps = int(command)

        for i in range(num_steps):
            #update the grid for visualizaton purposes (showing our path)
            board[coords[0]][coords[1]]=direction_character_dict[direction]

            #move forward a single step
            coords, direction = execute_step(coords,direction,board,boundary_dict)

    return coords,direction

#execute a single step when traveling along the perimeter of the map
#note that it makes the assumption that we are starting from an "inner corner" of the 2D pattern
#then moving outwards, and this perimeter traversal will terminate before we hit another inner corner
#As such, the only corners that will be "rounded" are outer corners, meaning that moving along the tangential
#direction would bring us into the exterior of the pattern (not the case for inner corners)
def perimeter_step(coords,direction,board):
    #compute the nominal next grid coordinates after moving forward along the perimeter 1 step
    next_coords = coords+direction_dict_grid[direction]

    #if moving in the current direction would take us to the exterior of the 2D pattern
    if on_exterior(next_coords,board):
        #computer the directions that are left/right of the current one
        #as well as the adjacent grid points in these two directions

        directionL = (direction-1)%4
        next_coordsL = coords+direction_dict_grid[directionL]

        directionR = (direction+1)%4
        next_coordsR = coords+direction_dict_grid[directionR]

        #whichever of these directions would keep us on the interior of the map is the new direction
        #since we are rounding a corner, we keep the current coordinates, and just change the direction
        if on_interior(next_coordsL,board):
            return coords, directionL

        if on_interior(next_coordsR,board):
            return coords, directionR

    return next_coords, direction

#checks for grid-points in the 2D pattern that are "inner corners"
#these correspond to locations where a zipper starts on the cube
#grid points who are missing a diagonal neighbor, but also have both cardinal neighbors shared with the missing diagonal
#are considered to the locations of inner corners. 
#the location of the missing diagonal neighbor tells us which two cardinal directions to travel in
#to leave th inner corner and travel along the perimeter
def check_if_inner_corner(coords,board):
    if on_exterior(coords,board):
        return False, None

    direction_pair_list = []

    for i in range(4):
        if (on_interior(coords+direction_dict_grid[i],board) and on_interior(coords+direction_dict_grid[(i+1)%4],board)
            and on_exterior(coords+diagonal_dict_grid[i],board)):
            direction_pair_list.append([i,(i+1)%4])    

    if len(direction_pair_list)>0:
        return True, direction_pair_list
    else:
        return False, None

#checks for grid-points in the 2D pattern that are "outer corners"
#zippers can sometimes start at a pair of outer corners after all the inner corner zips have been performed
#grid points on the interior who are missing two consecutive cardinal neighbors are considered outer corners
def check_if_outer_corner(coords,board):
    if on_exterior(coords,board):
        return False, None

    direction_pair_list = []

    for i in range(4):
        if on_exterior(coords+direction_dict_grid[i],board) and on_exterior(coords+direction_dict_grid[(i+1)%4],board):
            direction_pair_list.append([(i-1)%4,(i+2)%4])  

    if len(direction_pair_list)>0:
        return True, direction_pair_list
    else:
        return False, None

#starting from an inner corner, zip up the cube, generating the corresponding 
#adjacency mapping of (coord,direction)<->(coord,direction) for seams of the cube
#we'll need to do this for several inner corners to get the complete map
def zip_up_edges_from_corner(coords,direction_pair,board,dict_in,is_inner):
    direction0 = direction_pair[0]
    direction1 = direction_pair[1]

    direction0_prev = direction0
    direction1_prev = direction1


    if is_inner:
        coords0 = coords+direction_dict_grid[direction0]
        coords1 = coords+direction_dict_grid[direction1]

    
    #travel along the perimeter of the 2D pattern in opposite directions
    #this process continues until 2 corners are rounded simultaneously during the traversal
    #also terminate process if we hit another inner corner
    while direction0 == direction0_prev or direction1_prev == direction1:
        direction0_prev = direction0
        direction1_prev = direction1

        #identify the inner/outer normal directions for both line segments we are currently looking at
        normal_direction_outer0 = (direction0+1)%4
        if on_interior(coords0+direction_dict_grid[normal_direction_outer0],board):
            normal_direction_outer0 = (direction0-1)%4

        normal_direction_outer1 = (direction1+1)%4
        if on_interior(coords1+direction_dict_grid[normal_direction_outer1],board):
            normal_direction_outer1 = (direction1-1)%4

        normal_direction_inner0 = (normal_direction_outer0+2)%4
        normal_direction_inner1 = (normal_direction_outer1+2)%4

        key0 = (tuple(coords0.tolist()),normal_direction_outer0)
        key1 = (tuple(coords1.tolist()),normal_direction_outer1)

        if key0 in dict_in or key1 in dict_in:
            break

        #update the adjacency map using current coords and inner/outer normals
        dict_in[key0]=(tuple(coords1.tolist()),normal_direction_inner1)
        dict_in[key1]=(tuple(coords0.tolist()),normal_direction_inner0)

        #move along the perimeter in each direction by one step
        coords0, direction0 = perimeter_step(coords0,direction0,board)
        coords1, direction1 = perimeter_step(coords1,direction1,board)

        #terminate process if we hit another inner corner
        bool0, dummy =check_if_inner_corner(coords0,board)
        bool1, dummy =check_if_inner_corner(coords1,board)

        if bool0 or bool1:
            break



#zip up the entire cube
def generate_off_grid_adjacency_cube(board):
    dict_out = {}

    #check every grid point
    for i in range(len(board)):
        for j in range(len(board[0])):
            coords = np.array([i,j])

            #if the grid point is an inner corner,
            #perform a single zip starting from that grid point
            corner_bool, direction_pair_list = check_if_inner_corner(coords,board)
            if corner_bool:
                for direction_pair in direction_pair_list:
                    zip_up_edges_from_corner(coords,direction_pair,board,dict_out,is_inner=True)

    return dict_out

#this is for part 1: construct the adjacency map using the wrap-rule
def generate_off_grid_adjacency_wrap(board):
    dict_out = {}

    for i in range(len(board)):
        left = 0
        while board[i][left]==' ':
            left+=1


        right = len(board[0])-1
        while board[i][right]==' ':
            right-=1

        dict_out[((i,left),2)]=((i,right),2)
        dict_out[((i,right),0)]=((i,left),0)

    for i in range(len(board[0])):
        top = 0
        while board[top][i]==' ':
            top+=1

        bottom = len(board)-1
        while board[bottom][i]==' ':
            bottom-=1

        dict_out[((top,i),3)]=((bottom,i),3)
        dict_out[((bottom,i),1)]=((top,i),1)

    return dict_out

cell_palette = {'A':'red','B':'cyan','C':'forestgreen','D':'yellow','E':'orange','F':'pink'}
arrow_palette = {0:'orange',1:'teal',2:'grey',3:'brown'}


def visualize_grid(board,ax):
    right_vector = np.array([1,0])
    down_vector = np.array([0,-1])

    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]!=' ':
                top_left_coord = j*right_vector+i*down_vector

                ax.add_patch(Rectangle((top_left_coord[0], top_left_coord[1]-1), 1, 1,
                            edgecolor = 'black',
                            facecolor = cell_palette[board[i][j]],
                            fill=True,))

def plot_inner_corner(coords,direction_pair,ax):
    right_vector = np.array([1,0])
    down_vector = np.array([0,-1])

    i = coords[0]
    j = coords[1]

    corner_coord = (j+.5)*right_vector+(i+.5)*down_vector+diagonal_dict_plot[direction_pair[0]]/2
                    
    ax.add_patch(Circle((corner_coord[0], corner_coord[1]), .2,
            edgecolor = 'black',
            facecolor = 'black',
            fill=True,))

def plot_all_inner_corners(board,ax):
    adjacency_dict = {}
    count = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            coords = np.array([i,j])
            corner_bool, direction_pair_list = check_if_inner_corner(coords,board)
            if corner_bool:
                for direction_pair in direction_pair_list:
                    plot_inner_corner(coords,direction_pair,ax)
                    visualize_zip(coords,direction_pair,board,adjacency_dict,ax,count)
                    count+=1

def plot_edge_vector(coords,normal_outer,direction,ax,color_code):
    right_vector = np.array([1,0])
    down_vector = np.array([0,-1])

    i = coords[0]
    j = coords[1]

    arrow_vector = direction_dict_plot[direction]
    cell_centroid_ = (j+.5)*right_vector+(i+.5)*down_vector
    boundary_midpoint = cell_centroid_+.5*direction_dict_plot[normal_outer]
    tail_location = boundary_midpoint-.5*arrow_vector

    color = arrow_palette[color_code]

    ax.arrow(tail_location[0],tail_location[1],arrow_vector[0],arrow_vector[1],
            head_width=0.15, head_length=0.2, length_includes_head = True ,fc = color, color = color)


def plot_zip_step(coords0,coords1,direction0,direction1,board,dict_in,ax,color_code):

    direction0_prev = direction0
    direction1_prev = direction1

    #identify the inner/outer normal directions for both line segments we are currently looking at
    normal_direction_outer0 = (direction0+1)%4
    if on_interior(coords0+direction_dict_grid[normal_direction_outer0],board):
        normal_direction_outer0 = (direction0-1)%4

    normal_direction_outer1 = (direction1+1)%4
    if on_interior(coords1+direction_dict_grid[normal_direction_outer1],board):
        normal_direction_outer1 = (direction1-1)%4

    normal_direction_inner0 = (normal_direction_outer0+2)%4
    normal_direction_inner1 = (normal_direction_outer1+2)%4


    #update the adjacency map using current coords and inner/outer normals
    dict_in[(tuple(coords0.tolist()),normal_direction_outer0)]=(tuple(coords1.tolist()),normal_direction_inner1)
    dict_in[(tuple(coords1.tolist()),normal_direction_outer1)]=(tuple(coords0.tolist()),normal_direction_inner0)


    plot_edge_vector(coords0,normal_direction_outer0,direction0,ax,color_code)
    plot_edge_vector(coords1,normal_direction_outer1,direction1,ax,color_code)

    #move along the perimeter in each direction by one step
    coords0, direction0 = perimeter_step(coords0,direction0,board)
    coords1, direction1 = perimeter_step(coords1,direction1,board)

    #terminate process if we hit another inner corner
    bool0, dummy =check_if_inner_corner(coords0,board)
    bool1, dummy =check_if_inner_corner(coords1,board)
    bool2 = direction0 != direction0_prev and direction1_prev != direction1

    termination_condition = bool0 or bool1 or bool2

    return coords0,coords1,direction0,direction1,termination_condition


def visualize_zip(coords,direction_pair,board,dict_in,ax,color_code):
    direction0 = direction_pair[0]
    direction1 = direction_pair[1]

    direction0_prev = direction0
    direction1_prev = direction1

    coords0 = coords+direction_dict_grid[direction0]
    coords1 = coords+direction_dict_grid[direction1]

    #identify the inner/outer normal directions for both line segments we are currently looking at
    normal_direction_outer0 = (direction0+1)%4
    if on_interior(coords0+direction_dict_grid[normal_direction_outer0],board):
        normal_direction_outer0 = (direction0-1)%4

    normal_direction_outer1 = (direction1+1)%4
    if on_interior(coords1+direction_dict_grid[normal_direction_outer1],board):
        normal_direction_outer1 = (direction1-1)%4

    key0 = (tuple(coords0.tolist()),normal_direction_outer0)
    key1 = (tuple(coords1.tolist()),normal_direction_outer1)

    if key0 in dict_in or key1 in dict_in:
        return None


    termination_condition = False

    while not termination_condition:
        coords0,coords1,direction0,direction1, termination_condition = plot_zip_step(coords0,coords1,direction0,direction1,board,dict_in,ax,color_code)
        plot_inner_corner(coords,direction_pair,ax)

def run_visualization():
    fname = 'Input03.txt'

    data = parse_input01(fname)
    board = parse_board(data[7])

    fig, ax = plt.subplots()

    visualize_grid(board,ax)
    plot_all_inner_corners(board,ax)

    
    ax.axis('off')
    ax.axis('equal')
    plt.show()

#only difference between solution01/solution02 is the
#adjacency map used for gridpoints that are out of bounds

#runs part 1
def solution01():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    board = parse_board(data[0])
    command_list = parse_instructions(data[1][0])

    adjacency_dict = generate_off_grid_adjacency_wrap(board)

    coords = np.array([0,0])
    while board[coords[0]][coords[1]]==' ':
        coords[1]+=1
    
    direction = 0

    for command in command_list:
        coords,direction = execute_command(coords,direction,command,board,adjacency_dict)

    code = 1000*(coords[0]+1)+4*(coords[1]+1)+direction
    print(code)


#runs part 2
def solution02():
    # fname = 'Input01.txt'
    fname = 'Input02.txt'

    data = parse_input01(fname)
    board = parse_board(data[0])
    command_list = parse_instructions(data[1][0])

    adjacency_dict = generate_off_grid_adjacency_cube(board)

    coords = np.array([0,0])
    while board[coords[0]][coords[1]]==' ':
        coords[1]+=1

    direction = 0

    for command in command_list:
        coords,direction = execute_command(coords,direction,command,board,adjacency_dict)

    code = 1000*(coords[0]+1)+4*(coords[1]+1)+direction
    print(code)



if __name__ == '__main__':
    t0 = time.time()
    solution01()
    solution02()
    print('runtime in seconds: ','%.3f' % (time.time()-t0))

    # run_visualization()
    

