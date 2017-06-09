#!/usr/bin/env python

"""
    This file contains all necessary functions to build the world
"""

from copy import deepcopy
from math import sqrt
from random import randint

from Draw import *
from Trap import *
from mcpi.minecraft import Minecraft

mc = Minecraft.create()


####################################################################
#                           Terrance                               #
####################################################################


def clear_world():
    """clear sky and create ground"""

    # ground
    mc.setBlocks(127, Global.ground_height, 127, -128, -64, -128, GOLD_BLOCK)

    # air
    mc.setBlocks(127, 63, 127, -128, Global.ground_height, -128, 0)


def create_craggy_mountains():
    """create tall mountains surround the land"""

    def constrain(val, min_val, max_val):
        """make sure val in its range"""
        return min(max_val, max(min_val, val))

    y = Global.ground_height
    mountain_width = 10
    max_init_height = 3
    min_init_height = 1
    max_height_inc = 4
    min_height_inc = 1
    snow_height = 30

    # northern mountains
    for x in xrange(-128, 128):
        height = randint(min_init_height, max_init_height)
        mountain_width = constrain(mountain_width + randint(-1, 1), 15, 20)
        snow_height = constrain(snow_height + randint(-2, 2), 30, 40)
        for z in xrange(-128 + mountain_width, -128, -1):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)

    # western mountains
    for z in xrange(-128, 128):
        height = randint(min_init_height, max_init_height)
        mountain_width = constrain(mountain_width + randint(-1, 1), 15, 20)
        snow_height = constrain(snow_height + randint(-2, 2), 30, 40)
        for x in xrange(-128 + mountain_width, -128, -1):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)

    # eastern mountains
    for z in xrange(-128, 128):
        height = randint(min_init_height, max_init_height)
        mountain_width = constrain(mountain_width + randint(-1, 1), 15, 20)
        snow_height = constrain(snow_height + randint(-2, 2), 30, 40)
        for x in xrange(128 - mountain_width, 128):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)


def create_river():
    """create a chocolate river"""

    # origin of the river
    x0 = 84 - 128
    z = 30 - 128

    # read data from file and create river
    try:
        f = open("data/object/river.txt")
    except IOError:
        print "Data of river can not be loaded"
        return

    for line in f:
        # how wide the river
        width = line.count('#') + 3

        # where the first water block is
        x = x0 + line.find('#')

        # fill water up to ground height
        y = Global.ground_height - 1

        # create
        for i in xrange(2):
            mc.setBlocks(x, y, z, x + width, y, z, AIR)
            width -= 2
            x += 1
            y -= 1

        # create water
        for i in xrange(4):
            mc.setBlocks(x, y, z, x + width, y, z, WATER)
            width -= 2
            x += 1
            y -= 1

        # move to next line
        z += 1


def create_corn_mountain(x, y, z, h, r):
    """
            create a corn candy mountain with a parabola shape
        x, y, z: position of center of lowest layer of the mountain
        h      : height
        r      : radius of the base of the mountain
    """

    for i in range(0, h):
        if i < h / 3:
            color = WOOL_ORANGE
        elif i < 2 * h / 3:
            color = WOOL_YELLOW
        else:
            color = WOOL_WHITE
        draw_horizontal_circle(x, y + i, z, r * sqrt(1 - (y * 1.0 + i) / (y + h)), color)


def create_corn_candy_mountains():
    """ create a forest at the south of the map"""
    i = 0
    y = Global.ground_height - 7
    x = [-82, -62, -55, -65, -40, -38, -98]
    z = [-77, -73, -48, -26, -100, -5, -120]
    while i < len(x):
        height = randint(40, 50)
        radius = randint(15, 20)
        create_corn_mountain(x[i], y, z[i], height, radius)
        i += 1


def create_ice_cream_hills():
    """create ice cream hills at the west of the map"""
    i = 0
    y = Global.ground_height
    x = [-85, -60, -48, -11]
    z = [83, 65, 43, 25]
    c = [WOOL_LIME, WOOL_BROWN, WOOL_GREEN, WOOL_PURPLE]
    while i < len(x):
        r = randint(20, 30)
        draw_upper_hemisphere(x[i], y, z[i], r, c[i])
        i += 1


