from globals import *
from entity import Entity
import random
print("running block.py")

def link_types():
    static_entity_types.add(Block)
    static_entity_types.add(Grass)

class Block(Entity):
    radius = UNIT_RADIUS_BLOCK
    
    def __init__(self, tile):
        Entity.__init__(self, tile)
        self.color = COLOR_BLOCK


class Grass(Entity):
    color_eaten = (0, 50, 0)
    color_grown = (0, 100, 0)
    radius = UNIT_RADIUS_BLOCK
    crop_max = 500

    def __init__(self, tile):
        Entity.__init__(self, tile, born_naturally = True)
        self.crop_current = random.randint(0, self.__class__.crop_max)
        self.is_marked = False
        self.marked_until_d = 0
        if self.crop_current == self.__class__.crop_max: self.color = self.__class__.color_grown
        else: self.color = self.__class__.color_eaten

    def update(self):
        if current_date[DT_HOUR_OD] == self.birth[DT_HOUR_OD]:
            if self.is_marked == True and current_date[DT_DAY] >= self.marked_until_d:
                self.is_marked = False
            if self.crop_current < self.__class__.crop_max:
                self.crop_current = min(self.crop_current + 8, self.__class__.crop_max)
            if self.crop_current >= self.__class__.crop_max:
                self.color = self.__class__.color_grown
            else:
                self.color = self.__class__.color_eaten

    def can_be_eaten(self):
        return self.crop_current > 0

    def can_be_hunted(self):
        return self.crop_current == self.__class__.crop_max and self.is_marked == False

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
        self.marked_until_d = current_date[DT_DAY] + 20
        self.is_marked = True

    def die(self):
        self.is_dead = True


link_types()


