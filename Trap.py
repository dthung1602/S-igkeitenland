# coding=utf-8

import Global
from mcpi.block import *
from mcpi.vec3 import *
from time import *
import RPi.GPIO as GPIO


###################################################################################
#                           Base classes for all triggers                         #
###################################################################################


class TriggerStepOn(object):
    """Base class for blocks that trigger an event when it is step on"""

    def __init__(self, x, y, z, block_type, block_data=0, one_time=True):
        # set values
        self.pos = Vec3(x, y + 1, z)
        self.block = Block(block_type, block_data)
        self.one_time = one_time

        # add self to triggers list
        Global.triggers.append(self)

        # set block under trigger block to correct type
        Global.mc.setBlock(x, y, z, self.block)

    def condition(self):
        """check if hansel steps on block"""
        if self.pos == Global.tilePos:
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
        Global.triggers.append(self)

    def distance(self):
        return (self.pos - Global.pos).length()

    def condition(self):
        """check if hansel is close enough"""
        if self.distance() < self.d:
            return True
        return False

    def action(self):
        pass


###################################################################################
#                                    Messages                                     #
###################################################################################


class Message(TriggerComeClose):
    """Base class for showing message to player"""

    def __init__(self, x, y, z, message, d=2, block_type=0, block_data=0, one_time=True):
        TriggerComeClose.__init__(self, x, y, z, d, block_type, block_data, one_time)
        self.message = message

    def action(self):
        Global.mc.postToChat(self.message)


###################################################################################
#                                 Traps in the maze                               #
###################################################################################


# ------------------------------------------------------------------------------- #
#                                      Falling                                    #
# ------------------------------------------------------------------------------- #


class FallTrap(TriggerStepOn):
    def __init__(self, x, y, z, depth, block_type, block_data=0, one_time=True):
        TriggerStepOn.__init__(self, x, y, z, block_type, block_data, one_time)
        self.depth = self.pos.y - depth

        # create a hole
        Global.mc.setBlocks(self.pos.x, self.pos.y - 2, self.pos.z,
                            self.pos.x, self.depth, self.pos.z, AIR)

    def action(self):
        Global.mc.setBlock(Global.tilePos.x, Global.tilePos.y - 1, Global.tilePos.z, AIR)


class FallIntoMazeTrap(FallTrap):
    """This will open a hole under Hansel and he 
    will fall into the lowest level of the maze"""

    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, (Global.floor_height + 4) * Global.number_of_floor, STONE.id, 0, True)

        # create a chamber at the end of the hole
        Global.mc.setBlocks(Global.pos.x - 5, self.depth, Global.pos.z - 5,
                            Global.pos.x + 5, self.depth - 5, Global.pos.z + 5, AIR)

        # create water in the chamber to catch hansel
        Global.mc.setBlocks(Global.pos.x - 6, self.depth - 6, Global.pos.z - 6,
                            Global.pos.x + 5, self.depth - 12, Global.pos.z + 6, GLOWSTONE_BLOCK)
        Global.mc.setBlocks(Global.pos.x - 5, self.depth - 5, Global.pos.z - 5,
                            Global.pos.x + 5, self.depth - 12, Global.pos.z + 5, WATER)


class FallIntoLavaTrap(FallTrap):
    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, 3, STONE.id, 0, True)
        Global.mc.setBlock(x, self.depth, z, LAVA)


# ------------------------------------------------------------------------------- #
#                                       Riddle                                    #
# ------------------------------------------------------------------------------- #

class Riddle(TriggerComeClose):
    # TODO read 'static var'
    riddle_num = 0
    number_of_riddle = 5

    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 3, STONE.id, STONE.data, False)

        # load riddle from file
        f = open("./data/riddle/riddle" + str(Riddle.riddle_num) + ".txt", "r")
        Riddle.riddle_num = Riddle.riddle_num + 1 if Riddle.riddle_num < Riddle.number_of_riddle - 1 else 0

        # set values
        self.riddle = f.readline().replace("\\n", "\n")
        self.answer = f.readline()

        # set blocks to stop hansel
        Global.mc.setBlocks(self.pos.x, self.pos.y, self.pos.z,
                            self.pos.x, self.pos.y + 3, self.pos.z, STONE_BRICK)

    @staticmethod
    def button_pressed():
        """return player's answer"""
        if GPIO.input(Global.A):
            return "A"
        if GPIO.input(Global.B):
            return "B"
        if GPIO.input(Global.C):
            return "C"
        if GPIO.input(Global.D):
            return "C"
        return None

    @staticmethod
    def wrong():
        """what happens when player's answer is incorrect"""
        Global.mc.postToChat("Wrong!")
        for x in Global.x_surround:
            for z in Global.z_surround:
                # TODO choose some random trap
                FallIntoLavaTrap(Global.pos.x + x, Global.pos.y, Global.pos.z + z)

    def right(self):
        """what happens when player's answer is correct"""
        Global.mc.postToChat("Correct! You may go")
        Global.mc.setBlocks(self.pos.x, self.pos.y, self.pos.z,
                            self.pos.x, self.pos.y + 3, self.pos.z, AIR)

    def action(self):
        # show player the riddle
        Global.mc.postToChat("RIDDLE: " + self.riddle)

        # check for answer 5 continuous times, with delay time
        for i in xrange(5):
            bt = self.button_pressed()
            if bt is not None:
                if bt != self.answer:
                    self.wrong()
                else:
                    self.right()
                Global.triggers.remove(self)
            else:
                sleep(0.1)


###################################################################################
#                                   Final trap                                    #
###################################################################################
class FinalTrap(TriggerComeClose):
    def __init__(self):
        TriggerComeClose.__init__(self, 10, 10, 10, 5, AIR)

    def condition(self):
        return Global.escape and self.distance() < self.d

    def action(self):
        # end python program
        Global.end_game = True

        # build the wall of the hole
        Global.mc.setBlocks(Global.tilePos.x - 10, Global.tilePos.y - 5, Global.tilePos.z - 10,
                            Global.tilePos.x + 10, Global.tilePos.y - 1, Global.tilePos.z + 10, STONE_BRICK)

        # fill air
        Global.mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y - -5, Global.tilePos.z - 9,
                            Global.tilePos.x + 9, Global.tilePos.y - 1, Global.tilePos.z + 9, AIR)

        # fill lava
        Global.mc.setBlocks(Global.tilePos.x - 10, Global.tilePos.y - 10, Global.tilePos.z - 10,
                            Global.tilePos.x + 10, Global.tilePos.y - 5, Global.tilePos.z + 10, LAVA)

        # make a bridge
        Global.mc.setBlocks(Global.tilePos.x, Global.tilePos.y - 1, Global.tilePos.z,
                            Global.tilePos.x + 8, Global.tilePos.y - 1, Global.tilePos.z, GRASS)

        # show message and wait for player to read
        Global.mc.postToChat("Valar Morghulis\nYou should run now.")
        sleep(2)

        # start destroying the bridge. if player jump to land then make a hole
        hole = Vec3(Global.tilePos.x + 11, Global.tilePos.y, Global.tilePos.z)
        t = time()
        count = 0

        while Global.mc.player.getTilePos() != hole and count < 10:
            if time() - t > 500:
                Global.mc.setBlock(Global.tilePos.x + count, Global.tilePos.y - 1, Global.tilePos.z, SAND)
                count += 1
                t = time()

        Global.mc.setBlocks(hole.x - 1, hole.y, hole.z - 1, hole.x + 1, hole.y - 6, hole.z + 1, AIR)
