from globals import *
from point import *
import pygame, random
from utility import *
from map import *
from path import *
import pathfinding

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
        self.move_range = 30
        
        self.tile = tile
        self.is_selected = False
        self.name = self.new_name()
        self.kill_types = {}
        self.path = Path()
        MAP.add_unit_at(self, tile.x, tile.y)

    def init_b(self, tile):
        self.move_current = self.move_period

    def class_name(self):
        return type(self).__name__.lower()


    def update(self, dead_units):   
        if self.is_dead == False:
            # if path is empty
            if self.path.size() == 0:
                # generate new target if not idle
                if self.idle_current == 0:
                    self.idle_current = random.randint(self.idle_min, self.idle_max)
                    self.update_target()
                else:
                    self.idle_current = self.idle_current - 1

            # if we run into something
            elif self.path.size() > 0:
                if type(MAP.get_unit_at(self.path.points[0])) in self.kill_types:
                    dead_units.add(MAP.get_unit_at(self.path.points[0]))

                if type(MAP.get_unit_at(self.path.points[0])) in self.block_pathing_types:
                    print("recalculating")
                    self.update_target()


            # if we have path, and move is ready
            if self.path.size() > 0:
                if self.move_current == 0:
                    self.move_to(self.path.pop())
                    self.move_current = self.move_period
                else:
                    self.move_current = self.move_current - 1


                
                    


    def get_name_index(self):
        raise NotImplementedError()

    def update_target(self):
        raise NotImplementedError()


    def set_path(self, path):
        self.path = path


    def move_by(self, vector):
        target = self.tile + vector
        self.move_to(target)


    def move_to(self, target):
        if MAP.tile_within_bounds(target) == False:
            print (self.name, "tried to move of bounds")
            return

        unit = MAP.get_unit_at(target)
        if type(MAP.get_unit_at(target)) in self.block_pathing_types:
            print(self.name, "tried to move onto", unit.name)
            return
        
        old_tile = self.tile.copy()
        self.tile = target.copy()
        MAP.move_unit(self, old_tile, self.tile)
            

    def draw(self):
        if self.is_selected:
            outter_rect = Map.calculate_rect(self.tile, self.radius+2)    
            pygame.draw.rect(screen, COLOR_YELLOW, outter_rect)
        rect = Map.calculate_rect(self.tile, self.radius)
        pygame.draw.rect(screen, self.color, rect)

        


    def draw_path(self):
        if self.is_selected:
            if self.path is not None:
                for point in self.path.points:
                    rect = Map.calculate_rect(point, self.radius - 2)
                    pygame.draw.rect(screen, COLOR_YELLOW, rect)

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False


    def print(self):
        print("--Unit id: ", self.id, "  x: ", self.tile.x, "  y: ", self.tile.y)



    def kill_unit(self, unit):
        unit.is_dead = True
        self.satiation = randint(1000, 1000)
        self.color = self.satiation_color



def tup_from_tile(tile):
    return (tile.x, tile.y)

def tile_from_tup(tup):
    return Point(x = tup[0], y = tup[1])

        
class Deer(Unit):
    name_index = [0]

    def __init__(self, tile):
        Unit.init_a(self, tile)
        # self.name = "deer"
        self.color = UNIT_COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.block_pathing_types = { Block, Deer, Wolf, Person }
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Deer.name_index

    # @measure
    def update_target(self):
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, self.move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path



class Wolf(Unit):
    name_index = [0]

    def __init__(self, tile):
        Unit.init_a(self, tile)
        # self.name = "wolf"
        self.color = UNIT_COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.block_pathing_types = { Block, Wolf, Person }
        self.kill_types = { Deer }
        self.satiation = 0
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Wolf.name_index

    def update_target(self):
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types, self.move_range)
        if tile is not None:
            path = pathfinding.astar(self.tile, tile, self.block_pathing_types)
            self.path = path



class Person(Unit):
    name_index = [0]

    def __init__(self, tile):
        # self.name = "person"
        Unit.init_a(self, tile)
        self.color = UNIT_COLOR_PERSON
        self.radius = UNIT_RADIUS_PERSON
        self.moving_right = True
        self.move_distance = 20
        self.move_period = 30
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