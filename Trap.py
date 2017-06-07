# coding=utf-8

from random import choice
from time import *

import RPi.GPIO as GPIO

from Draw import draw_sphere
import Global
from mcpi.block import *
from mcpi.vec3 import *


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

        # set block under trigger block to correct type
        Global.mc.setBlock(x, y, z, self.block)

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
#                           Messages & Riddles                                    #
###################################################################################


class Message(TriggerComeClose):
    """Base class for showing message to player"""

    def __init__(self, x, y, z, message, d=2, block_type=0, block_data=0, one_time=True):
        TriggerComeClose.__init__(self, x, y, z, d, block_type, block_data, one_time)
        self.message = message

    def action(self):
        Global.mc.postToChat(self.message)


class Riddle(TriggerComeClose):
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
                choice(trap.keys())
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
#                                 Traps in the maze                               #
###################################################################################


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
        FallTrap.__init__(self, x, y, z, (Global.floor_height + 4) * (Global.number_of_floor + 2), STONE.id, 0, True)

        # create a chamber at the end of the hole
        Global.mc.setBlocks(Global.pos.x - 5, self.depth, Global.pos.z - 5,
                            Global.pos.x + 5, self.depth - 5, Global.pos.z + 5, AIR)

        # create water in the chamber to catch hansel
        Global.mc.setBlocks(Global.pos.x - 6, self.depth - 6, Global.pos.z - 6,
                            Global.pos.x + 5, self.depth - 12, Global.pos.z + 6, GLOWSTONE_BLOCK)
        Global.mc.setBlocks(Global.pos.x - 5, self.depth - 5, Global.pos.z - 5,
                            Global.pos.x + 5, self.depth - 12, Global.pos.z + 5, WATER)


class FallIntoLavaTrap(FallTrap):
    """player fall into lava"""

    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, 3, STONE.id, 0, True)
        Global.mc.setBlock(x, self.depth, z, LAVA)


class PushBackTrap(TriggerComeClose):
    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 4, WOOL_ORANGE.id, 0, False)
        self.old_pos = None

    @staticmethod
    def move_player(vec3):
        new_pos = vec3 + Global.hansel.getPos()
        Global.hansel.setPos(new_pos.x, new_pos.y, new_pos.z)
        sleep(0.01)

    def action(self):
        if self.old_pos is None and self.distance() > self.d / 2:
            self.old_pos = Global.pos
        else:
            step = self.old_pos - Global.pos
            for i in xrange(10):
                self.move_player(step)
            self.old_pos = None


class FlowLavaBlockWayX(TriggerStepOn):
    """block both x directions with lava"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlock(x + 5, y, z, LAVA)
        Global.mc.setBlock(x + 6, y, z, STONE)
        Global.mc.setBlock(x - 5, y, z, LAVA)
        Global.mc.setBlock(x - 6, y, z, STONE)


class FlowLavaBlockWayZ(TriggerStepOn):
    """block both z directions with lava"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlock(x, y, z + 5, LAVA)
        Global.mc.setBlock(x, y, z + 6, STONE)
        Global.mc.setBlock(x, y, z - 5, LAVA)
        Global.mc.setBlock(x, y, z - 6, STONE)


class StoneBlockWayX(TriggerStepOn):
    """block x ways with rising blocks"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        for i in xrange(4):
            Global.mc.setBlock(x + 5, y, z, STONE_BRICK)
            Global.mc.setBlock(x - 5, y, z, STONE_BRICK)
            y += 1
            sleep(2)


class StoneBlockWayZ(TriggerStepOn):
    """block z ways with rising blocks"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        for i in xrange(4):
            Global.mc.setBlock(x, y, z + 3, STONE_BRICK)
            Global.mc.setBlock(x, y, z - 3, STONE_BRICK)
            y += 1
            sleep(3)


class FallSand(TriggerStepOn):
    """ sand fall on player's head"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        Global.mc.setBlocks(Global.pos.x - 5, Global.pos.y + 4, Global.pos.z - 5,
                            Global.pos.x + 5, Global.pos.y + 4, Global.pos.z + 5, SAND)


class TrapInHoleX(TriggerStepOn):
    """trap you in a hole with closing door"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlocks(x - 5, y - 1, z, x + 5, y - 3, z, AIR)
        sleep(2)
        for i in xrange(-5, 6):
            Global.mc.setBlock(x + i, y - 1, z, 89)
            sleep(1)


