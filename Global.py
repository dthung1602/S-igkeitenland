"""
    This file contains shared variables and constants
"""

import os

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

GROUND_HEIGHT = 0

FLOOR_HEIGHT = 6
NUMBER_OF_FLOOR = 3

# buttons
A = 5
B = 6
C = 13
D = 19
E = 26

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


######################################
#             Functions              #
######################################


def output_message(message):
    # display text
    mc.postToChat(message)

    # read the message
    os.system("espeak -ven+f3 -s120 -k10 \"" + message + "\" &>/dev/null")
