from globals import *
import pygame, random
from utility import measure
from path import Path
import pathfinding
from map import calculate_rect
from entity import Entity
from block import Block

print("running unit.py")

class Unit(Entity):

    def init_a(self, tile):
        Entity.__init__(self, tile)
        self.is_dead = False
        self.is_manual = False
        self.path = Path()
        self.kills = 0
        self.satiation_current = 200
        self.satiation_max = 200
        self.idle_min = 1000 # after completing path
        self.idle_max = 2000
        self.move_range_min = 60
        self.move_range_max = 60
        self.move_period = 5
        self.move_current = 0
        # self.idle_current = random.randint(0, self.idle_max)
        self.idle_current = random.randint(1, 100)
        self.kill_types = {}

        self.patience_max = 20
        self.patience_current = self.patience_max
        
    def init_b(self, tile):
        self.move_current = self.move_period
        self.color = self.satiation_color
        self.color_original = self.color

    def die(self):
        dead_units.add(self)
        self.is_dead = True

    def update(self):
        self.going_to_move = False

        if self.is_dead == False:
            testing_my_patiece = False

            # check hunger  
            if frames[0] % 20 == 0:
                if self.satiation_current > 0:
                    self.satiation_current -= 1
                    self.color = self.satiation_color
                else:
                    self.color = self.hungery_color
            # generate new target if empty
            if self.path.size() == 0 and self.is_manual == False:
                if self.idle_current == 0:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                    if self.is_manual == False:
                        self.update_target()
                else:
                    self.idle_current = self.idle_current - 1

            # we ran into something
            elif self.path.size() > 0:
                unit = MAP.get_entity_at(self.path.points[0])
                
                if type(unit) in self.kill_types:
                    self.kill_unit(unit)
                
                if type(unit) in self.block_move_types:
                    if self.is_manual == True:
                        testing_my_patiece = True
                    else:
                        self.update_target()
                        print(self.name, "blocked by", unit.name, "@", frames[0])
            
            if testing_my_patiece == True:
                self.patience_current = self.patience_current - 1
                if self.patience_current == 0:
                    self.path.clear()
                    self.patience_current = self.patience_max
                    print(self.name, "lost patience with", unit.name, "@", frames[0])
            else:
                self.patience_current = self.patience_max


            # move if ready
            
            if self.path.size() > 0:
                if testing_my_patiece == False and self.move_current < 1:
                    self.going_to_move = True
                    self.move_current = self.move_period
            self.move_current = self.move_current - 1 

    def update_2(self):
        if self.going_to_move:
            self.move()


    def move(self):
        target = self.path.points[0]
        if MAP.tile_within_bounds(target) == False:
            print (self.name, "tried to move of bounds")
            return False
        unit = MAP.get_entity_at(target)
        if type(MAP.get_entity_at(target)) in self.block_move_types:
            print(self.name, "tried to move onto", unit.name)
            return False
        self.path.pop()
        old_tile = self.tile.copy()
        self.tile = target.copy()
        MAP.move_entity(self, old_tile, self.tile)
        return True
          
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def print(self):
        print("--Unit id: ", self.id, "  x: ", self.tile.x, "  y: ", self.tile.y)

    def kill_unit(self, unit):
        self.color = self.satiation_color
        self.satiation_current = self.satiation_max
        self.kills += 1
        unit.die()
        

class Deer(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (160, 70, 0)
        self.satiation_color = (100, 40, 0)
        self.radius = UNIT_RADIUS_DEER
        self.block_move_types = { Block, Deer, Wolf, Person }
        self.block_pathing_types = { Block, Deer, Wolf, Person }
        Unit.init_b(self, tile)

    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path


class Wolf(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (255, 151, 151)
        self.satiation_color = (191, 191, 191)
        self.radius = UNIT_RADIUS_WOLF
        self.block_move_types = { Block, Wolf, Person }
        self.block_pathing_types = { Block, Wolf, Person }
        self.kill_types = { Deer }
        Unit.init_b(self, tile)

    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path



class Person(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (175, 35, 255)
        self.satiation_color = (35, 35, 255)
        self.radius = UNIT_RADIUS_PERSON
        self.move_distance = 20
        self.is_manual = True
        self.kill_types = { Deer, Wolf }
        self.block_pathing_types = { Block }
        self.block_move_types = { Block, Person }
        Unit.init_b(self, tile)

