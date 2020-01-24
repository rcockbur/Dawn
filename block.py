from globals import *

from entity import Entity

print("running block.py")

class Block(Entity):
    
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = COLOR_GREY_DARK
        self.radius = UNIT_RADIUS_BLOCK


