from globals import *
import random
from entity import Entity
print("running block.py")

class Block(Entity):

    radius = UNIT_RADIUS_BLOCK
    
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = COLOR_BLOCK


class Grass(Entity):
    def __init__(self, tile):
        Entity.__init__(self, tile, born_naturally = True)
        self.color_eaten = (0, 50, 0)
        self.color_grown = (0, 100, 0)
        self.__class__.radius = UNIT_RADIUS_BLOCK
        self.crop_max = 300
        self.crop_current = random.randint(0, self.crop_max)

        if self.crop_current == self.crop_max:
            self.color = self.color_grown
        else:
            self.color = self.color_eaten

        self.is_marked = False
        self.marked_at = -100000

    def update(self):
        if current_date[DT_HOUR_OD] == self.birth[DT_HOUR_OD]:
            if self.is_marked == True:
                if current_date[DT_DAY] - self.marked_at > 20:
                    self.is_marked = False
                    self.marked_at = -1000
        
            if self.crop_current < self.crop_max:
                self.crop_current = min(self.crop_current + 8, self.crop_max)
            if self.crop_current >= self.crop_max:
                self.color = self.color_grown
            else:
                self.color = self.color_eaten

    def can_be_eaten(self):
        return self.crop_current > 0

    def can_be_hunted(self):
        return self.crop_current == self.crop_max and self.is_marked == False

    def get_marked_string(self):
        if self.is_marked:
            return "Yes"
        else:
            return "No"

    # returns a satiation amount, and a bool whether there is more to eat
    def eaten(self, amount):
        amount = min(amount, self.crop_current)
        self.crop_current -= amount

        if self.crop_current <= 0:
            return (amount, False)
        return (amount, True)



    def mark(self):
        self.marked_at = current_date[DT_DAY]
        self.is_marked = True

    def destroy(self):
        if self.is_dead == False:
            self.die()
        destroyed_units.add(self)
        self.is_destroyed = True


    def die(self):
        self.is_dead = True








