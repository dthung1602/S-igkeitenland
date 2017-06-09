from World import *
from mcpi.minecraft import *
from time import time

mc = Minecraft.create()
hansel = mc.player
x, y, z = hansel.getTilePos()
y -= y

clear_world()

create_maze_floor(3, x + 1, y, z + 5)

t = time()
while len(Global.triggers):
    # update info
    Global.pos = Global.hansel.getPos()
    Global.tilePos = Global.hansel.getTilePos()
    new = time()
    print new - t, "=======================================================", len(Global.triggers)
    print "                   ", Global.tilePos

    # check triggers
    for trig in Global.triggers:
        print trig.pos
        if trig.condition():
            trig.action()
            if trig.one_time:
                Global.triggers.remove(trig)
