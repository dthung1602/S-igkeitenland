#!/usr/bin/env python

"""
    This file contains a function responsible for moving player around the word
    and a function to record player position
"""

import sys
from signal import SIGINT, signal

import Global
from Trap import *

record_delay = 0.075
init_hansel_pos = Vec3(105, 0, 127)


def take_a_tour():
    """ move player around the map to show he/she the world"""
    # setup
    global record_delay, init_hansel_pos
    hansel = Global.hansel
    number_of_step = 5
    play_back_delay = record_delay / number_of_step * 1.5

    # move player to init position
    hansel.setTilePos(init_hansel_pos.x, init_hansel_pos.y, init_hansel_pos.z)

    # open file to read
    try:
        f = open("data/tour/tour.txt", "r")
        g = open("data/tour/message.txt", "r")
    except IOError:
        print "Data of tour can not be loaded"
        return

    # read messages from g
    # each line of g: [position to display message]: [message]
    message = {}  # a dictionary maps a number to a message to display
    for line in g:
        data = line.strip().split(": ")
        pos = int(data[0])
        mes = data[1]
        message[pos] = mes

    # move player around the map
    count = 0
    for line in f:
        # get values from a line of text
        data = line.strip()
        x, y, z = data.split()

        # display message and read it
        if count in message.keys():
            Global.output_message(message[count])
        count += 1

        # vec3 points from current position to new position
        movement = Vec3(float(x), float(y), float(z)) - hansel.getPos()

        # divide movement to steps
        step = movement / number_of_step

        # move hansel
        old_pos = hansel.getPos()

        for i in xrange(number_of_step):
            new_pos = old_pos + step
            hansel.setPos(new_pos.x, new_pos.y, new_pos.z)
            sleep(play_back_delay)

    # by this time the player is already on the trap
    # push player into maze
    x, y, z = hansel.getTilePos()
    mc.setBlocks(x - 1, y, z - 1,
                 x + 1, y - 1, z + 1, AIR)

    # print message
    sleep(5)
    Global.output_message("It's look like that you have fall into the trap of the evil witch!")

    sleep(5)
    Global.output_message("You must solve the maze to get to the ground. There's no other way around")


def create_a_tour():
    """
        record player position in the world until CTRL_C is pressed
        create a text file that function take_a_tour can use to move player around
    """

    def signal_handler(*args):
        """function to save string to file when interrupt signal is received (CTRL_C is pressed)"""
        # open file to write
        try:
            f = open("data/tour/tour.txt", "w")
        except IOError:
            print "Data file of tour can not be created"
            sys.exit(1)

        # save x, y, z to file
        for i in xrange(len(x)):
            line = " ".join((str(x[i]), str(y[i]), str(z[i])))
            f.write(line + "\n")

        f.close()
        print "Saved to file"
        sys.exit(0)

    # setup
    global record_delay
    hansel = Global.hansel
    signal(SIGINT, signal_handler)

    x = []
    y = []
    z = []

    # move player to init position
    hansel.setTilePos(init_hansel_pos.x, init_hansel_pos.y, init_hansel_pos.z)

    # wait for player to move to another place to avoid division by 0
    sleep(2)

    # record
    while True:
        position = hansel.getPos()
        x.append(position.x)
        y.append(position.y)
        z.append(position.z)
        print str(len(x)) + "  " + str(position)
        sleep(record_delay)


# test
if __name__ == '__main__':
    create_a_tour()
