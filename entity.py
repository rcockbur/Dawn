from globals import *
import pygame, random
print("running entity.py")

class Entity():
    id_index = 0
    name_indexes = dict()
    name_index = 0
    is_manual = False

    def new_id():
        Entity.id_index += 1
        return Entity.id_index - 1

    def new_name(self):
        if self.__class__.__name__ not in Entity.name_indexes:
            Entity.name_indexes[self.__class__.__name__] = 0
        Entity.name_indexes[self.__class__.__name__] += 1
        class_count = Entity.name_indexes[self.__class__.__name__]
        s = str(class_count)
        return self.__class__.__name__ + " " + s

    def __init__(self, tile, born_naturally = True):
        self.id = Entity.new_id()
        MAP.add_entity_at_tile(self, tile)
        self.is_selected = False
        self.is_destroyed = False
        self.tile = tile        
        self.name = self.new_name()
        self.birth = dict()       
        if born_naturally == True:
            for DATE_TYPE in DATE_TYPES:
                self.birth[DATE_TYPE] = current_date[DATE_TYPE]
        else:
            self.birth[DT_HOUR] = random.randint((current_date[DT_YEAR] - 9) * HOURS_PER_YEAR, current_date[DT_YEAR] * HOURS_PER_YEAR - 1)
            self.birth[DT_DAY] = self.birth[DT_HOUR] // HOURS_PER_DAY
            self.birth[DT_MONTH] = self.birth[DT_DAY] // DAYS_PER_MONTH
            self.birth[DT_YEAR] = self.birth[DT_MONTH] // MONTHS_PER_YEAR
            self.birth[DT_HOUR_OD] = self.birth[DT_HOUR] % HOURS_PER_DAY
            self.birth[DT_HOUR_OM] = self.birth[DT_HOUR] % HOURS_PER_MONTH
            self.birth[DT_HOUR_OY] = self.birth[DT_HOUR] % HOURS_PER_YEAR
            self.birth[DT_DAY_OM] = self.birth[DT_DAY] % DAYS_PER_MONTH
            self.birth[DT_DAY_OY] = self.birth[DT_DAY] % DAYS_PER_YEAR
            self.birth[DT_MONTH_OY] = self.birth[DT_MONTH] % MONTHS_PER_YEAR
        self.age = (current_date[DT_DAY] - self.birth[DT_DAY]) // DAYS_PER_YEAR

    def destroy(self):
        destroyed_units.add(self)
        self.is_destroyed = True

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def get_tile_string(self):
        return str(self.tile[0]) + " , " + str(self.tile[1])