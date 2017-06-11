#!/usr/bin/env python

"""
    This file contains definitions of all traps in the maze
"""

from time import *

import RPi.GPIO as GPIO

import Global
from Draw import draw_sphere
from mcpi.block import *
from mcpi.vec3 import *

mc = Global.mc


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
        mc.setBlock(x, y, z, self.block)

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
        mc.setBlock(x, y, z, self.block)

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
        mc.postToChat(self.message)


class Riddle(TriggerComeClose):
    riddle_num = 0
    number_of_riddle = 5

    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 3, DIAMOND_BLOCK.id, 0, True)

        # load riddle from file
        try:
            f = open("./data/riddle/riddle" + str(Riddle.riddle_num) + ".txt", "r")
        except IOError:
            print "Data of riddle %d can not be loaded" % Riddle.riddle_num
            return

        Riddle.riddle_num = Riddle.riddle_num + 1 if Riddle.riddle_num < Riddle.number_of_riddle - 1 else 0

        # set values
        self.riddle = f.readline().strip()
        self.answer = f.readline().strip()
        print self.riddle + "#"
        print self.answer + "#"

    @staticmethod
    def button_pressed():
        """return player's answer"""
        # print GPIO.input(Global.A)
        # print GPIO.input(Global.B)
        # print GPIO.input(Global.C)
        # print GPIO.input(Global.D)
        # print "----------------------"
        # return None
        if not GPIO.input(Global.A):
            return "A"
        if not GPIO.input(Global.B):
            return "B"
        if not GPIO.input(Global.C):
            return "C"
        if not GPIO.input(Global.D):
            return "D"
        return None

    @staticmethod
    def wrong():
        """what happens when player's answer is incorrect"""
        mc.postToChat("Wrong! You will die")

        # build a wall surround player
        x = Global.x_surround
        z = Global.z_surround
        for i in xrange(8):
            mc.setBlocks(Global.tilePos.x + x[i], Global.tilePos.y, Global.tilePos.z + z[i],
                         Global.tilePos.x + x[i], Global.tilePos.y + 2, Global.tilePos.z + z[i], LAVA_STATIONARY)

    @staticmethod
    def right():
        """what happens when player's answer is correct"""
        mc.postToChat("Correct! You may go")

        # build a wall surround player
        x = Global.x_surround
        z = Global.z_surround
        for i in xrange(8):
            mc.setBlocks(Global.tilePos.x + x[i], Global.tilePos.y, Global.tilePos.z + z[i],
                         Global.tilePos.x + x[i], Global.tilePos.y + 2, Global.tilePos.z + z[i], AIR)

    def action(self):
        # build a wall surround player
        Global.hansel.setPos(Global.tilePos.x, Global.tilePos.y, Global.tilePos.z)
        x = Global.x_surround
        z = Global.z_surround
        for i in xrange(8):
            mc.setBlocks(Global.tilePos.x + x[i], Global.tilePos.y, Global.tilePos.z + z[i],
                         Global.tilePos.x + x[i], Global.tilePos.y + 2, Global.tilePos.z + z[i], GLASS)

        # show player the riddle
        mc.postToChat("RIDDLE: " + self.riddle)

        # check for answer
        while True:
            answer = self.button_pressed()
            if answer is not None:
                if answer == self.answer:
                    self.right()
                else:
                    self.wrong()
                break
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
        mc.setBlocks(self.pos.x, self.pos.y - 2, self.pos.z,
                     self.pos.x, self.depth, self.pos.z, AIR)

    def action(self):
        mc.setBlock(Global.tilePos.x, Global.tilePos.y - 1, Global.tilePos.z, AIR)


class FallIntoLavaTrap(FallTrap):
    """player fall into lava"""

    def __init__(self, x, y, z):
        FallTrap.__init__(self, x, y, z, 2, GRASS.id, 0, True)
        mc.setBlock(x, self.depth, z, LAVA)


