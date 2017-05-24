#! /usr/bin/env python
# coding=utf-8
# TODO style guide

"""
                Project Minecraft - Süßigkeitenland
    Course : English for Computer Science 
    Team   : 1 
    Group  : CD
    Members:    Nguyen Cong Dat,    Duong Thanh HUng
                Huynh Vinh Long,    Le Hong Thang
    Due day: --/06/2017 
    
"""

from World import *
import utility


def main():

    #######################################
    #             Create world            #
    #######################################

    # surface
    create_ground()
    create_craggy_mountains()
    create_forest()
    create_corn_candy_mountains()
    create_river()
    create_ice_cream_hills()
    create_lollipop_forest()
    create_cane_candy_forest()
    create_oreos()
    create_cupcake_village()
    create_coke_tower()

    # underground
    create_mazes()
    create_ladder_rooms()
    create_mobs()

    #######################################
    #            Main game loop           #
    #######################################

    # move player to the initial position
    # TODO set init pos
    utility.hansel.setTilePos(100, 100, 100)

    # loop
    while len(utility.triggers) > 0:
        # update info
        utility.update_info()

        # check triggers
        for trig in utility.triggers:
            if trig.condition():
                trig.action()
                if trig.one_time:
                    utility.triggers.remove(trig)


if __name__ == "__main__":
    main()
