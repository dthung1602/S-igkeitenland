# coding=utf-8

import utility
from mcpi.block import *
from mcpi.vec3 import *


#################################################
#         Base classes for all triggers         #
#################################################

class TriggerStepOn(object):
    """Base class for blocks that trigger an event when it is step on"""

    def __init__(self, x, y, z, block_type, block_data=0, one_time=True):
        # set values
        self.pos = Vec3(x, y + 1, z)
        self.block = Block(block_type, block_data)
        self.one_time = one_time

        # add self to triggers list
        utility.triggers.append(self)

        # set block under trigger block to correct type
        utility.mc.setBlock(x, y, z, self.block)

    def condition(self):
        """check if hansel steps on block"""
        if self.pos == utility.tilePos:
            return True
        return False

    def action(self):
        pass


class TriggerComeClose(object):
    """Base class for blocks that trigger an event when hansel is close enough"""

    def __init__(self, x, y, z, d, block_type, block_data=0, one_time=True):
        # set values
        self.pos = Vec3(x, y, z)
        self.block = Block(block_type, block_data)
        self.one_time = one_time
        self.d = d

        # add self to triggers list
        utility.triggers.append(self)

    def distance(self):
        return (self.pos - utility.pos).length()

    def condition(self):
        """check if hansel is close enough"""
        if self.distance() < self.d:
            return True
        return False

    def action(self):
        pass


#################################################
#                    Messages                   #
#################################################

class Message(TriggerComeClose):
    """Base class for showing message to player"""

    def __init__(self, x, y, z, message, d=2, block_type=0, block_data=0, one_time=True):
        TriggerComeClose.__init__(self, x, y, z, d, block_type, block_data, one_time)
        self.message = message

    def action(self):
        utility.mc.postToChat(self.message)


################################################
#              Traps in the maze               #
################################################

# -------------------Falling------------------ #
class FallTrap(TriggerStepOn):
    def __init__(self, x, y, z, depth, block_type, block_data=0, one_time=True):
        TriggerStepOn.__init__(self, x, y, z, block_type, block_data, one_time)
        self.depth = self.pos.y - depth

        # create a hole
        utility.mc.setBlocks(self.pos.x, self.pos.y - 2, self.pos.z,
                             self.pos.x, self.depth, self.pos.z, AIR)

    def action(self):
        utility.mc.setBlock(utility.tilePos.x, utility.tilePos.y - 1, utility.tilePos.z, AIR)


class FallIntoMazeTrap(FallTrap):
    """This will open a hole under Hansel and he 
    will fall into the lowest level of the maze"""

    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, 10 * utility.number_of_floor, STONE.id, 0, True)

        # create a chamber at the end of the hole
        utility.mc.setBlocks(utility.pos.x - 5, self.depth, utility.pos.z - 5,
                             utility.pos.x + 5, self.depth - 5, utility.pos.z + 5, AIR)

        # create water in the chamber to catch hansel
        utility.mc.setBlocks(utility.pos.x - 5, self.depth - 5, utility.pos.z - 5,
                             utility.pos.x + 5, self.depth - 10, utility.pos.z + 5, WATER)


class FallIntoLavaTrap(FallTrap):
    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, 3, STONE.id, 0, True)
        utility.mc.setBlock(x, self.depth, z, LAVA)

################################################
#                 Final trap                   #
################################################
