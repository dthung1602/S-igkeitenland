#!/usr/bin/env python

"""
    This file contains a function responsible for moving player around the word
    and a function to record player position
"""

from Trap import *
from signal import SIGINT, signal
import sys
import Global

record_delay = 0.75
init_hansel_pos = Vec3(-90, 0, 127)


def take_a_tour():
    """ move player around the map to show he/she the world"""

    # setup
    global record_delay, init_hansel_pos
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

    # how long each step is
    step_length = 0.1

    # move player around the map
    count = 0
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

        # a vector from current position to the new position
        movement = Vec3(x, y, z) - hansel.getPos()

        if movement.length() > 0:
            # a vector from current position to the new destination with the length of 1
            step = movement / movement.length()
            # change vector's length
            step *= step_length
        else:
            # stand still
            step = Vec3(0, 0, 0)

        # move player
        number_of_step = int(movement.length() / step_length)
        play_back_delay = 0.05 if number_of_step == 0 else record_delay / number_of_step / 2
        for i in xrange(number_of_step):
            new_pos = hansel.getPos() + step
            hansel.setPos(new_pos.x, new_pos.y, new_pos.z)
            sleep(play_back_delay)

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
