"""
    Provide common utilities for program
"""
from mcpi import minecraft
from mcpi import minecraftstuff

######################################
#         Important variables        #
######################################

mc = minecraft.Minecraft.create()
draw = minecraftstuff.MinecraftDrawing(mc)
hansel = mc.player
pos = hansel.getPos()
tilePos = hansel.getTilePos()
triggers = []

######################################
#              Constants             #
######################################

ground_height = 0
number_of_floor = 3


######################################
#              Functions             #
######################################

def update_info():
    global hansel, pos, tilePos
    pos = hansel.getPos
    tilePos = hansel.getTilePos
