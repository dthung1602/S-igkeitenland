#!/usr/bin/env python

"""
    This file contains a function responsible for moving player around the word
    and a function to record player position
"""

from Trap import *
from signal import SIGINT, signal
import sys
import Global

delay = 0.075
init_hansel_pos = Vec3(105, 0, 127)

count = 0


def take_a_tour():
    """ move player around the map to show he/she the world"""
    # setup
    global delay, init_hansel_pos
    hansel = Global.hansel

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
    global count
    for line in f:
        # get values from a line of text
        data = line.strip()
        x, y, z = data.split()

        # display message
        if count in message.keys():
            mc.postToChat(message[count])
        count += 1

        # convert to number
        x = float(x)
        y = float(y)
        z = float(z)

        hansel.setPos(x, y, z)
        sleep(delay * 2)

    # by this time the player is already on the trap
    # push player into maze
    x, y, z = hansel.getTilePos()
    mc.setBlocks(x - 1, y, z - 1,
                 x + 1, y - 1, z + 1, AIR)

    # print message
    sleep(2)
    mc.postToChat("It's look like that you have fall into the trap of the evil witch!")
    sleep(3)
    mc.postToChat("You must solve the maze to get to the ground. There's no other way around")


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
    global delay
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
        sleep(delay)


# test
if __name__ == '__main__':
    create_a_tour()
