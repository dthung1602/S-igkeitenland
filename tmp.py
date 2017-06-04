class FlowLavaBlockWay_x(TriggerStepOn):
    """
    block both directions w/ lava(change x)
    """

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


class FlowLavaBlockWay_z(TriggerStepOn):
    """
    block both directions w/ lava(change z)
    """

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


class StoneBlockWay_x(TriggerStepOn):
    """
    block ways w/ rising blocks (change x)
    """

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


class StoneBlockWay_z(TriggerStepOn):
    """
    block ways w/ rising blocks (change z)
    """

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
    """
    sand fall on ur head
    """

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        Global.mc.setBlock(Global.pos.x, Global.pos.y + 3, Global.pos.z, SAND)


class TrapInHole_x(TriggerStepOn):
    """
    trap you in a hole with closing door (change x)
    """

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlocks(x, y - 1, z, x + 5, y - 3, z, AIR)
        sleep(3)
        for i in xrange(6):
            Global.mc.setBlock(x, y - 1, z, 89)
            x += 1
            sleep(1)


class TrapInHole_z(TriggerStepOn):
    """
    trap you in a hole with closing door (change x)
    """

    def __init__(self, x, y, z):
        TriggerStepOn.__init__(self, x, y, z, STONE.id, 0, True)

    def action(self):
        x = Global.pos.x
        y = Global.pos.y
        z = Global.pos.z
        Global.mc.setBlocks(x, y - 1, z, x, y - 3, z + 5, AIR)
        sleep(3)
        for i in xrange(6):
            Global.mc.setBlock(x, y - 1, z, 89)
            z += 1
            sleep(1)
