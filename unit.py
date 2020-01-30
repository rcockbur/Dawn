from globals import *
import pygame, random
from utility import measure
from path import Path
from pathfinding import get_path
from map import calculate_rect
from entity import Entity
from block import Block, Grass
print("running unit.py")

class Unit(Entity):
    next_unit_is_male = True

    def get_gender():
        r = Unit.next_unit_is_male
        Unit.next_unit_is_male = not Unit.next_unit_is_male
        return r

    def init_a(self, tile):
        Entity.__init__(self, tile)
        self.is_manual = False
        self.path = Path()
        self.kills = 0
        self.satiation_max = 100
        self.satiation_min = -200
        self.idle_min = 5
        self.idle_max = 20
        self.move_range_min = 15
        self.move_range_max = 30
        self.move_period = 3
        self.move_current = 0
        self.status = IDLE
        self.kill_types = {}
        self.eats_grass = False
        self.patience_max = 10
        self.is_male = Unit.get_gender()
        if self.is_male == False:
            self.is_fertile = False
            self.pregnant_with = None
            self.pregnant_at = None
        
    def init_b(self, tile):
        self.move_current = self.move_period
        self.color = self.satiation_color
        self.color_original = self.color
        self.patience_current = self.patience_max
        self.satiation_current = random.randint(0, self.satiation_max)
        self.idle_current = random.randint(0, self.idle_max)


    def update(self):
        self.going_to_move = False

        if self.is_dead == False:
            is_blocked = False

            # check hunger  
            if sim_ticks[0] % 8 == 0:
                if self.satiation_current > self.satiation_min:
                    self.satiation_current -= 1
                    if self.satiation_current > 0:
                        self.color = self.satiation_color
                    else:
                        self.color = self.hungery_color
                else:
                    print(self.name, "died of starvation")
                    self.die()
                    return

            # check fertility
            if sim_ticks[0] % 8 == 0 and self.is_male == False and self.is_fertile == False:
                if random.randint(0, 100) == 0:
                        self.is_fertile = True    

            # update target if automatic, out of path, and idle_current is out
            if self.is_manual == False:
                if self.status == IDLE and self.idle_current == 0:
                    self.update_target()
                    
            # check whats right in front of us
            if self.path.size() > 0:
                entity = MAP.get_entity_at_tile(self.path.points[0])
                if type(entity) == Grass and self.eats_grass == True and entity.crop_current == entity.crop_max:
                    self.eat_grass(entity)
                if type(self) == type(entity) and self.is_male == False and entity.is_male == True and self.is_fertile:
                    self.sex(entity)
                if type(entity) in self.kill_types:
                    self.kill_entity(entity)
                if type(entity) in self.block_move_types:
                    is_blocked = True

            # we are blocked
            if is_blocked == True:
                self.patience_current = self.patience_current - 1
                if self.patience_current == 0:
                    self.patience_current = self.patience_max  
                    self.path.clear()
                    # print(self.name, "lost patience with", entity.name, "@", sim_ticks[0])
            else:
                self.patience_current = self.patience_max

            # move if ready
            if self.path.size() > 0:
                self.status = MOVING
                if is_blocked == False and self.move_current == 0:
                    self.move()
                    self.move_current = self.move_period
            else:
                if self.status == MOVING:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                self.status = IDLE
                self.idle_current = max(self.idle_current - 1, 0)
            self.move_current = max(self.move_current - 1, 0)

    def get_target_string(self):
        if self.path.size() > 0:
            return str(self.path.get(0)[0]) + " , " + str(self.path.get(0)[1])
        return "-"

    def get_status_string(self):
        if self.status == IDLE:
            return "Idle"
        elif self.status == MOVING:
            return "Moving"
        else:
            return "error"

    def get_hungery_string(self):
        if self.satiation_current < 1:
            return "Yes"
        return "No"

    def get_gender_string(self):
        if self.is_male:
            return "Male"
        return "Female"

    def get_fertile_string(self):
        if self.is_fertile:
            return "Yes"
        else:
            return "No"

    def move(self):
        target = self.path.points[0]
        if MAP.tile_within_bounds(target) == False:
            print (self.name, "tried to move of bounds")
            return False
        entity = MAP.get_entity_at_tile(target)
        if entity is not None:

            if type(MAP.get_entity_at_tile(target)) in self.block_move_types:
                print(self.name, "tried to move onto", entity.name)
                return False
        self.path.pop()
        old_tile = self.tile
        self.tile = target
        MAP.move_entity(self, old_tile, self.tile)
        return True
          
    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    def print(self):
        print("--Unit id: ", self.id, "  x: ", self.tile[0], "  y: ", self.tile[1])

    def kill_entity(self, entity):
        print(self.name, "killed", entity.name)
        self.satiation_current = min(self.satiation_current + 200, self.satiation_max)
        self.kills += 1
        entity.die()

    def eat_grass(self, grass):
        # print(self.name, "ate", grass.name)
        self.satiation_current = min(self.satiation_current + 100, self.satiation_max)
        grass.eaten()

    def sex(self, entity):
        
        if type(self) is Deer:
            baby = Deer(self.tile)
        elif type(self) is Wolf:
            baby = Wolf(self.tile)
        
        if baby.is_male == False: baby.is_fertile = False

        self.is_fertile = False
        self.satiation_current -= 100
        print(baby.name, "is born")
        