class TrapInHoleZ(TriggerStepOn):
    """trap you in a hole with closing door"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlocks(x, y - 1, z - 5, x, y - 3, z + 5, AIR)
        sleep(2)
        for i in xrange(-5, 6):
            Global.mc.setBlock(x, y - 1, z + i, 89)
            sleep(1)


class GoOutOfMaze(TriggerComeClose):
    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 7, GLASS)

    def action(self):
        Global.escape = True
        x, y, z = self.pos

        # open the way out
        while y < Global.ground_height:
            Global.mc.setBlock(x, y, z, STAIRS_COBBLESTONE, 1)
            Global.mc.setBlocks(x, y + 1, z, x, y + 3, z, AIR)
            y += 1
            x += 1

        # build path lead to final trap
        Global.mc.setBlocks(x - 5, y, z - 1, x - 4, y + 8, z + 1, GLASS)
        Global.mc.setBlocks(x - 5, y, z - 1, x + 15, y + 8, z - 1, GLASS)
        Global.mc.setBlocks(x - 5, y, z + 1, x + 15, y + 8, z + 1, GLASS)

        # room to contain final trap
        Global.mc.setBlocks(x + 15, y, z - 5, x + 25, y + 8, z + 5, GLASS)
        Global.mc.setBlocks(x + 16, y, z - 4, x + 24, y + 8, z + 4, AIR)
        Global.mc.setBlocks(x + 15, y, z, x + 24, y + 8, z, AIR)

        # add final trap
        draw_sphere(x + 20, y + 3, z, 3, GOLD_BLOCK)
        # f = FinalTrap(x + 20, y + 1, z)
        # f.action()


###################################################################################
#                                   Final trap                                    #
###################################################################################

class FinalTrap(TriggerComeClose):
    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 5, GOLD_BLOCK)

    def condition(self):
        return Global.escape and self.distance() < self.d

    def action(self):
        # end python program
        Global.end_game = True

        length = 30
        depth = 7

        # build the wall of the hole
        Global.mc.setBlocks(Global.tilePos.x - 10, Global.tilePos.y - depth, Global.tilePos.z - 10,
                            Global.tilePos.x + length, Global.tilePos.y - 1, Global.tilePos.z + 10, STONE_BRICK)

        # fill air
        Global.mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y - depth, Global.tilePos.z - 9,
                            Global.tilePos.x + length - 1, Global.tilePos.y - 1, Global.tilePos.z + 9, AIR)

        Global.mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y, Global.tilePos.z - 9,
                            Global.tilePos.x + length - 1, Global.tilePos.y + 8, Global.tilePos.z + 9, AIR)

        # fill lava
        Global.mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y - depth - 2, Global.tilePos.z - 10,
                            Global.tilePos.x + length + 10, Global.tilePos.y - depth, Global.tilePos.z + 10, LAVA)

        # make a bridge
        Global.mc.setBlocks(Global.tilePos.x - 3, Global.tilePos.y - 1, Global.tilePos.z,
                            Global.tilePos.x + length - 3, Global.tilePos.y - 1, Global.tilePos.z, GRASS)

        # show message and wait for player to read
        Global.mc.postToChat("Valar Morghulis\nYou should run now.")
        sleep(3)

        # start destroying the bridge. if player jump to land then make a hole
        hole = Vec3(Global.tilePos.x + length + 1, Global.tilePos.y, Global.tilePos.z)
        t = time()
        delay = 0.5
        count = 0

        while Global.mc.player.getTilePos() != hole and count < length - 5:
            if time() - t > delay:
                Global.mc.setBlock(Global.tilePos.x - 3 + count, Global.tilePos.y - 1, Global.tilePos.z, SAND)
                count += 1
                t = time()

        Global.mc.setBlocks(hole.x - 1, hole.y, hole.z - 1, hole.x + 1, hole.y - 6, hole.z + 1, AIR)


# a dictionary to convert letter to trap
trap = {
    'a': FallIntoLavaTrap,
    'b': PushBackTrap,
    'c': FlowLavaBlockWayX,
    'D': FlowLavaBlockWayZ,
    'e': StoneBlockWayX,
    'F': StoneBlockWayZ,
    'g': FallSand,
    'h': TrapInHoleX,
    'I': TrapInHoleZ,

}

# test
if __name__ == '__main__':
    x, y, z = Global.tilePos
    y -= 1
    # FallTrap(x, y, z + 3, 5, BRICK_BLOCK)
    # FallIntoLavaTrap(x + 3, y, z)
    # PushBackTrap(x - 3, y + 1, z - 5)
    # Riddle(x - 6, y + 1, z + 5)
    # FlowLavaBlockWayX(x + 6, y, z)
    # FlowLavaBlockWayZ(x, y, z + 6)
    # StoneBlockWayX(x + 6, y, z)
    # StoneBlockWayZ(x, y, z + 6)
    # FallSand(x, y, z + 5)
    # TrapInHoleX(x + 5, y, z)
    # TrapInHoleZ(x, y, z + 5)
    Global.escape = True
    f = FinalTrap(x + 10, y + 1, z)

    while len(Global.triggers) > 0:
        # update info
        Global.pos = Global.hansel.getPos()
        Global.tilePos = Global.hansel.getTilePos()

        print Global.tilePos, "  **"

        # check triggers
        for trig in Global.triggers:
            print trig.pos
            if trig.condition():
                trig.action()
                if trig.one_time:
                    Global.triggers.remove(trig)
        print "------------------------------------\n\n"
