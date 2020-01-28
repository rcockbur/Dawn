from globals import *
import random
from entity import Entity

print("running block.py")

class Block(Entity):
    
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = COLOR_BLOCK
        self.radius = UNIT_RADIUS_BLOCK


class Grass(Entity):
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = (0, 100, 0) 
        self.color_eaten = (0, 50, 0)
        self.color_grown = (0, 100, 0)
        self.radius = UNIT_RADIUS_BLOCK
        self.crop_max = 100
        self.crop_current = random.randint(self.crop_max / 2, self.crop_max)


    def update(self):
                    # check hunger  
        if sim_ticks[0] % 30 == 0:
            if self.crop_current < self.crop_max:
                self.crop_current += 1

        if self.crop_current == self.crop_max:
            self.color = self.color_grown
        else:
            self.color = self.color_eaten

    def eaten(self):
        self.crop_current = 0


    def die(self):
        dead_units.add(self)
        self.is_dead = True








