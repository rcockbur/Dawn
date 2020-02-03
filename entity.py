from globals import *
import pygame, random
print("running entity.py")

class Entity():
    id_index = 0
    name_indexes = dict()
    name_index = 0

    def new_id():
        Entity.id_index += 1
        return Entity.id_index - 1

    def new_name(self):
        if self.class_name not in Entity.name_indexes:
            Entity.name_indexes[self.class_name] = 0

        Entity.name_indexes[self.class_name] += 1
        return self.class_name + " " + str(Entity.name_indexes[self.class_name])

    def __init__(self, tile):
        self.id = Entity.new_id()
        MAP.add_entity_at_tile(self, tile)
        self.is_selected = False
        self.is_dead = False
        self.tile = tile
        self.class_name = type(self).__name__
        self.name = self.new_name()
        self.dies_when_eaten = False

    def die(self):
        dead_units.add(self)
        self.is_dead = True

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def get_tile_string(self):
        return str(self.tile[0]) + " , " + str(self.tile[1])