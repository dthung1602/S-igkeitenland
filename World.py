#! /usr/bin/env python
# coding=utf-8

from Trigger import *
from utility import *

##################################################
#                   surface                      #
##################################################


def create_ground():
    """clear sky and create ground"""

    # ground
    # TODO select material
    mc.setBlocks(127, ground_height, 127, -128, -64, -128, 1)

    # air
    mc.setBlocks(127, 63, 127, -128, ground_height, -128, 0)


def create_mountain():
    """create a mountain"""
    pass


def create_craggy_mountains():
    """create tall mountains surround map"""
    pass


def create_tree():
    """create one tree"""
    pass


def create_forest():
    """ create a forest at the south of the map"""
    pass


def create_corn_mountain():
    """create a corn candy mountain"""
    pass


def create_corn_candy_mountains():
    """ create a forest at the south of the map"""
    pass


def create_river():
    """create a chocolate river"""
    pass


def create_hill():
    """create an ice-cream hill"""


def create_ice_cream_hills():
    """create ice cream hills at the west of the map"""


def create_lollipop():
    """create a lollipop"""


def create_lollipop_forest():
    """create a lollipop forest at the south of the map"""


def create_cane_candy():
    """create a cane candy"""


def create_cane_candy_forest():
    """create cane candy forest at the north of the map"""


def create_oreo():
    """create a oreo"""


def create_oreos():
    """create oreos at the east of the map"""


def create_cupcake_village():
    """create cupcake village at the center of the map"""


def create_coke_tower(x, y, z):
    """
    create_coke_tower at the north of the village
    x, y, z: position of center of lowest layer of tower
    """
    block_type = {
        "W" : WOOL,
        "R" : STONE_BRICK,
        "B" : GRASS,
    }

    file = open('data/coke_tower.txt', 'r')

    for line in file:
        r, color = line.split(" ")
        draw.drawHorizontalCircle(x, y, z, int(r), block_type[color])
        y += 1




####################################
#          underground             #
####################################

# a dictionary to convert number to trap
trap = {
    'a': FallIntoLavaTrap,
    'b': PushBackTrap,
    'c': FlowLavaBlockWay_x,
    'D': FlowLavaBlockWay_z,
    'e': StoneBlockWay_x,
    'F': StoneBlockWay_z,
    'g': FallSand,
    'h': TrapInHole_x,
    'I': TrapInHole_z,
}


def create_maze_floor(floor):
    """
            Create a floor of the maze
            File structure:
        length width height : dimensions of the maze
        x y z               : position of first block of maze
        x_in z_in           : relative position of player when first in floor
        x_out z_out         : relative position of player when finish in floor
        [map of maze]
        ' '        = air
        '#'        = stone wall
        '*'        = torch
        '[number]' = trap
        
    """

    # load data from file to array
    f = open("./data/mazes/maze" + str(floor) + ".txt", "r")
    maze_map = f.read().split("\n")
    l, w, h = maze_map.pop(0).split()
    x, y, z = maze_map.pop(0).split()

    # create maze
    for i in xrange(l):
        for j in xrange(w):
            # find the correct block to build
            if maze_map[i][j] == ' ' or maze_map[i][j] == '*':
                block = AIR
            elif maze_map[i][j] == '#':
                block = STONE
            else:
                block = trap[int(maze_map[i][j])](x + i, y, z + j)

            # build
            for k in xrange(h + 1):
                mc.setBlock(x + i, y + k, z + j, block)

            # if '*' then create a torch at the highest block
            mc.setBlock(x + i, y + h, z + j, TORCH)


def create_mazes():
    """create floors of the maze"""
    for i in xrange(number_of_floor):
        create_maze_floor(i)


def create_ladder_room():
    """create a room with ladders lead to upper floor"""


def create_ladder_rooms():
    """create ladders to connect floors of maze"""


def create_mobs():
    """create mobs all over the maze"""
