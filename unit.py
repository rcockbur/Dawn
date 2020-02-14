from globals import *
import pygame, random
from utility import measure
# from path import Path
from pathfinding import get_path, get_path
from map import calculate_rect
from ability import Move, Eat, Mate, Socialize
from entity import Entity
from block import Block, Grass
print("running unit.py")

abilities = { HUNTING: Eat, MATING: Mate, MOVING: Move, SOCIAL: Socialize }

def link_types():
    Unit.cant_path_to_types = { Block }
    Unit.cant_path_over_types = { Block, Deer, Wolf, Person, Grass }
    Unit.cant_move_types = { Block, Deer, Wolf, Person, Grass }
    Deer.avoid_types.add(Wolf)
    Wolf.avoid_types.add(Person)

class Unit(Entity):
    food_remaining =4000
    is_social = False
    move_period = 20
    patience_max = 50
    pregnancy_duration_d = 150
    sat_min = -1000
    sat_starving = -500
    sat_hungery = 0
    sat_peckish = 500
    sat_full = 1000
    sat_max = 1200
    sat_lost_per_day = 20

    def init_a(self, tile, born_naturally):
        Entity.__init__(self, tile, born_naturally)
        self.ability_list = list()
        self.is_dead = False
        self.eat_rate = 150
        self.idle_is_dirty = False
        self.can_scan_at = 0
        self.is_male = random.randint(1,2) == 1
        self.parent_mom = None
        self.parent_dad = None
        self.in_danger = False

        if self.is_male == False:
            self.is_fertile = False
            self.pregnant_with = None
            self.pregnant_until = None
        
    def init_b(self, tile, born_naturally):
        # self.patience_current = self.__class__.patience_max
        self.sat_current = 10 * (random.randint(self.__class__.sat_hungery, self.__class__.sat_full) // 10)
        if self.__class__.is_manual == False:
            self.idle_current = random.randint(0, self.__class__.idle_max)

    def update(self):
        if self.is_destroyed == False:
            if self.is_dead == False:
                if current_date[DT_HOUR_OD] == self.birth[DT_HOUR_OD]:
                    # its my own tick - happens once a day
                    if current_date[DT_DAY_OM] == self.birth[DT_DAY_OM]:
                        if self.is_male == False and self.is_fertile == False and self.pregnant_until == None and self.__class__.age_adult <= self.age < self.__class__.age_senior:
                            if random.randint(1, 2) == 1:
                                self.is_fertile = True
                        if current_date[DT_DAY_OY] == self.birth[DT_DAY_OY]:
                            self.age += 1
                            if self.age == self.death_at_age:
                                self.__class__.monthly_died_age += 1
                                self.die()
                                return
                    # hunger  
                    if self.sat_current > self.__class__.sat_min:
                        self.sat_current = max(self.sat_current - self.__class__.sat_lost_per_day, self.sat_min)
                    else:
                        self.__class__.monthly_died_starved += 1
                        self.die()
                        return
                # pregnancy
                if self.is_male == False and self.pregnant_until is not None and self.pregnant_until == current_date[DT_HOUR]:
                    self.give_birth()
                # automatic unit update ability
                if self.__class__.is_manual == False:
                    if len(self.ability_list) == 0 :
                        if self.idle_current == 0:
                            if self.idle_is_dirty:
                                self.reset_idle_current()
                            else:
                                self.update_abilities()
                                self.idle_is_dirty = True
                        else:
                            self.idle_current = max(self.idle_current - 1, 0)
                if len(self.ability_list) > 0 :
                    results = self.ability_list[0].execute()
                    if results["complete"]:
                        self.ability_list.pop(0)
            else:
                if current_date[DT_HOUR_OD] == self.birth[DT_HOUR_OD]:
                    self.food_remaining -= 20
                    if self.food_remaining <= 0:
                        self.destroy()

    def update_abilities(self):
        wants_to_hunt = False
        wants_to_mate = False
        wants_to_socialize = False
        if self.sat_current < self.__class__.sat_full:
            eat_chance = (100 * (self.sat_current - self.__class__.sat_full)) // (self.__class__.sat_starving - self.__class__.sat_peckish) # ranges from 0 to 99 
            if random.randint(0, 99) <= eat_chance:
                wants_to_hunt = True
        if wants_to_hunt == False and self.can_mate():
            wants_to_mate = True
        if wants_to_hunt == False and self.__class__.is_social and random.randint(1,3) > 1:
            wants_to_socialize = True

        search_range = self.__class__.move_range_idle

        if wants_to_hunt:
            search_range = max(search_range, self.__class__.move_range_hunt)
        if wants_to_mate:
            search_range = max(search_range, self.__class__.move_range_mate)    
        if wants_to_socialize:
            search_range = max(search_range, self.__class__.move_range_social)

        if (wants_to_hunt and self.sat_current <= self.sat_hungery) or wants_to_mate or wants_to_socialize:
            if current_date[DT_HOUR] >= self.can_scan_at:
                self.can_scan_at = current_date[DT_HOUR] + self.__class__.scan_period
                search_range = search_range * 1.5

        path_info = get_path(self, True, wants_to_hunt, wants_to_mate, wants_to_socialize, self.prefer_food, search_range, self.__class__.move_range_idle)
        path = path_info[0]
        ability_type = path_info[1]
        target = path_info[2]
        self.in_danger = path_info[3]
        if ability_type is not STOPPED:
            ability = abilities[ability_type]
            self.ability_list.append(ability(self, path, target))
                    
    def reset_idle_current(self):
        self.idle_current = random.randint(self.__class__.idle_min, self.__class__.idle_max)
        speed_up = 1
        if self.in_danger:
            speed_up += 1.0
            self.in_danger = False
        else:    
            if self.sat_current < self.__class__.sat_hungery:
                speed_up += 0.3
                if self.sat_current < self.__class__.sat_starving:
                    speed_up += 0.3
            else:
                if self.can_mate():
                    speed_up += 0.3
        self.idle_current = round(self.idle_current / speed_up)
        self.idle_is_dirty = False

    def destroy(self):
        if self.is_dead == False:
            self.die()
        destroyed_units.add(self)
        self.is_destroyed = True

    def die(self):
        self.is_dead = True
        self.color = COLOR_RED
        self.food_remaining = self.__class__.food_remaining
        self.ability_list.clear()

    def move(self, tile):
        if MAP.tile_within_bounds(tile) == False:
            print (self.name, "tried to move of bounds")
            return False
        entity = MAP.get_entity_at_tile(tile)
        if entity is not None:
            if type(entity) in self.__class__.cant_move_types:
                print(self.name, "tried to move onto", entity.name)
                return False
        old_tile = self.tile
        self.tile = tile
        MAP.move_entity(self, old_tile, self.tile)
        return True

    # returns true if there is more to be eaten here
    def eat(self, entity):
        if self.can_eat(entity) and self.sat_current < self.__class__.sat_full:
            if isinstance(entity, Unit) and entity.is_dead == False:
                self.kills += 1
            r = entity.eaten(self.eat_rate)
            food_gained = r[0]
            is_more = r[1]
            self.sat_current = min(self.sat_current + food_gained, self.__class__.sat_max)
            return {"complete": is_more == False or self.sat_current >= self.__class__.sat_full}
        else:
            print(self.name, "tried to eat", entity.name)
            return {"complete": True}

    # returns a satiation amount, and a bool whether there is more to eat
    def eaten(self, amount):
        amount = min(amount, self.food_remaining)
        if self.is_dead == False:
            self.die()
            self.__class__.monthly_died_hunted += 1
        self.food_remaining -= amount
        if self.food_remaining <= amount:
            self.destroy()
            return (amount, False)
        return (amount, True)

    def can_be_eaten(self):
        return self.is_destroyed == False

    def can_be_hunted(self):
        return self.is_destroyed == False

    def give_birth(self):
        if type(self) is Deer:
            baby = Deer(self.tile, True)
        elif type(self) is Wolf:
            baby = Wolf(self.tile, True)
        baby.parent_mom = self.id
        baby.parent_dad = self.pregnant_with
        self.pregnant_until = None
        self.pregnant_with = None
        self.__class__.monthly_born += 1

    def mate(self, entity):
        if random.randint(1, 2) == 1:
            min_duration = int(self.__class__.pregnancy_duration_d * (9/10)) * HOURS_PER_DAY
            max_duration = int(self.__class__.pregnancy_duration_d * (11/10)) * HOURS_PER_DAY
            self.pregnant_until = current_date[DT_HOUR] + random.randint(min_duration, max_duration)
            self.pregnant_with = entity.id
            self.is_fertile = False 
        return {"complete": True}
        
    def can_mate(self):
        return self.is_male == False and self.is_fertile == True and self.sat_current > self.__class__.sat_hungery and self.__class__.age_adult <= self.age <= self.__class__.age_senior

    def can_be_mated_with(self):
        return self.is_male and self.age >= self.__class__.age_adult and self.is_destroyed == False

    def select(self):
        self.is_selected = True

    def socialize(self, entity):
        return {"complete": True}

    def deselect(self):
        self.is_selected = False

    def get_food_string(self):
        if self.sat_current <= self.__class__.sat_starving:
            return str(self.sat_current) + " Starving"
        elif self.sat_current <= self.__class__.sat_hungery:
            return str(self.sat_current) + " Hungery"
        elif self.sat_current <= self.__class__.sat_peckish:
            return str(self.sat_current) + " Peckish"
        elif self.sat_current >= self.__class__.sat_full:
            return str(self.sat_current) + " Full"
        else:
            return str(self.sat_current) + " Neutral"

    def get_sex_string(self):
        if self.is_male:
            return "Male"
        else:
            s = "Female"
            if self.is_fertile: s = s + "(F)"
            if self.pregnant_until is not None: s = s + "(P)"
            return s
    
class Deer(Unit):
    age_adult = 2
    age_senior = 9
    avoid_types = set()
    eat_types = { Grass }
    idle_min = 40
    idle_max = 60
    monthly_born = 0
    monthly_died_age = 0
    monthly_died_starved = 0
    monthly_died_hunted = 0
    move_range_idle = 8
    move_range_hunt = 8
    move_range_mate = 8
    radius = UNIT_RADIUS_DEER
    repath_attempts = 1
    scan_period = HOURS_PER_DAY * 120

    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.color = COLOR_DEER
        self.death_at_age = random.randint(10, 12)
        Unit.init_b(self, tile, born_naturally)

    def can_eat(self, entity):
        return type(entity) in self.__class__.eat_types

    def prefer_food(self, entity):
        return True


class Wolf(Unit):
    age_adult = 2
    age_senior = 9
    avoid_types = set()
    eat_types = { Deer }
    idle_min = 60
    idle_max = 100
    is_social = True
    monthly_born = 0
    monthly_died_age = 0
    monthly_died_starved = 0
    monthly_died_hunted = 0
    move_range_idle = 8
    move_range_hunt = 10
    move_range_mate = 10
    move_range_social = 10
    radius = UNIT_RADIUS_WOLF
    repath_attempts = 2
    scan_period = HOURS_PER_DAY * 60

    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.color = COLOR_WOLF
        self.death_at_age = random.randint(10, 12)
        self.kills = 0
        Unit.init_b(self, tile, born_naturally)

    def can_eat(self, entity):
        return type(entity) in self.__class__.eat_types or type(entity) == Wolf and entity.is_dead == True

    def prefer_food(self, entity):
        return entity.is_dead == True


class Person(Unit):
    age_adult = 16
    age_senior = 75
    eat_types = { Deer, Wolf }
    is_manual = True
    monthly_born = 0
    monthly_died_age = 0
    monthly_died_starved = 0
    monthly_died_hunted = 0
    radius = UNIT_RADIUS_PERSON
    repath_attempts = 2
    sat_lost_per_day = 5

    def __init__(self, tile, born_naturally):
        Unit.init_a(self, tile, born_naturally)
        self.color = COLOR_PERSON
        self.death_at_age = random.randint(80, 100)
        self.kills = 0
        Unit.init_b(self, tile, born_naturally)

link_types()