import Global


def draw_horizontal_circle_outline(x0, y, z0, r, block_id, block_data=0):
    """draw a horizontal circle with outline only"""
    f = 1 - r
    ddf_x = 1
    ddf_z = -2 * r
    x = 0
    z = r
    Global.mc.setBlock(x0, y, z0 + r, block_id, block_data)
    Global.mc.setBlock(x0, y, z0 - r, block_id, block_data)
    Global.mc.setBlock(x0 + r, y, z0, block_id, block_data)
    Global.mc.setBlock(x0 - r, y, z0, block_id, block_data)

    while x < z:
        if f >= 0:
            z -= 1
            ddf_z += 2
            f += ddf_z
        x += 1
        ddf_x += 2
        f += ddf_x
        Global.mc.setBlock(x0 + x, y, z0 + z, block_id, block_data)
        Global.mc.setBlock(x0 - x, y, z0 + z, block_id, block_data)
        Global.mc.setBlock(x0 + x, y, z0 - z, block_id, block_data)
        Global.mc.setBlock(x0 - x, y, z0 - z, block_id, block_data)
        Global.mc.setBlock(x0 + z, y, z0 + x, block_id, block_data)
        Global.mc.setBlock(x0 - z, y, z0 + x, block_id, block_data)
        Global.mc.setBlock(x0 + z, y, z0 - x, block_id, block_data)
        Global.mc.setBlock(x0 - z, y, z0 - x, block_id, block_data)


def draw_horizontal_circle(x, y, z, r, block_id, block_data=0):
    """draw a horizontal circle with outline and inside part"""
    r = int(r)
    for i in xrange(-r, r):
        for j in xrange(-r, r):
            if i ** 2 + j ** 2 < r ** 2:
                Global.mc.setBlock(x + i, y, z + j, block_id, block_data)


def draw_sphere(x, y, z, r, block_id, block_data=0):
    """draw a sphere"""
    for i in range(-r, r):
        for j in range(-r, r):
            for k in range(-r, r):
                if i ** 2 + j ** 2 + k ** 2 < r ** 2:
                    Global.mc.setBlock(x + i, y + j, z + k, block_id, block_data)


def draw_upper_hemisphere(x, y, z, r, block_id, block_data=0):
    """draw the upper half of sphere"""
    for i in range(-r, r):
        for j in range(0, r):
            for k in range(-r, r):
                if i ** 2 + j ** 2 + k ** 2 < r ** 2:
                    Global.mc.setBlock(x + i, y + j, z + k, block_id, block_data)
