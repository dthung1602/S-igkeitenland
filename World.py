#! /usr/bin/env python
# coding=utf-8

from Trap import *
from mcpi.minecraft import Minecraft
import Global
from copy import deepcopy
from Draw import *

mc = Minecraft.create()


####################################################################
#                            Surface                               #
####################################################################


def create_ground():
    """clear sky and create ground"""

    # ground
    # TODO select material
    mc.setBlocks(127, Global.ground_height, 127, -128, -64, -128, 1)

    # air
    mc.setBlocks(127, 63, 127, -128, Global.ground_height, -128, 0)


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


def create_corn_mountain(x, y, z, h, r):
    """
            create a corn candy mountain
        x, y, z: position of center of lowest layer of the mountain
        h: height
        r: radius of the base of the mountain
    """

    # create the wall
    # TODO change material
    for i in range(0, h):
        if i < h / 3:
            block_type = WOOL
        elif i < 2 * h / 3:
            block_type = STONE
        else:
            block_type = GRASS
        draw_horizontal_circle_outline(x, y + i, z, r * sqrt(1 - (y * 1.0 + i) / (y + h)), block_type)

    # create the roof
    draw_horizontal_circle(x, y + h, z, r * sqrt(1 - (y + h - 1.0) / (y + h)), GRASS)


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


def create_lollipop(x, y, z, r, h, block_type, block_data):
    """create a lollipop"""
    # Create the lollipop stick
    mc.setBlocks(x, y + h, z, x, y, z, ICE)
    # Create the lollipop top
    draw_sphere(x, y + h, z, r, block_type, block_data)


def create_lollipop_forest():
    """create a lollipop forest at the south of the map"""


def create_cane_candy(x, y, z, candy_data):
    """
            create a cane candy
        x, y, z: position of the first lowest block of cane candy
        candy_data: list to construct cane candy
    """

    for i in xrange(0, len(candy_data)):
        for j in xrange(0, len(candy_data[i])):
            for k in xrange(0, len(candy_data[i][j])):
                mc.setBlock(x + i, y + j, z + k, candy_data[i][j][k])


def create_cane_candy_forest():
    """create cane candy forest at the north of the map"""

    # read data from file
    f = open('data/candy/cane_candy.txt', 'r')

    # translate data to blocks and store in 2D list
    data2d = []
    for line in f:
        tmp = []
        for char in line.strip():
            if char == 'W':
                tmp.append(WOOL)
            elif char == 'R':
                tmp.append(STONE)
            elif char == '.':
                tmp.append(AIR)
        data2d.append(tmp)

    # reverse data2d so that the candy not up side down
    data2d = data2d[::-1]

    # make the candy 3D
    data3d = []
    for i in xrange(4):
        data3d.append(data2d)

    # make copies of data3d that face north, south, west, east
    # original : +z
    # x: east, z: south
    south = data3d

    north = deepcopy(south)
    for i in xrange(len(north)):
        for j in xrange(len(north[i])):
            north[i][j] = south[i][j][::-1]

    east = []
    for i in xrange(len(south[0][0])):
        temp = []
        for j in xrange(len(south[0])):
            tmp = []
            for k in xrange(len(south)):
                tmp.append(south[k][j][i])
            temp.append(tmp)
        east.append(temp)

    west = deepcopy(east)[::-1]

    # TODO tmp
    global x, y, z
    create_cane_candy(x + 15, y, z, south)
    create_cane_candy(x + 20, y, z, north)
    create_cane_candy(x, y, z + 15, east)
    create_cane_candy(x, y, z + 20, west)


def create_oreo(x, y, z, r):
    """create an oreo cookie"""
    for i in xrange(3):
        draw_horizontal_circle(x, y + i, z, r, COAL_ORE)
    for i in xrange(3):
        draw_horizontal_circle(x, y + 3 + i, z, r - 1, SNOW_BLOCK)
    for i in xrange(3):
        draw_horizontal_circle(x, y + 6 + i, z, r, COAL_ORE)