class Deer(Unit):

    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = COLOR_DEER_HUNGERY
        self.satiation_color = COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.block_move_types = { Block, Deer, Wolf, Person, Grass }
        self.block_pathing_types = { Block, Wolf, Person, Deer }
        self.kill_types = {}
        self.eats_grass = True
        Unit.init_b(self, tile)

    def update_target(self):
        if self.satiation_current < 1 and random.randint(1, 1) == 1:
            self.path = get_path(self.tile, 0, self.move_range_max, self.block_pathing_types, lambda e : type(e) == Grass and e.crop_current == e.crop_max, random.choice, debug_pathfinding, COLOR_PATH_HUNT)
        elif self.is_male == False and self.is_fertile == True and random.randint(1, 1) == 1:
            self.path = get_path(self.tile, 0, self.move_range_max, self.block_pathing_types, lambda e : type(e) == type(self) and e.is_male == True, random.choice, debug_pathfinding, COLOR_PATH_MATE)
        else:
            self.path = get_path(self.tile, 0, self.move_range_min, self.block_pathing_types, None, None, debug_pathfinding, None)


class Wolf(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = COLOR_WOLF_HUNGERY
        self.satiation_color = COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.block_move_types = { Block, Wolf, Person, Grass }
        self.block_pathing_types = { Block, Person, Grass }
        self.kill_types = { Deer }
        self.satiation_max = 200
        Unit.init_b(self, tile)

    def update_target(self):
        if self.satiation_current < 1 and random.randint(1, 1) == 1:
            self.path = get_path(self.tile, 0, self.move_range_max, self.block_pathing_types, lambda e : type(e) == Deer, random.choice, debug_pathfinding, COLOR_PATH_HUNT)
        elif self.is_male == False and self.is_fertile == True and random.randint(1, 1) == 1:
            self.path = get_path(self.tile, 0, self.move_range_max, self.block_pathing_types, lambda e : type(e) == type(self) and e.is_male == True, random.choice, debug_pathfinding, COLOR_PATH_MATE)
        else:
            self.path = get_path(self.tile, 0, self.move_range_min, self.block_pathing_types, None, None, debug_pathfinding, None)
            

class Person(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = COLOR_PERSON_HUNGERY
        self.satiation_color = COLOR_PERSON
        self.radius = UNIT_RADIUS_PERSON
        self.is_manual = True
        self.kill_types = { Deer, Wolf }
        self.block_pathing_types = { Block }
        self.block_move_types = { Block, Person }
        self.patience_max = 20
        self.satiation_max = 1000
        Unit.init_b(self, tile)