def create_oreo(x, y, z, r, w):
    """
            create an oreo cookie
        x, y, z: coordinate of center of lowest floor
        r      : radius
        w      : width of each floor
    """
    for i in xrange(w):
        draw_horizontal_circle(x, y + i, z, r, COAL_ORE)
    for i in xrange(w):
        draw_horizontal_circle(x, y + w + i, z, r - 1, SNOW_BLOCK)
    for i in xrange(w):
        draw_horizontal_circle(x, y + w * 2 + i, z, r, COAL_ORE)


def create_oreos():
    """create oreos at the east of the map"""
    i = 0
    x = [55, 62, 73, 80, 85, 90, 75]
    y = [0, 6, 0, 6, 0, 0, 6]
    z = [-23, -11, 2, 8, 15, -35, -32]

    while i < len(x):
        radius = randint(8, 16)
        width = randint(2, 4)
        create_oreo(x[i], Global.ground_height + y[i], z[i], radius, width)
        i += 1


####################################################################
#                            Forests                               #
####################################################################


def create_tree(x, y, z):
    """ create one tree in forest"""

    def create_leave(height, height_of_leave, width_of_leave):
        """
                create one leave floor of the tree
            height         : y coordinate of leave
            height_of_leave: how high this leave floor is
            width_of_leave : how wide this leave floor is
        """
        for i in xrange(height_of_leave):
            mc.setBlocks(x - width_of_leave / 2, height + i, z - width_of_leave / 2,
                         x + width_of_leave / 2, height + i, z + width_of_leave / 2, LEAVES)
            mc.setBlocks(x - width_of_leave / 2 + randint(-1, 1), height + i, z - width_of_leave / 2 + randint(-1, 1),
                         x + width_of_leave / 2 + randint(-1, 1), height + i, z + width_of_leave / 2 + randint(-1, 1),
                         LEAVES)
            width_of_leave -= 2

    tree_height = randint(20, 35)

    # trunk
    mc.setBlocks(x, y, z, x - 1, y + tree_height * 2 / 3, z + 1, WOOD)
    mc.setBlocks(x, y + tree_height * 2 / 3, z, x, y + tree_height, z, WOOD)

    # leaves at the top
    mc.setBlocks(x - 1, y + tree_height, z - 1, x + 1, y + tree_height, z + 1, LEAVES)
    mc.setBlocks(x - 1, y + tree_height + 1, z, x + 1, y + tree_height + 1, z, LEAVES)
    mc.setBlocks(x, y + tree_height + 1, z - 1, x, y + tree_height + 1, z + 1, LEAVES)
    mc.setBlock(x, y + tree_height + 2, z, LEAVES)

    # leaves floors
    leave_height = 2
    leave_width = 5
    h = y + tree_height - leave_height - 1

    while h > y + tree_height / 3:
        create_leave(h, leave_height, leave_width)
        leave_height += 1
        leave_width += 2
        h -= 1 + leave_height


def create_forest():
    """ create a forest at the south of the map"""
    i = 0
    y = Global.ground_height

    # create trees
    while i < 125:
        x = randint(-120, 120)
        z = randint(80, 120)
        if mc.getHeight(x, z) == y:
            create_tree(x, y, z)
            i += 1

    # create touches
    i = 0
    while i < 75:
        x = randint(-120, 120)
        z = randint(90, 127)
        if mc.getBlock(x, y, z) == AIR:
            mc.setBlock(x, y, z, TORCH)
            i += 1


def create_lollipop(x, y, z):
    """create a lollipop"""

    # get random values
    radius = randint(3, 5)
    height = max(radius + 1, randint(3, 5))
    block = choice(Global.color)

    # Create the lollipop stick
    mc.setBlocks(x, y + height, z, x, y, z, ICE)

    # Create the lollipop top
    draw_sphere(x, y + height + radius, z, radius, block)


