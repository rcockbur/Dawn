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
        self.id = Unit.new_id()
        self.move_period = 10
        self.move_in = self.move_period
        self.tile = tile
        self.is_selected = False
        self.name = self.new_name()
        self.path = Path()
        MAP.add_unit_at(self, tile.x, tile.y)

    def init_b(self, tile):
        self.move_in = self.move_period

    def class_name(self):
        return type(self).__name__.lower()


    def update(self):   
        self.move_in = self.move_in - 1
        if self.move_in == 0:
            # Need new target
            if self.path.size() == 0:
                self.update_target()

            # Process target
            if self.path.size() > 0:
                unit = MAP.get_unit_at(self.path.points[0])
                if unit == None:
                    self.move_to(self.path.pop())
                else:
                    self.path.clear()
                        
            self.move_in = self.move_period

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
        if MAP.get_unit_at(target) is not None:
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



    def kill_deer_at_tile(self, tile):
        global deer_killed
        unit = MAP.get_unit_at(tile)
        if type(unit) == Deer:
            deer_killed = deer_killed + 1
            if deer_killed % 10 == 0: print(deer_killed, " deer killed")
            MAP.remove_unit(unit)
            self.satiation = randint(1000, 1000)
            self.color = COLOR_PINK



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
        self.move_in = 5
        self.block_target_types = { Block }
        self.block_pathing_types = { Block, Deer, Wolf, Person }
        self.block_movement_type = { Block, Deer, Wolf, Person }
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Deer.name_index

    # @measure
    def update_target(self):
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types)
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
        self.move_in = 8
        self.block_target_types = { Block }
        self.block_pathing_types = { Block, Deer, Wolf, Person }
        self.block_movement_type = { Block, Deer, Wolf, Person }
        self.satiation = 0
        Unit.init_b(self, tile)

    def get_name_index(self):
        return Wolf.name_index

    def update_target(self):
        tile = pathfinding.find_nearby_tile(self.tile, self.block_pathing_types)
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
        self.move_period = 5
        self.moving_right = True
        self.move_distance = 20
        self.block_target_types = { Block }
        self.block_pathing_types = { Block, Person }
        self.block_movement_type = { Block, Deer, Wolf, Person }
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