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
    # next_unit_is_male = False

    # def get_gender():
    #     r = Unit.next_unit_is_male
    #     Unit.next_unit_is_male = not Unit.next_unit_is_male
    #     return r

    def init_a(self, tile, born_naturally):
        Entity.__init__(self, tile)
        self.is_manual = False
        self.path = Path()
        self.kills = 0
        self.satiation_max = 1000
        self.satiation_full = 800
        self.satiation_starving = -500
        self.satiation_min = -1000
        self.move_period_diag = 28
        self.move_period_ortho = 20
        self.move_current = 0
        self.status = STOPPED
        self.age_adult = 2
        
        self.kill_types = {}
        self.eat_types = {}
        self.patience_max = 50
        self.last_scanned_at = 0
        self.is_male = random.randint(1,2) == 1
        
        self.dies_when_eaten = True
        self.target = None
        
        if born_naturally == True:
            self.age = 0
            self.birth_tick = tick[0]
            self.birth_day = day[0]
            self.birth_month = month[0]
            self.birth_year = year[0]
            self.birth_tick_of_day = tick_of_day[0]
            self.birth_tick_of_month = tick_of_month[0]
            self.birth_tick_of_year = tick_of_year[0]
            self.birth_day_of_month = day_of_month[0]
            self.birth_day_of_year = day_of_year[0]
            self.birth_month_of_year = month_of_year[0]
        else:
            self.birth_tick = random.randint((START_YEAR - 9) * TICKS_PER_YEAR, START_YEAR * TICKS_PER_YEAR)
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

        if self.is_male == False:
            self.is_fertile = self.age >= self.age_adult
            self.pregnant_with = None
            self.pregnant_until = None
            
        
    def init_b(self, tile, born_naturally):
        self.move_current = self.move_period_ortho
        self.patience_current = self.patience_max
        self.satiation_current = 10 * (random.randint(0, self.satiation_full) // 10)
        self.idle_current = random.randint(0, self.idle_max)


    def update(self):


        if self.is_dead == False:
            # its my own tick - happens once a day
            if tick_of_day[0] == self.birth_tick_of_day:
                # age
                if day_of_year[0] == self.birth_day_of_year:
                    self.age += 1
                    if self.age == self.age_max:
                        print(self.name, "died of old age")
                        self.die()
                        return
                    if self.age == self.age_adult and self.is_male == False:
                        self.is_fertile = True

                # hunger  
                if self.satiation_current > self.satiation_min:
                    self.satiation_current -= self.food_eat_rate
                else:
                    print(self.name, "died of starvation")
                    self.die()
                    return

                if self.is_male == False and self.pregnant_until is not None and self.pregnant_until == day[0]:
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
                    # print(self.name, "lost patience with", entity.name, "@", day[0])
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
        self.satiation_current = min(self.satiation_current + entity.food_value, self.satiation_max)
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
            baby = Deer(self.tile, True)
        elif type(self) is Wolf:
            baby = Wolf(self.tile, True)

        self.pregnant_until = None
        self.pregnant_with = None
        if self.age < self.age_senior:
            self.is_fertile = True

        print(self.name, "gave birth to", baby.name, "(", str(len(MAP.get_entities_of_type(self.__class__))), ")")


    def mate(self, entity):
        self.pregnant_until = day[0] + random.randint(int(self.pregnancy_duration * (9/10)), int(self.pregnancy_duration * (11/10)))
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
            day = str(self.pregnant_until % DAYS_PER_MONTH)
            month = (self.pregnant_until // DAYS_PER_MONTH) % MONTHS_PER_YEAR
            year = str((self.pregnant_until // DAYS_PER_YEAR))
            return MONTH_NAMES[month] + " " + day + ", " + year
            

    def get_food_string(self):
        if self.satiation_current >= 0:
            if self.satiation_current >= self.satiation_full:
                s = "Full     "
            else:
                s = "Neutral  "
        else:
            if self.satiation_current <= self.satiation_starving:
                s = "Starving "
            else:
                s = "Hungery  "
        return s + str(self.satiation_current)


    def get_sex_string(self):
        if self.is_male:
            return "Male"
        else:
            s = "Female"
            if self.is_fertile: s = s + "(F)"
            if self.pregnant_until is not None: s = s + "(P)"
            return s

    def get_fertile_string(self):
        if self.is_fertile:
            return "Yes"
        else:
            return "No"

    def get_birthday_string(self):
        if self.birth_day_of_month < 10:
            s = "0" + str(self.birth_day_of_month)
        else:
            s = str(self.birth_day_of_month)
        return MONTH_NAMES[self.birth_month_of_year] + " " + s + ", " + str(self.birth_year)
    
     
   

class Deer(Unit):

    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.idle_min = 100
        self.idle_max = 200
        self.move_range_idle = 8
        self.move_range_hunt = 12
        self.move_range_mate = 12
        self.is_wolf = False
        self.color = COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Grass }
        self.age_max = random.randint(10, 12)
        self.age_senior = 9
        self.food_value = 500
        self.food_eat_rate = 10

        if self.is_male == False:
            self.fertile_odds = 35
            self.pregnancy_duration = 100
        Unit.init_b(self, tile, born_naturally)

    def update_target(self):
        
        path_info = get_path(self, True)
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]
        if type(self.target) == Grass:
            self.target.mark()



class Wolf(Unit):
    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.idle_min = 100
        self.idle_max = 200
        self.move_range_idle = 8
        self.move_range_hunt = 12
        self.move_range_mate = 12
        self.is_wolf = True
        self.color = COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.cant_path_to_types = { Block }
        self.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
        self.cant_move_types = { Block, Deer, Wolf, Person, Grass }
        self.eat_types = { Deer }
        self.age_max = random.randint(20, 22)
        self.age_senior = 18
        self.food_eat_rate = 10

        if self.is_male == False:
            self.fertile_odds = 35
            self.pregnancy_duration = 200

        Unit.init_b(self, tile, born_naturally)

    def update_target(self):
        path_info = get_path(self, True)
        self.path = path_info[0]
        self.status = path_info[1]
        self.target = path_info[2]

            

class Person(Unit):
    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.color = COLOR_PERSON
        self.radius = UNIT_RADIUS_PERSON
        self.is_manual = True
        self.kill_types = { Deer, Wolf }
        self.block_pathing_types = { Block }
        self.block_move_types = { Block, Person }
        self.patience_max = 20
        self.satiation_max = 1000
        Unit.init_b(self, tile)

