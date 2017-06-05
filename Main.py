#! /usr/bin/env python
# coding=utf-8

"""
                Project Minecraft - Süßigkeitenland
    Course : English for Computer Science, Vietnamese German University
    Team   : 1 
    Group  : CD
    Members:    Nguyen Cong Dat,    Duong Thanh HUng
                Huynh Vinh Long,    Le Hong Thang
    Due day: --/06/2017
    Description: a MineCraft world based on “Hansel and Gretel” of the Brothers Grimm
    Connection:
    Reference: minecraftstuff package from www.github.com/martinohanlon/minecraft-stuff
               It is used to create basic shapes (circle, line, sphere, etc)
"""

import RPi.GPIO as GPIO

import Global
from World import *


def main():
    #######################################
    #             Set up GPIO             #
    #######################################

    # setup GPIO mode
    GPIO.setmode(GPIO.BOARD)

    # setup pin mode
    GPIO.setup(Global.A, GPIO.IN)
    GPIO.setup(Global.B, GPIO.IN)
    GPIO.setup(Global.C, GPIO.IN)
    GPIO.setup(Global.D, GPIO.IN)

    #######################################
    #             Create world            #
    #######################################

    # surface
    create_ground()
    create_craggy_mountains()
    create_corn_candy_mountains()
    create_river()
    create_ice_cream_hills()
    create_oreos()
    create_cupcake_village()
    create_coke_tower()
    create_forest()
    create_lollipop_forest()
    create_cane_candy_forest()

    # underground
    create_mazes()

    #######################################
    #            Main game loop           #
    #######################################

    # move player to the initial position
    # TODO set init pos
    Global.mc.player.setTilePos(100, 100, 100)

    # loop
    while not Global.end_game:
        # update info
        Global.update_position()

        # check triggers
        for trig in Global.triggers:
            if trig.condition():
                trig.action()
                if trig.one_time:
                    Global.triggers.remove(trig)


if __name__ == "__main__":
    main()
