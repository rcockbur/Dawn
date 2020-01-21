from globals import *
import pygame, random
from utility import measure
from path import Path
import pathfinding
from map import calculate_rect

print("running unit.py")

class Unit:
    color = (0, 128, 255)
    id_index = 0

    def new_id():
        Unit.id_index += 1
        return Unit.id_index - 1

    def new_name(self):
        index = self.get_name_index()
        r = self.class_name() + "_" + str(index[0])
        index[0] += 1
        return r

    def init_a(self, tile):
        self.is_dead = False
        self.id = Unit.new_id()
        self.move_period = 70
        self.move_current = self.move_period
        self.idle_min = 1000
        self.idle_max = 2000
        self.idle_current = random.randint(0, self.idle_max)
        self.move_range_min = 20
        self.move_range_max = 40
        self.satiation_current = 200
        self.satiation_max = 200
        self.manual_movement = False
        self.kills = 0
        self.tile = tile
        self.is_selected = False
        self.name = self.new_name()
        self.kill_types = {}
        self.path = Path()
        MAP.add_unit_at(self, tile.x, tile.y)

    def init_b(self, tile):
        self.move_current = self.move_period
        self.color = self.satiation_color
        self.color_original = self.color

    def class_name(self):
        return type(self).__name__.lower()


    def update(self, dead_units):
        if self.is_dead == False:
            # check hunger  
            if frames[0] % 20 == 0:
                if self.satiation_current > 0:
                    self.satiation_current -= 1
                    self.color = self.satiation_color
                else:
                    self.color = self.hungery_color

            # generate new target if empty
            if self.path.size() == 0 and self.manual_movement == False:
                if self.idle_current == 0:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                    self.update_target()
                else:
                    self.idle_current = self.idle_current - 1

            # we ran into something
            if self.path.size() > 0:
                unit = MAP.get_unit_at(self.path.points[0])
                
                if type(unit) in self.kill_types:
                    self.kill_unit(unit, dead_units)

                if type(unit) in self.block_pathing_types:
                    if self.manual_movement == True:
                        # print(self.name, "dropping path because of", unit.name, "@", frames[0])
                        # self.path.clear()
                        pass
                    else:
                        print(self.name, "recalculating because of", unit.name, "@", frames[0])
                        self.update_target()


            # if we have path, and move is ready
            if self.path.size() > 0:
                if self.move_current == 0:
                    self.move()
                    self.move_current = self.move_period
                else:
                    self.move_current = self.move_current - 1


                
                    


    def get_name_index(self):
        raise NotImplementedError()

    def update_target(self):
        raise NotImplementedError()


    def set_path(self, path):
        self.path = path


    def move(self):
        target = self.path.points[0]
        if MAP.tile_within_bounds(target) == False:
            print (self.name, "tried to move of bounds")
            return

        unit = MAP.get_unit_at(target)
        if type(MAP.get_unit_at(target)) in self.block_pathing_types:
            print(self.name, "tried to move onto", unit.name)
            return
        self.path.pop()
        old_tile = self.tile.copy()
        self.tile = target.copy()
        MAP.move_unit(self, old_tile, self.tile)
            

    def draw(self):
        if self.is_selected:
            outter_rect = calculate_rect(self.tile, self.radius+2)    
            pygame.draw.rect(screen, COLOR_YELLOW, outter_rect)
        rect = calculate_rect(self.tile, self.radius)
        pygame.draw.rect(screen, self.color, rect)

        


    def draw_path(self):
        if self.is_selected:
            if self.path is not None:
                for point in self.path.points:
                    rect = calculate_rect(point, self.radius - 2)
                    pygame.draw.rect(screen, COLOR_YELLOW, rect)

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False


    def print(self):
        print("--Unit id: ", self.id, "  x: ", self.tile.x, "  y: ", self.tile.y)



    def kill_unit(self, unit, dead_units):
        dead_units.add(unit)
        unit.is_dead = True
        self.color = self.satiation_color
        self.satiation_current = self.satiation_max
        self.kills += 1


def tup_from_tile(tile):
    return (tile.x, tile.y)

def tile_from_tup(tup):
    return Point(x = tup[0], y = tup[1])

        
class Deer(Unit):
    name_index = [0]

    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (160, 70, 0)
        self.satiation_color = (100, 40, 0)
        self.radius = UNIT_RADIUS_DEER
        self.block_pathing_types = { Block, Deer, Wolf, Person }
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Deer.name_index

    # @measure
    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path



class Wolf(Unit):
    name_index = [0]

    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (255, 151, 151)
        self.satiation_color = (191, 191, 191)
        self.radius = UNIT_RADIUS_WOLF
        self.block_pathing_types = { Block, Wolf, Person }
        self.kill_types = { Deer }
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Wolf.name_index

    def update_target(self):
        move_range = random.randint(self.move_range_min, self.move_range_max)
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path



class Person(Unit):
    name_index = [0]

    def __init__(self, tile):
        Unit.init_a(self, tile)
        self.hungery_color = (175, 35, 255)
        self.satiation_color = (35, 35, 255)
        self.radius = UNIT_RADIUS_PERSON
        self.moving_right = True
        self.move_distance = 20
        self.move_period = 30
        self.manual_movement = True
        self.kill_types = { Deer, Wolf }
        self.block_pathing_types = { Block, Person }
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Person.name_index


    def update_target(self):
        pass


class Block(Unit):
    name_index = [0]

    def __init__(self, tile):
        # self.name = "block"
        Unit.init_a(self, tile)
        self.color = COLOR_GREY_DARK
        self.satiation_color = COLOR_GREY_DARK
        self.radius = UNIT_RADIUS_BLOCK
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Block.name_index


def create_block_line(tile_1, tile_2) :
    # vertical
    if tile_1.x == tile_2.x and tile_1.y < tile_2.y:
        for i in range(tile_2.y - tile_1.y + 1):
            Block(Point(x = tile_1.x, y = tile_1.y + i))
    # horizontal
    elif tile_1.y == tile_2.y and tile_1.x < tile_2.x:
        pass