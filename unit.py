from globals import *
import pygame, random
from utility import measure
from path import Path
import pathfinding
from map import calculate_rect
from entity import Entity
from block import Block, Grass

print("running unit.py")

class Unit(Entity):

    def init_a(self, tile):
        Entity.__init__(self, tile)
        
        self.is_manual = False
        self.path = Path()
        self.kills = 0
        self.satiation_max = 100
        self.satiation_current = random.randint(0, self.satiation_max)
        self.idle_min = 1000 # after completing path
        self.idle_max = 2000
        self.move_range_min = 20
        self.move_range_max = 40
        self.move_period = 10
        self.move_current = 0
        self.status = IDLE
        self.idle_current = random.randint(0, self.idle_max / 2)
        # self.idle_current = random.randint(1, 100)
        self.kill_types = {}
        self.eats_grass = False

        self.patience_max = 50
        self.patience_current = self.patience_max
        
    def init_b(self, tile):
        self.move_current = self.move_period
        self.color = self.satiation_color
        self.color_original = self.color


    def update(self):
        self.going_to_move = False

        if self.is_dead == False:
            is_blocked = False

            # check hunger  
            if frames[0] % 20 == 0:
                if self.satiation_current > 0:
                    self.satiation_current -= 1
                    self.color = self.satiation_color
                else:
                    self.color = self.hungery_color

            # automatic unit is out of path - reset idle if first time without path, update path if idle has counted down, count down idle
            if self.path.size() == 0 and self.is_manual == False:
                if self.status == MOVING:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                else:
                    if self.idle_current == 0:
                        if self.is_manual == False:
                            self.update_target()
                    else:
                        self.idle_current = self.idle_current - 1
            # we ran into something
            if self.path.size() > 0:
                unit = MAP.get_entity_at(self.path.points[0])
                if type(unit) == Grass and self.eats_grass == True and unit.crop_current == unit.crop_max:
                    self.eat_grass(unit)
                if type(unit) in self.kill_types:
                    self.kill_unit(unit)
                if type(unit) in self.block_move_types:
                    is_blocked = True
            # we are blocked
            if is_blocked == True:
                self.patience_current = self.patience_current - 1
                if self.patience_current == 0:
                    self.patience_current = self.patience_max  
                    self.path.clear()
                    # print(self.name, "lost patience with", unit.name, "@", frames[0])
            else:
                self.patience_current = self.patience_max
            # move if ready
            if self.path.size() > 0:
                self.status = MOVING
                if is_blocked == False and self.move_current < 1:
                    # self.going_to_move = True
                    self.move()
                    self.move_current = self.move_period
            else:
                self.status = IDLE
            self.move_current = max(self.move_current - 1, 0)


    def get_target_string(self):
        if self.path.size() > 0:
            return str(self.path.get(0).x) + " , " + str(self.path.get(0).y)
        return "-"

    def get_status_string(self):
        if self.status == IDLE:
            return "Idle"
        elif self.status == MOVING:
            return "Moving"
        else:
            return "error"

    def get_hungery_string(self):
        if self.satiation_current == 0:
            return "Yes"
        return "No"



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
        print(self.name, "killed", unit.name)
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
        self.block_move_types = { Block, Deer, Wolf, Person, Grass }
        self.block_pathing_types = { Block, Deer, Wolf, Person, Grass }
        self.idle_min = 50 # after completing path
        self.idle_max = 75
        self.kill_types = {}
        self.move_range_min = 20
        self.move_range_max = 40
        self.eats_grass = True
        Unit.init_b(self, tile)

    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)

        if self.satiation_current == 0 and random.randint(1, 1) == 1:
            tile = pathfinding.find_nearby_entity(self.tile, self.block_pathing_types, self.move_range_max, {Grass}, True, debug_search_food)
            if tile is not None:
                print(self.name, "found grass")
        else:
            tile = None

        if tile is None:
            tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range, debug_search_tile)

        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types, debug_pathfinding)
            self.path = path

    def eat_grass(self, grass):
        self.satiation_current = self.satiation_max
        grass.eaten()



class Wolf(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (255, 151, 151)
        self.satiation_color = (191, 191, 191)
        self.radius = UNIT_RADIUS_WOLF
        self.block_move_types = { Block, Wolf, Person, Grass }
        self.block_pathing_types = { Block, Wolf, Person, Grass }
        self.kill_types = { Deer }
        self.idle_min = 500 # after completing path
        self.idle_max = 1000
        Unit.init_b(self, tile)

    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)

        
        if random.randint(1, 1) == 1 and self.satiation_current == 0:
            tile = pathfinding.find_nearby_entity(self.tile, self.block_pathing_types, move_range, self.kill_types, False, debug_search_food)
        else:
            tile = None

        if tile is None:
            tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range, debug_search_tile)

        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types, debug_pathfinding)
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

