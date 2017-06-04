from mcpi import minecraft

######################################
#         Important variables        #
######################################

mc = minecraft.Minecraft.create()
hansel = mc.player
pos = hansel.getPos()
tilePos = mc.player.getTilePos()

triggers = []

escape = False
end_game = False

######################################
#              Constants             #
######################################

ground_height = 0

floor_height = 6
number_of_floor = 3

# buttons
A = 1
B = 2
C = 3
D = 4

# list to loop through surrounding blocks of player
x_surround = [1, 1, 1, 0, -1, -1, -1, 0]
z_surround = [-1, 0, 1, 1, 1, 0, -1, -1]


######################################
#              Functions             #
######################################

def update_position():
    global hansel, pos, tilePos
    pos = hansel.getPos
    tilePos = hansel.getTilePos
