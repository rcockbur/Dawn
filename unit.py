from globals import *
import pygame, random
from utility import measure
from path import Path
from pathfinding import get_path, get_path
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
        self.idle_min = 25
        self.idle_max = 50
        self.move_range_min = 10
        self.move_range_max = 20
        self.move_period_diag = 14
        self.move_period_ortho = 10
        self.move_current = 0
        self.status = STOPPED
        self.kill_types = {}
        self.eat_types = {}
        self.patience_max = 10
        self.is_male = Unit.get_gender()
        self.dies_when_eaten = True
        self.target = None
        if self.is_male == False:
            self.is_fertile = False
            self.pregnant_with = None
            self.pregnant_at = None
            self.fertile_odds = 100
        
    def init_b(self, tile):
        self.move_current = self.move_period_ortho
        self.color = self.satiation_color
        self.color_original = self.color
        self.patience_current = self.patience_max
        self.satiation_current = random.randint(self.satiation_min / 2, self.satiation_max)
        self.idle_current = random.randint(0, self.idle_max)


    def update(self):
        self.going_to_move = False

        if self.is_dead == False:
            is_blocked = False

            # check hunger  
            if sim_ticks[0] % 8 == 0:
                if self.satiation_current > self.satiation_min:
                    self.satiation_current -= 1
                    # if self.satiation_current > 0:
                    #     self.color = self.satiation_color
                    # else:
                    #     self.color = self.hungery_color
                else:
                    print(self.name, "died of starvation")
                    self.die()
                    return

            # check fertility
            if sim_ticks[0] % 8 == 0 and self.is_male == False and self.is_fertile == False and self.satiation_current >= 0:
                if random.randint(0, self.fertile_odds) == 0:
                    self.is_fertile = True    

            # update target if automatic, out of path, and idle_current is out
            if self.is_manual == False:
                if self.status == STOPPED and self.idle_current == 0:
                    self.update_target()
                    
            # check whats right in front of us
            if self.path.size() > 0:
                ate_the_blocker = False
                entity = MAP.get_entity_at_tile(self.path.points[0])
                if self.can_eat() and type(entity) in self.eat_types and entity.can_be_eaten():
                    self.eat(entity)
                    ate_the_blocker = entity.dies_when_eaten
                if self.can_mate() and type(self) == type(entity) and entity.can_be_mated_with():
                    self.mate(entity)
                if type(entity) in self.cant_move_types and ate_the_blocker == False:
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
                # self.status = MOVING
                if is_blocked == False and self.move_current == 0:
                    
                    if self.tile[0] != self.path.points[0][0] and self.tile[1] != self.path.points[0][1]:
                        self.move_current = self.move_period_diag
                    else:
                        self.move_current = self.move_period_ortho
                    self.move()
            else:
                if self.status != STOPPED:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                    self.status = STOPPED
                self.idle_current = max(self.idle_current - 1, 0)
            self.move_current = max(self.move_current - 1, 0)


    def move(self):
        target = self.path.points[0]
        if MAP.tile_within_bounds(target) == False:
            print (self.name, "tried to move of bounds")
            return False
        entity = MAP.get_entity_at_tile(target)
        if entity is not None:
            if type(entity) in self.cant_move_types:
                print(self.name, "tried to move onto", entity.name)
                return False
        self.path.pop()
        old_tile = self.tile
        self.tile = target
        MAP.move_entity(self, old_tile, self.tile)
        return True


    def eat(self, entity):
        if type(self) is not Deer:
            print(self.name, "ate", entity.name)
        self.satiation_current = min(self.satiation_current + 100, self.satiation_max)
        entity.eaten()

    def eaten(self):
        self.die() 

    def can_eat(self):
        return self.satiation_current < 0

    def can_be_eaten(self):
        return True

    def can_be_hunted(self):
        return True


    def mate(self, entity):
        if type(self) is Deer:
            baby = Deer(self.tile)
        elif type(self) is Wolf:
            baby = Wolf(self.tile)
        
        if baby.is_male == False: 
            baby.is_fertile = False

        self.is_fertile = False
        self.satiation_current -= 100
        print(baby.name, "is born")

    def can_mate(self):
        return self.is_male == False and self.is_fertile == True and self.can_eat() == False

    def can_be_mated_with(self):
        return self.is_male


    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False


    def get_target_string(self):
        if self.path.size() > 0:
            return str(self.path.get(0)[0]) + " , " + str(self.path.get(0)[1])
        return "-"

    def get_status_string(self):
        if self.status == STOPPED:
            return "Stopped"
        elif self.status == MOVING:
            return "Moving"
        elif self.status == HUNTING:
            return "Hunting"
        elif self.status == MATING:
            return "Mating"
        else:
            return "error"

    def get_hungery_string(self):
        if self.can_eat():
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
        

class Deer(Unit):

    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = COLOR_DEER_HUNGERY
        self.satiation_color = COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Grass }
        Unit.init_b(self, tile)

    def update_target(self):
        
        path_info = get_path(self, True, self.move_range_min, self.move_range_max, get_debug_pathfinding())
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]
        if type(self.target) == Grass:
            self.target.mark()



class Wolf(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = COLOR_WOLF_HUNGERY
        self.satiation_color = COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Deer }

        if self.is_male == False:
            self.fertile_odds = 500
        Unit.init_b(self, tile)

    def update_target(self):
        path_info = get_path(self, True, self.move_range_min, self.move_range_max, get_debug_pathfinding())
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]

            

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

