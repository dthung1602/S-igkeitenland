"""
    This file contains shared variables and constants
"""

from mcpi import minecraft
from mcpi.block import *

######################################
#         Important variables        #
######################################

mc = minecraft.Minecraft.create()
hansel = mc.player
pos = hansel.getPos()
tilePos = mc.player.getTilePos()

triggers = []

escape = False
end_game = False

######################################
#              Constants             #
######################################

ground_height = 0

floor_height = 6
number_of_floor = 3

# buttons
A = 1
B = 2
C = 3
D = 4

# list to loop through 8 surrounding blocks of player
x_surround = [1, 1, 1, 0, -1, -1, -1, 0]
z_surround = [-1, 0, 1, 1, 1, 0, -1, -1]

# a list to save block color
color = [
    WOOL_WHITE,
    WOOL_ORANGE,
    WOOL_MAGENTA,
    WOOL_LIGHT_BLUE,
    WOOL_YELLOW,
    WOOL_LIME,
    WOOL_PINK,
    WOOL_LIGHT_GREY,
    WOOL_CYAN,
    WOOL_PURPLE,
    WOOL_BLUE,
    WOOL_BROWN,
    WOOL_GREEN,
    WOOL_RED,
]
