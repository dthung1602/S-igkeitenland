#! /usr/bin/env python
# coding=utf-8

# TODO select material

from copy import deepcopy
from math import sqrt
from random import randint

from Draw import *
from Trap import *
from mcpi.minecraft import Minecraft

mc = Minecraft.create()


####################################################################
#                            Surface                               #
####################################################################


def create_ground():
    """clear sky and create ground"""

    # ground
    mc.setBlocks(127, Global.ground_height, 127, -128, -64, -128, 2)

    # air
    mc.setBlocks(127, 63, 127, -128, Global.ground_height, -128, 0)


def create_craggy_mountains():
    """create tall mountains surround the land"""

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
        mountain_width = max(randint(-1, 1) + mountain_width, 10)
        snow_height += randint(-2, 2)
        for z in xrange(-128 + mountain_width, -128, -1):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)

    # western mountains
    for z in xrange(-128, 128):
        height = randint(min_init_height, max_init_height)
        mountain_width = max(randint(-1, 1) + mountain_width, 10)
        snow_height += randint(-2, 2)
        for x in xrange(-128 + mountain_width, -128, -1):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)

    # eastern mountains
    for z in xrange(-128, 128):
        height = randint(min_init_height, max_init_height)
        mountain_width = max(randint(-1, 1) + mountain_width, 10)
        snow_height += randint(-2, 2)
        for x in xrange(128 - mountain_width, 128):
            mc.setBlocks(x, y, z, x, y + height, z, GRASS)
            if height > snow_height:
                mc.setBlock(x, y + height + 1, z, SNOW)
            height += randint(min_height_inc, max_height_inc)


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
    while i < 125:
        x = randint(-120, 120)
        z = randint(80, 120)
        if mc.getHeight(x, z) == y:
            create_tree(x, y, z)
            i += 1


def create_corn_mountain(x, y, z, h, r):
    """
            create a corn candy mountain with a parabola shape
        x, y, z: position of center of lowest layer of the mountain
        h      : height
        r      : radius of the base of the mountain
    """

    for i in range(0, h):
        if i < h / 3:
            color = WOOL
        elif i < 2 * h / 3:
            color = STONE
        else:
            color = GRASS
        draw_horizontal_circle(x, y + i, z, r * sqrt(1 - (y * 1.0 + i) / (y + h)), color)


def create_corn_candy_mountains():
    """ create a forest at the south of the map"""
    i = 0
    y = Global.ground_height
    x = []
    z = []
    while i < len(x):
        height = randint(40, 50)
        radius = randint(15, 25)
        create_corn_mountain(x[i], y, z[i], height, radius)
        i += 1


def create_river():
    """create a chocolate river"""

    # origin of the river
    x0 = 85 - 128
    z = 50 - 128

    # read data from file and create river
    f = open("data/candy/river.txt")
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


def create_ice_cream_hills():
    """create ice cream hills at the west of the map"""
    i = 0
    y = Global.ground_height
    x = []
    z = []
    while i < len(x):
        r = randint(20, 30)
        block = choice(Global.color)
        draw_upper_hemisphere(x, y, z, r, block)
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
        x = randint(-90, 110)
        z = randint(0, 90)
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
    f = open('data/candy/cane_candy.txt', 'r')

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
    y = Global.ground_height
    while i < 75:
        x = randint(-20, 110)
        z = randint(-110, 0)
        if mc.getHeight(x, z) == y:
            create_cane_candy(x, y, z, choice(direction))
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
        draw_horizontal_circle(x, y + 3 + i, z, r - 1, SNOW_BLOCK)
    for i in xrange(w):
        draw_horizontal_circle(x, y + 6 + i, z, r, COAL_ORE)


def create_oreos():
    """create oreos at the east of the map"""
    i = 0
    y = Global.ground_height
    x = []
    z = []
    while i < len(x):
        radius = randint(10, 20)
        width = randint(2, 4)
        create_oreo(x[i], y, z[i], radius, width)


def create_cupcake_house(x, y, z, r):
    """
            create a cupcake house
        x, y, z: coordinate of house
        r      : radius of the roof
    """

    # roof
    draw_upper_hemisphere(x, y + r, z, r, GLOWSTONE_BLOCK)
    sleep(r / 3.0)  # wait for minecraft to finish rendering
    draw_upper_hemisphere(x, y + r, z, r - 1, AIR)
    sleep(r / 3.0)  # wait for minecraft to finish rendering

    # wall
    for i in xrange(r + 1):
        draw_horizontal_circle_outline(x, y + i, z, r / 2 + i / 2, STONE)
        if i % 2 == 1:
            draw_horizontal_circle_outline(x, y + i + 1, z, r / 2 + i / 2, TORCH)


def create_cupcake_village():
    """create cup cake village in the center of the map"""
    i = 0
    y = Global.ground_height
    x = []
    z = []
    while i < len(x):
        radius = randint(3, 9)
        create_cupcake_house(x[i], y, z[i], radius)


def create_coke_tower():
    """
        create_coke_tower at the north of the village
    """
    x = 20
    y = Global.ground_height
    z = -20

    # load data from file
    f = open('data/candy/coke_tower.txt', 'r')

    # dictionary to convert data to block
    block = {
        'W': WOOL,
        'R': BRICK_BLOCK,
        'B': STONE
    }

    # construct coke tower
    for line in f:
        radius, color = line.strip().split(" ")
        draw_horizontal_circle_outline(x, y, z, int(radius), block[color])
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

            # if [letter] then create a trap
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
    y = Global.triggers[0].depth - 10
    z = Global.triggers[0].pos.z + 11

    # create mazes
    for i in xrange(1, 1 + Global.number_of_floor):
        create_maze_floor(i, x, y + (i - 1) * (Global.floor_height + 4), z)

        # cover teh


# test
if __name__ == "__main__":
    create_river()
    print "river"
    exit()

    # surface
    print "start"
    create_ground()
    print "ground"
    create_craggy_mountains()
    print "mountain"
    create_corn_candy_mountains()
    print "corn"
    create_river()
    print "river"
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
    FallIntoMazeTrap(0, 0, 0)
    create_mazes()
    print "maze"
    print "done"
