from globals import *

from entity import Entity

print("running block.py")

class Block(Entity):
    
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = COLOR_GREY_DARK
        self.radius = UNIT_RADIUS_BLOCK


class Grass(Entity):
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = (0, 100, 0) 
        self.color_eaten = (0, 50, 0)
        self.color_grown = (0, 100, 0)
        self.radius = UNIT_RADIUS_BLOCK
        self.remaining_crop = 1

    def eaten(self):
        self.remaining_crop = 0
