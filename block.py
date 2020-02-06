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
        self.crop_max = 10
        self.food_value = 370
        self.crop_current = random.randint(0, self.crop_max)
        self.is_marked = False
        self.marked_at = -100000
        

        self.birth_tick = random.randint((START_YEAR - 10) * TICKS_PER_YEAR, START_YEAR * TICKS_PER_YEAR)
        self.birth_day = self.birth_tick // TICKS_PER_DAY
        self.birth_month = self.birth_day // DAYS_PER_MONTH
        self.birth_year = self.birth_month // MONTHS_PER_YEAR
        self.birth_tick_of_day = self.birth_tick % TICKS_PER_DAY
        self.birth_tick_of_month = self.birth_tick % TICKS_PER_MONTH
        self.birth_tick_of_year = self.birth_tick % TICKS_PER_DAY
        self.birth_day_of_month = self.birth_day % DAYS_PER_MONTH
        self.birth_day_of_year = self.birth_day % DAYS_PER_YEAR
        self.birth_month_of_year = self.birth_month % MONTHS_PER_YEAR
        self.age = (day[0] - self.birth_day) // DAYS_PER_YEAR

    def update(self):
        if tick_of_day[0] == self.birth_tick_of_day:
            if self.is_marked == True:
                if day[0] - self.marked_at > 100:
                    self.is_marked = False
                    self.marked_at = -1000
            if day_of_month[0] == self.birth_day_of_month:
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








