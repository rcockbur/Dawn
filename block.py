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
        self.food_value = 25
        self.crop_current = random.randint(self.crop_max, self.crop_max)
        self.is_marked = False
        self.marked_at = -100000

    def update(self):
        if day[0] % 8 == 0:
            if self.is_marked == True:
                if day[0] - self.marked_at > 100:
                    self.is_marked = False
                    self.marked_at = -1000


            if self.crop_current < self.crop_max:
                self.crop_current += 1
        if self.crop_current == self.crop_max:
            self.color = self.color_grown
        else:
            self.color = self.color_eaten

    def can_be_eaten(self):
        return self.crop_current == self.crop_max

    def can_be_hunted(self):
        return self.crop_current == self.crop_max and self.is_marked == False

    def get_marked_string(self):
        if self.is_marked:
            return "Yes"
        else:
            return "No"

    def eaten(self):
        self.crop_current = 0
        self.is_marked = False
        self.marked_at = -1000

    def mark(self):
        self.marked_at = day[0]
        self.is_marked = True

    def die(self):
        dead_units.add(self)
        self.is_dead = True