def create_lollipop_forest():
    """create a lollipop forest at the south of the map"""
    i = 0
    y = Global.ground_height
    while i < 100:
        x = randint(-120, 120)
        z = randint(-10, 90)
        if mc.getHeight(x, z) == y:
            create_lollipop(x, y, z)
            i += 1


def create_cane_candy(x, y, z, candy_data):
    """
            create a cane candy
        x, y, z: position of the first lowest block of cane candy
        candy_data: 3D list to construct cane candy
    """

    for i in xrange(0, len(candy_data)):
        for j in xrange(0, len(candy_data[i])):
            for k in xrange(0, len(candy_data[i][j])):
                if candy_data[i][j][k] is not None:
                    mc.setBlock(x + i, y + j, z + k, candy_data[i][j][k])


def create_cane_candy_forest():
    """create cane candy forest at the north of the map"""

    # read data from file
    try:
        f = open('data/object/cane_candy.txt', 'r')
    except IOError:
        print "Data of cane candy can not be loaded"
        return

    # translate data to blocks and store in 2D list
    data2d = []
    for line in f:
        tmp = []
        for char in line.strip():
            if char == 'W':
                tmp.append(WOOL_WHITE)
            elif char == 'R':
                tmp.append(WOOL_RED)
            else:
                tmp.append(None)
        data2d.append(tmp)

    # reverse data2d so that the candy not up side down
    data2d = data2d[::-1]

    # make the candy 3D
    data3d = []
    for i in xrange(4):
        data3d.append(data2d)

    # make copies of data3d that face north, south, west, east
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

    # a list to choose direction
    direction = [north, south, west, east]

    # create forest
    i = 0
    while i < 100:
        x = randint(-120, 120)
        z = randint(-120, -20)
        if mc.getHeight(x, z) == Global.ground_height:
            y = Global.ground_height + randint(-6, 0)
            create_cane_candy(x, y, z, choice(direction))
            i += 1


####################################################################
#                          Buildings                               #
####################################################################


def create_cupcake_house(x, y, z, r):
    """
            create a cupcake house
        x, y, z: coordinate of house
        r      : radius of the roof
    """

    # roof
    draw_upper_hemisphere(x, y + r, z, r, GLOWSTONE_BLOCK)
    draw_upper_hemisphere(x, y + r, z, r - 1, AIR)
    sleep(r)

    # wall
    color = choice(Global.color)
    for i in xrange(r + 1):
        draw_horizontal_circle_outline(x, y + i, z, r / 2 + i / 2, color)
        if i % 2 == 1:
            draw_horizontal_circle_outline(x, y + i + 1, z, r / 2 + i / 2, TORCH)
    sleep(3)

    # door
    mc.setBlocks(x, y, z, x + r, y + 2, z, AIR)


def create_cupcake_village():
    """create cup cake village in the center of the map"""
    i = 0
    y = Global.ground_height
    x = [58, 90, 77, 97, 0, -16, -77, -97, 6]
    z = [22, -70, 38, -11, 56, 73, -14, -33, 0]
    while i < len(x):
        radius = randint(5, 13)
        create_cupcake_house(x[i], y, z[i], radius)
        i += 1


def create_coke_tower():
    """
        create_coke_tower at the north of the village
    """
    x = 30
    y = Global.ground_height
    z = -70

    # load data from file
    try:
        f = open('data/object/coke_tower.txt', 'r')
    except IOError:
        print "Data of coke tower can not be loaded"
        return

    # dictionary to convert data to block
    block = {
        'W': WOOL_WHITE,
        'R': WOOL_RED,
        'B': WOOL_BLACK,
    }

    # construct coke tower
    for line in f:
        radius, color = line.strip().split(" ")
        radius = int(radius)
        mc.setBlocks(x - radius, y, z - radius, x + radius, y, z + radius, AIR)
        draw_horizontal_circle_outline(x, y, z, radius, block[color])
        y += 1