def create_oreos():
    """create oreos at the east of the map"""


def create_cupcake_house(x, y, z, r):
    """create a cupcake house"""
    # roof
    draw_sphere(x, y + r, z, r, GLOWSTONE_BLOCK)
    draw_sphere(x, y + r, z, r - 1, AIR)
    sleep(r * 3)
    mc.setBlocks(x - r - 3, y, z - r - 3, x + r + 3, y + r, z + r + 3, AIR)

    # wall
    for i in xrange(r + 1):
        draw_horizontal_circle_outline(x, y + i, z, r / 2 + i / 2, STONE)
        if i % 2 == 1:
            draw_horizontal_circle_outline(x, y + i + 1, z, r / 2 + i / 2, TORCH)


def create_cupcake_village():
    """create cup cake village in the center of the map"""


def create_coke_tower(x, y, z):
    """
    create_coke_tower at the north of the village
    x, y, z: position of center of lowest layer of tower
    """
    block_type = {
        "W": WOOL,
        "R": STONE_BRICK,
        "B": GRASS,
    }

    f = open('data/candy/coke_tower.txt', 'r')

    for line in f:
        r, color = line.strip().split(" ")
        draw_horizontal_circle_outline(x, y, z, int(r), block_type[color[0]])
        y += 1


####################################################################
#                          Underground                             #
####################################################################


# a dictionary to convert number to trap
trap = {
    '0': FallIntoLavaTrap,
}


def create_maze_floor(floor, x, y, z):
    """
            Create a floor of the maze
        File structure:
        ' '        = air
        '#'        = stone wall
        '*'        = stone wall with torch at highest block
        [number]   = trap

    """

    # open file
    try:
        f = open("./data/maze/maze" + str(floor) + ".txt", "r")
    except IOError:
        print "Data of maze %d can not be loaded" % floor
        return

    # load data from file to array
    maze_map = f.read().split("\n")

    # create maze
    for i in xrange(len(maze_map)):
        for j in xrange(len(maze_map[i])):
            # select block type to build
            if maze_map[i][j] == '#' or maze_map[i][j] == '*':
                block = GLOWSTONE_BLOCK
            else:
                block = AIR

            # build
            mc.setBlocks(x + i, y, z + j, x + i, y + Global.floor_height, z + j, block)

            # if '*' then create a torch at the highest block
            if maze_map[i][j] == '*':
                mc.setBlock(x + i, y + Global.floor_height, z + j, TORCH)

            # if [number] then create a trap
            if isinstance(maze_map[i][j], int):
                trap[maze_map[i][j]](x + i, y, z + j)

    # create maze entrance room
    mc.setBlocks(x, y, z - 1, x + 7, y + Global.floor_height, z - 7, AIR)

    # create a hole to upper floor
    mc.setBlocks(x + 1, y, z, x + 1, y + Global.floor_height + 4, z + Global.floor_height + 3, AIR)

    # create stairs
    for i in xrange(Global.floor_height + 4):
        mc.setBlock(x + 1, y + i, z + Global.floor_height + 3 - i, STAIRS_COBBLESTONE.id, 3)


def create_mazes():
    """create floors of the maze"""
    # coordinate of first block of lowest floor of the maze
    # depend on position of FallIntoMaze trap - triggers[0]
    x = Global.triggers[0].pos.x - 3
    y = Global.triggers[0].depth - 4
    z = Global.triggers[0].pos.z + 11

    # create mazes
    for i in xrange(1, 1 + Global.number_of_floor):
        create_maze_floor(i, x, y + (i - 1) * (Global.floor_height + 4), z)


def create_mobs():
    """create mobs all over the maze"""


if __name__ == "__main__":
    x, y, z = Global.mc.player.getTilePos()
    create_cane_candy_forest()
