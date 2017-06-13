#!/usr/bin/env python
# coding=utf-8

"""
                    Minecraft World - Süßigkeitenland
    Course : English for Computer Science, phase 4, Vietnamese German University
    Team   : 1 
    Group  : CD
    Members:    Nguyen Cong Dat,    Duong Thanh Hung
                Huynh Vinh Long,    Le Hong Thang
    Due day: 15/06/2017
    Description: a MineCraft world based on “Hansel and Gretel” of the Brothers Grimm
    Connection:
    Reference: minecraftstuff package from www.github.com/martinohanlon/minecraft-stuff
               A modified version of it is used to create basic shapes (circle, line, sphere, etc)
"""

import RPi.GPIO as GPIO

from World import *
from Tour import *


def main():
    #######################################
    #             Set up GPIO             #
    #######################################

    # setup GPIO mode
    GPIO.setmode(GPIO.BCM)

    # setup pin mode
    GPIO.setup(Global.A, GPIO.IN)
    GPIO.setup(Global.B, GPIO.IN)
    GPIO.setup(Global.C, GPIO.IN)
    GPIO.setup(Global.D, GPIO.IN)
    GPIO.setup(Global.E, GPIO.IN)

    #######################################
    #             Create world            #
    #######################################

    # clear_world()
    #
    # # terrance
    # create_craggy_mountains()
    # create_river()
    # create_corn_candy_mountains()
    # create_ice_cream_hills()
    # create_oreos()
    #
    # # forests
    # create_forest()
    # create_lollipop_forest()
    # create_cane_candy_forest()
    #
    # # buildings
    # create_cupcake_village()
    # create_coke_tower()

    # underground
    create_mazes()

    #######################################
    #            Main game loop           #
    #######################################

    # move player around to see the world
    # take_a_tour()

    # loop to activate traps in maze
    while not Global.end_game:
        # update position of player
        Global.pos = Global.hansel.getPos()
        Global.tilePos = Global.hansel.getTilePos()

        # check triggers
        for trigger in Global.triggers:
            if trigger.condition():
                trigger.action()
                if trigger.one_time:
                    Global.triggers.remove(trigger)


if __name__ == "__main__":
    main()