class PushBackTrap(TriggerComeClose):
    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 4, WOOL.id, 0, False)
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
        TriggerStepOn.__init__(self, x, y, z, BRICK_BLOCK.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        mc.setBlock(x + 2, y, z, LAVA)
        mc.setBlock(x + 3, y, z, STONE)
        mc.setBlock(x - 2, y, z, LAVA)
        mc.setBlock(x - 3, y, z, STONE)


class FlowLavaBlockWayZ(TriggerStepOn):
    """block both z directions with lava"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, BRICK_BLOCK.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        mc.setBlock(x, y, z + 2, LAVA)
        mc.setBlock(x, y, z + 3, STONE)
        mc.setBlock(x, y, z - 2, LAVA)
        mc.setBlock(x, y, z - 3, STONE)


class StoneBlockWayX(TriggerStepOn):
    """block x ways with rising blocks"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, LEAVES.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        for i in xrange(4):
            mc.setBlock(x + 5, y, z, STONE_BRICK)
            mc.setBlock(x - 5, y, z, STONE_BRICK)
            y += 1
            sleep(2)


class StoneBlockWayZ(TriggerStepOn):
    """block z ways with rising blocks"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, LEAVES.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        for i in xrange(4):
            mc.setBlock(x, y, z + 3, STONE_BRICK)
            mc.setBlock(x, y, z - 3, STONE_BRICK)
            y += 1
            sleep(3)


class FallSand(TriggerStepOn):
    """ sand fall on player's head"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, SAND.id, 0, True)

    def action(self):
        mc.setBlocks(Global.pos.x - 5, Global.pos.y + 4, Global.pos.z - 5,
                     Global.pos.x + 5, Global.pos.y + 4, Global.pos.z + 5, SAND)


class TrapInHoleX(TriggerStepOn):
    """trap you in a hole with closing door"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, MOSS_STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        mc.setBlocks(x - 5, y - 1, z, x + 5, y - 3, z, AIR)
        sleep(2)
        for i in xrange(-5, 6):
            mc.setBlock(x + i, y - 1, z, 89)
            sleep(1)


class TrapInHoleZ(TriggerStepOn):
    """trap you in a hole with closing door"""

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, MOSS_STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        mc.setBlocks(x, y - 1, z - 5, x, y - 3, z + 5, AIR)
        sleep(2)
        for i in xrange(-5, 6):
            mc.setBlock(x, y - 1, z + i, 89)
            sleep(1)


class GoOutOfMaze(TriggerStepOn):
    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, GLASS, one_time=False)
        mc.setBlocks(x, y + 1, z, x, y + 5, z, AIR)

    def action(self):
        Global.escape = True
        x, y, z = self.pos
        x += 1

        # build stairs
        while y < Global.GROUND_HEIGHT:
            mc.setBlock(x, y, z, STAIRS_COBBLESTONE, 1)
            mc.setBlocks(x, y + 1, z, x, y + 3, z, AIR)
            mc.setBlock(x, y + 4, z, GLASS)
            sleep(0.05)
            y += 1
            x += 1

        # build path lead to final trap
        mc.setBlocks(x - 12, y - 8, z - 1, x + 20, y + 8, z - 1, GLASS)  # wall on the left
        mc.setBlocks(x - 12, y - 8, z + 1, x + 20, y + 8, z + 1, GLASS)  # wall on the right
        mc.setBlocks(x - 11, y, z, x + 20, y + 8, z, AIR)  # air between
        mc.setBlocks(x, y - 1, z, x + 20, y - 1, z, GOLD_BLOCK)  # block to walk on
        mc.setBlocks(x - 12, y - 8, z - 1, x - 12, y + 8, z + 1, GLASS)  # wall at the back

        # add final trap
        Global.triggers = []
        draw_sphere(x + 26, y + 5, z, 3, REDSTONE_ORE)
        FinalTrap(x + 26, y + 5, z)


###################################################################################
#                                   Final trap                                    #
###################################################################################

class FinalTrap(TriggerComeClose):
    def __init__(self, x, y, z):
        TriggerComeClose.__init__(self, x, y, z, 7, GOLD_BLOCK)

    def condition(self):
        return Global.escape and self.distance() < self.d

    def action(self):
        # end python program
        Global.end_game = True

        length = 30
        depth = 7

        # build the wall of the hole
        mc.setBlocks(Global.tilePos.x - 10, Global.tilePos.y - depth, Global.tilePos.z - 10,
                     Global.tilePos.x + length, Global.tilePos.y - 1, Global.tilePos.z + 10, STONE_BRICK)

        # fill air
        mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y - depth, Global.tilePos.z - 9,
                     Global.tilePos.x + length - 1, Global.tilePos.y - 1, Global.tilePos.z + 9, AIR)

        mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y, Global.tilePos.z - 9,
                     Global.tilePos.x + length - 1, Global.tilePos.y + 50, Global.tilePos.z + 9, AIR)

        # fill lava
        mc.setBlocks(Global.tilePos.x - 9, Global.tilePos.y - depth - 2, Global.tilePos.z - 10,
                     Global.tilePos.x + length + 10, Global.tilePos.y - depth, Global.tilePos.z + 10, LAVA)

        # make a bridge
        mc.setBlocks(Global.tilePos.x - 3, Global.tilePos.y - 1, Global.tilePos.z,
                     Global.tilePos.x + length - 3, Global.tilePos.y - 1, Global.tilePos.z, GRASS)

        # show message and wait for player to read
        mc.postToChat("You have been told NOT to enter the Coke tower. Now you must pay. RUN")
        sleep(3)

        # start destroying the bridge. if player jump to land then make a hole
        hole = Vec3(Global.tilePos.x + length + 1, Global.tilePos.y, Global.tilePos.z)
        t = time()
        delay = 0.5
        count = 0

        while mc.player.getTilePos() != hole and count < length - 2:
            if time() - t > delay:
                mc.setBlock(Global.tilePos.x - 3 + count, Global.tilePos.y - 1, Global.tilePos.z, SAND)
                if count > 5:
                    mc.setBlock(Global.tilePos.x - 3 + count - 5, Global.tilePos.y - depth, Global.tilePos.z,
                                AIR)
                count += 1
                t = time()

        mc.setBlocks(hole.x - 1, hole.y, hole.z - 1, hole.x + 1, hole.y - 6, hole.z + 1, AIR)


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
    # Global.escape = True
    # f = FinalTrap(x + 10, y + 1, z)

    # setup GPIO mode
    GPIO.setmode(GPIO.BCM)

    # setup pin mode
    GPIO.setup(Global.A, GPIO.IN)
    GPIO.setup(Global.B, GPIO.IN)
    GPIO.setup(Global.C, GPIO.IN)
    GPIO.setup(Global.D, GPIO.IN)

    Riddle(x, y, z + 5)

    while len(Global.triggers) > 0:
        # update info
        Global.pos = Global.hansel.getPos()
        Global.tilePos = Global.hansel.getTilePos()

        # check triggers
        for trig in Global.triggers:
            if trig.condition():
                trig.action()
                if trig.one_time:
                    Global.triggers.remove(trig)
