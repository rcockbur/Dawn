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
    next_unit_is_male = False

    def get_gender():
        r = Unit.next_unit_is_male
        Unit.next_unit_is_male = not Unit.next_unit_is_male
        return r

    def init_a(self, tile):
        Entity.__init__(self, tile)
        self.is_manual = False
        self.path = Path()
        self.kills = 0
        self.satiation_max = 200
        self.satiation_full = 100
        self.satiation_starving = -100
        self.satiation_min = -200
        self.move_period_diag = 14
        self.move_period_ortho = 10
        self.move_current = 0
        self.status = STOPPED
        self.age_adult = 2
        
        self.kill_types = {}
        self.eat_types = {}
        self.patience_max = 50
        self.last_scanned_at = 0
        self.is_male = Unit.get_gender()
        
        self.dies_when_eaten = True
        self.target = None
        
        if sim_tick[0] == 0:
            self.birthday = random.randint(0, TICKS_PER_YEAR - 1)
            self.age = random.randint(2, 4)
        else:
            self.age = 0 # should be 0 if we want spawned units to have real age
            self.birthday = sim_tick[0]

        

        if self.is_male == False:

            self.is_fertile = self.age >= self.age_adult
            self.pregnant_with = None
            self.pregnant_until = None
            
        
    def init_b(self, tile):
        self.move_current = self.move_period_ortho
        self.patience_current = self.patience_max
        self.satiation_current = random.randint(0, self.satiation_max)
        self.idle_current = random.randint(0, self.idle_max)


    def update(self):
        # is it my birthday?
        if sim_tick[0] % TICKS_PER_YEAR == self.birthday:
            self.age += 1
            if self.age == self.age_max:
                print(self.name, "died of old age")
                self.die()
            if self.age == self.age_adult:
                self.is_fertile = True

        if self.is_dead == False:
            

            # check hunger  
            if sim_tick[0] % 8 == 0:
                if self.satiation_current > self.satiation_min:
                    self.satiation_current -= 1
                else:
                    print(self.name, "died of starvation")
                    self.die()
                    return


            if self.is_male == False and self.pregnant_until is not None and self.pregnant_until == sim_tick[0]:
                self.birth()
                        

            # update target if automatic, out of path, and idle_current is out
            if self.is_manual == False:
                if self.status == STOPPED and self.idle_current == 0:
                    self.update_target()
                    
            # check whats right in front of us
            is_blocked = False
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
                    # print(self.name, "lost patience with", entity.name, "@", sim_tick[0])
            else:
                self.patience_current = self.patience_max

            # move if ready
            if self.path.size() > 0:
                if is_blocked == False and self.move_current == 0:
                    self.update_move_cost(self.path.points[0])
                    self.move()
            else:
                if self.status != STOPPED:
                    self.update_idle_cost()
                    self.status = STOPPED
                self.idle_current = max(self.idle_current - 1, 0)
            self.move_current = max(self.move_current - 1, 0)

    def update_idle_cost(self):
        self.idle_current = random.randint(self.idle_min, self.idle_max)

        speed_up_factor = 1
        
        if self.satiation_current < 0:
            speed_up_factor += 0.5
            if self.satiation_current < self.satiation_starving:
                speed_up_factor += 0.5
        else:
            if self.can_mate():
                speed_up_factor += 0.5

        self.idle_current = int(self.idle_current / speed_up_factor)

    def update_move_cost(self, point):
        if self.tile[0] != point[0] and self.tile[1] != point[1]:
            self.move_current = self.move_period_diag
        else:
            self.move_current = self.move_period_ortho

        speed_up_factor = 1
        
        if self.satiation_current < 0:
            speed_up_factor += 0.5
            if self.satiation_current < self.satiation_starving:
                speed_up_factor += 0.5
        else:
            if self.can_mate():
                speed_up_factor += 0.5

        self.move_current = int(self.move_current / speed_up_factor)


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
        if entity.dies_when_eaten == False:
            self.path.clear()
        self.satiation_current = min(self.satiation_current + 100, self.satiation_max)
        entity.eaten()

    def eaten(self):
        self.die() 


    def can_eat(self):
        return self.satiation_current < self.satiation_full

    def can_be_eaten(self):
        return True

    def can_be_hunted(self):
        return True

    def birth(self):
        if type(self) is Deer:
            baby = Deer(self.tile)
        elif type(self) is Wolf:
            baby = Wolf(self.tile)
        
        self.satiation_current -= 50
        self.pregnant_until = None
        self.pregnant_with = None
        if self.age < self.age_senior:
            self.is_fertile = True
        print(self.name, "gave birth to", baby.name)


    def mate(self, entity):
        self.pregnant_until = sim_tick[0] + random.randint(self.pregnancy_duration//2, self.pregnancy_duration)
        self.pregnant_with = entity
        self.is_fertile = False
        # print(self.name, "is pregnant")
        
        

    def can_mate(self):
        return self.is_male == False and self.is_fertile == True and self.satiation_current > 0 and self.age_adult <= self.age <= self.age_senior

    def can_be_mated_with(self):
        return self.is_male and self.age >= self.age_adult


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

    def get_pregnant_string(self):
        if self.pregnant_until is None:
            return "-"
        else:
            return str(self.pregnant_until)

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
        self.idle_min = 50
        self.idle_max = 100
        self.move_range_idle = 8
        self.move_range_hunt = 14
        self.move_range_mate = 14
        self.is_wolf = False
        self.color = COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        # self.speed_up_factor = 2
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Grass }
        self.age_max = random.randint(8, 12)
        self.age_senior = 10

        if self.is_male == False:
            self.fertile_odds = 35
            self.pregnancy_duration = TICKS_PER_YEAR
        Unit.init_b(self, tile)

    def update_target(self):
        
        path_info = get_path(self, True)
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]
        if type(self.target) == Grass:
            self.target.mark()



class Wolf(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.idle_min = 100
        self.idle_max = 200
        self.move_range_idle = 12
        self.move_range_hunt = 20
        self.move_range_mate = 20
        self.is_wolf = True
        self.color = COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        # self.speed_up_factor = 2
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Deer }
        self.age_max = random.randint(32, 48)
        self.age_senior = 40

        if self.is_male == False:
            self.fertile_odds = 35
            self.pregnancy_duration = TICKS_PER_YEAR * 4

        Unit.init_b(self, tile)

    def update_target(self):
        path_info = get_path(self, True)
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]

            

class Person(Unit):
    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.color = COLOR_PERSON
        self.radius = UNIT_RADIUS_PERSON
        self.is_manual = True
        self.kill_types = { Deer, Wolf }
        self.block_pathing_types = { Block }
        self.block_move_types = { Block, Person }
        self.patience_max = 20
        self.satiation_max = 1000
        Unit.init_b(self, tile)