####################################################################
#                          Underground                             #
####################################################################


def create_maze_floor(floor, x, y, z):
    """
            Create a floor of the maze
        File structure:
        ' '        = air
        '#'        = wall
        '*'        = wall with torch at highest block
        [letter]   = trap

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
        print floor, i
        for j in xrange(len(maze_map[i])):
            # select block type to build
            if maze_map[i][j] == '#' or maze_map[i][j] == '*':
                block = GLOWSTONE_BLOCK
            else:
                block = AIR

            # build
            mc.setBlocks(x + i, y, z + j, x + i, y + Global.floor_height, z + j, block)

            # if '*' then create a torch at the highest block
            # if maze_map[i][j] == '*':
            #     mc.setBlock(x + i, y + Global.floor_height, z + j, TORCH)

            # # if [letter] then create a trap
            if maze_map[i][j] in trap.keys():
                trap[maze_map[i][j]](x + i, y - 1, z + j)

    # create maze entrance room
    mc.setBlocks(x, y, z - 1, x + 7, y + Global.floor_height, z - 7, AIR)

    # create stairs
    for i in xrange(Global.floor_height + 4):
        mc.setBlock(x + 1, y + i, z + Global.floor_height + 3 - i, STAIRS_COBBLESTONE.id, 3)
        mc.setBlocks(x + 1, y + i + 1, z + Global.floor_height + 3 - i,
                     x + 1, y + i + 3, z + Global.floor_height + 3 - i, AIR)


def create_mazes():
    """create floors of the maze"""

    # ---------------- Create maze entrance ------------------- #

    # create cupcake house on an island
    x = -20
    y = Global.ground_height
    z = -80
    mc.setBlocks(x - 7, y - 9, z - 7, x + 7, y - 1, z + 7, GOLD_BLOCK)
    mc.setBlocks(x - 8, y - 9, z - 8, x + 8, y - 2, z + 8, GOLD_BLOCK)
    mc.setBlocks(x - 9, y - 9, z - 9, x + 9, y - 3, z + 9, GOLD_BLOCK)
    create_cupcake_house(x, y, z, 15)

    # create a bridge to the island
    mc.setBlocks(x - 1, y, z - 8, x + 1, y - 1, z - 20, GLASS)

    # create a hole below the floor
    depth = y - 1 - (Global.floor_height + 4) * (Global.number_of_floor + 2)
    mc.setBlocks(x - 1, y - 2, z - 1, x + 1, depth, z + 1, AIR)

    # create a chamber at the end of the hole
    mc.setBlocks(x - 5, depth, z - 5,
                 x + 5, depth - 5, z + 5, AIR)

    # create water in the chamber to catch hansel
    mc.setBlocks(x - 6, depth - 6, z - 6,
                 x + 6, depth - 12, z + 6, GLOWSTONE_BLOCK)
    mc.setBlocks(x - 5, depth - 5, z - 5,
                 x + 5, depth - 11, z + 5, WATER)

    # ---------------------- Create maze ------------------------ #

    x -= 3
    y = depth - 4
    z += 11

    # create mazes
    for i in xrange(1, 1 + Global.number_of_floor):
        create_maze_floor(i, x, y + (i - 1) * (Global.floor_height + 4), z)

    # create GoOutOfMaze trigger
    GoOutOfMaze(x + 1, y + Global.number_of_floor * (Global.floor_height + 4) - 1, z - 1)


# test
if __name__ == "__main__":
    # surface
    print "start"
    clear_world()
    print "ground"
    create_craggy_mountains()
    print "mountain"
    create_river()
    print "river"
    create_corn_candy_mountains()
    print "corn"
    create_ice_cream_hills()
    print "ice cream"
    create_oreos()
    print "oreo"

    create_cupcake_village()
    print "cupcake"
    create_coke_tower()
    print "coke"
    create_forest()
    print "forest"
    create_lollipop_forest()
    print "lollipop"
    create_cane_candy_forest()
    print "cane"

    # underground
    create_mazes()
    print "maze"
    print "done"
