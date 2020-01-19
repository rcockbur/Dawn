from globals import *
from point import *
import pygame, random
from utility import *
from map import *
from path import *

class Unit:
    color = (0, 128, 255)
    id_index = 0


    def new_id():
        Unit.id_index += 1
        return Unit.id_index - 1


    def init_a(self, tile):
        self.move_in = 10
        self.move_period = 10

    def init_b(self, tile):
        self.id = Unit.new_id()
        self.tile = tile
        self.path = Path(list())
        self.target = None
        self.move_in = self.move_period

        MAP.add_unit_at(self, tile.x, tile.y)
        return self


    def update(self):   
        self.move_in = self.move_in - 1
        if self.move_in == 0:
            if self.path.size() == 0:
                self.update_target()
            if self.path.size() > 0:
                self.move_to(self.path.pop())
            self.move_in = self.move_period
                
                


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
            print(self.name, "blocked by", unit.name)
            return
        
        old_tile = self.tile.copy()
        self.tile = target.copy()
        MAP.move_unit(self, old_tile, self.tile)
            

    def calculate_rect(tile, radius):
        pos = Point(tile_get_mid_x(tile.x) - radius, tile_get_mid_y(tile.y) - radius)
        return pygame.Rect(pos.x, pos.y, radius * 2, radius * 2)

    def draw(self):
        rect = Unit.calculate_rect(self.tile, self.radius)
        pygame.draw.rect(screen, self.color, rect)

        if self.path is not None:
            self.draw_path()


    def draw_path(self):
        for point in self.path.points:
            rect = Unit.calculate_rect(point, self.radius - 2)
            pygame.draw.rect(screen, COLOR_YELLOW, rect)


    def print(self):
        print("--Unit id: ", self.id, "  x: ", self.tile.x, "  y: ", self.tile.y)


    def change_weights_for_types(self, weights, unitTypes, data, flip_direction = False):
        nearby_targets = MAP.get_units_near_unit_of_types(self, data[0][0], data[0][1], unitTypes)
        if len(nearby_targets) > 0:
            # calculate average deer position
            total_x = 0
            total_y = 0
            for deer in nearby_targets:
                total_x = total_x + deer.tile.x
                total_y = total_y + deer.tile.y        
            average = Point(float(total_x) / len(nearby_targets), float(total_y) / len(nearby_targets))
            diff = average - self.tile
            # only do something if we're not at the average
            if diff != Vector(0,0):
                if flip_direction == True: 
                    diff.flip()
                direction_target = diff.to_direction_number()

                direction_lower = direction_target - 1
                if direction_lower < 0 : direction_lower = 7

                direction_upper = direction_target + 1
                if direction_upper > 7 : direction_upper = 0

                weights[direction_target][0] = data[0][2](weights[direction_target][0], data[0][3])
                weights[direction_lower][0] = data[0][2](weights[direction_lower][0], data[0][3])
                weights[direction_upper][0] = data[0][2](weights[direction_upper][0], data[0][3])
            return True
        else:
            return False


    def change_weights_if_blocked(self, weights, unitTypes):
        for i in range(8):
            new_tile = self.tile + DIRECTION_VECTORS[i]
            if MAP.tile_within_bounds(new_tile) == False:
                # print("correction bounds")
                weights[i][0] = 0

            unit = MAP.get_unit_at(new_tile)
            if type(unit) in unitTypes:
                # print("correction type")
                weights[i][0] = 0


    def get_vector_from_weights(weights):
        direction_number = weighted_random(((0,weights[0][0]), (1,weights[1][0]), (2,weights[2][0]), (3,weights[3][0]), (4,weights[4][0]), (5,weights[5][0]), (6,weights[6][0]), (7,weights[7][0])))
        if direction_number is not None:
            return DIRECTION_VECTORS[direction_number]
        return None


    def kill_deer_at_tile(self, tile):
        global deer_killed
        unit = MAP.get_unit_at(tile)
        if type(unit) == Deer:
            deer_killed = deer_killed + 1
            if deer_killed % 10 == 0: print(deer_killed, " deer killed")
            MAP.remove_unit(unit)
            self.satiation = randint(1000, 1000)
            self.color = COLOR_PINK


        
class Deer(Unit):
    def __init__(self, tile):
        self.name = "deer"
        Unit.init_a(self, tile)
        self.color = UNIT_COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.target = None
        self.move_in = 5
        Unit.init_b(self, tile)


    def update_target(self):
        weight_n = [100]
        weight_ne = [100]
        weight_e = [100]
        weight_se = [100]
        weight_s = [100]
        weight_sw = [100]
        weight_w = [100]
        weight_nw = [100]
        weights = [weight_n, weight_ne, weight_e, weight_se, weight_s, weight_sw, weight_w, weight_nw]  

        # Group up
        # if not Unit.change_weights_for_types(self, weights, {Deer}, [(0, 15, ADD, 6)]):
        Unit.change_weights_for_types(self, weights, {Deer}, [(0, 40, ADD, 20)])
        # Run away from baddies
        if not Unit.change_weights_for_types(self, weights, {Wolf, Bear}, [(0, 20, ADD, 100)], flip_direction = True):
            Unit.change_weights_for_types(self, weights,    {Wolf, Bear}, [(0, 40, ADD, 20)], flip_direction = True)  

        # Don't run into stuff
        Unit.change_weights_if_blocked(self, weights, {Block, Deer, Wolf, Bear})
        vector = Unit.get_vector_from_weights(weights)
        # Move
        if vector is not None:
            target = self.tile + vector
            self.path.append(target)


class Wolf(Unit):
    def __init__(self, tile):
        self.name = "wolf"
        Unit.init_a(self, tile)
        self.color = UNIT_COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.satiation = 0
        Unit.init_b(self, tile)


    def update_target(self):
        weight_n = [100]
        weight_ne = [100]
        weight_e = [100]
        weight_se = [100]
        weight_s = [100]
        weight_sw = [100]
        weight_w = [100]
        weight_nw = [100]
        weights = [weight_n, weight_ne, weight_e, weight_se, weight_s, weight_sw, weight_w, weight_nw] 

        # Each Other
        Unit.change_weights_for_types(self, weights, {Wolf}, [(0, 40, ADD, 20)])
        # Deer
        if self.satiation > 0:
            self.satiation = self.satiation - 1
            self.color = COLOR_PINK
        else:
            self.color = UNIT_COLOR_WOLF
            if not Unit.change_weights_for_types(self, weights, {Deer}, [(0, 20, ADD, 50)]):
                Unit.change_weights_for_types(self, weights, {Deer}, [(0, 40, ADD, 20)])
        # Run away from bear
        if not Unit.change_weights_for_types(self, weights, {Bear}, [(0, 20, ADD, 100)], flip_direction = True):
            Unit.change_weights_for_types(self, weights,    {Bear}, [(0, 40, ADD, 20)], flip_direction = True)              
        # Don't run into stuff
        Unit.change_weights_if_blocked(self, weights, {Block, Wolf, Bear})
        vector = Unit.get_vector_from_weights(weights)
        # Move and kill any deer you hit
        if vector is not None:
            target = self.tile + vector
            self.kill_deer_at_tile(target)
            self.path.append(target)


class Bear(Unit):
    def __init__(self, tile):
        self.name = "bear"
        Unit.init_a(self, tile)
        self.color = COLOR_GREY_LIGHT
        self.radius = UNIT_RADIUS_WOLF
        self.path = list()
        self.add_path()
        Unit.init_b(self, tile)


    def add_path(self):
        target = self.get_target()
        # target = Point(x = 5, y = 10)
        x = self.tile.x
        y = self.tile.y
        if target.x == self.tile.x:
            if target.y > self.tile.y:
                for i in range(target.y - self.tile.y):
                    y = y + 1
                    self.path.append(Point(x=x, y=y))
            else:
                for i in range(self.tile.y - target.y):
                    y = y -1
                    self.path.append(Point(x=x, y=y))
        else:
            if target.x > self.tile.x:
                for i in range(target.x - self.tile.x):
                    x = x + 1
                    self.path.append(Point(x=x, y=y))
            else:
                for i in range(self.tile.x - target.x):
                    x = x -1
                    self.path.append(Point(x=x, y=y))


    def get_target(self):
        i = randint(0, TILE_COUNT - 1)
        if randint(0, 1) == 0:
            return Point(x = self.tile.x, y = i)
        else:
            return Point(x = i, y = self.tile.y)


    def update(self):
        if len(self.path) > 0:
            if randint(0, 9) == 0:
                if type(MAP.get_unit_at(self.path[0])) in {Block, Wolf, Deer}:
                    self.path.clear()
                else:
                    self.move_to(self.path.pop(0))
        else:
            if randint(0, 9) == 0:
                self.add_path()



class Person(Unit):
    def __init__(self, tile):
        self.name = "person"
        Unit.init_a(self, tile)
        self.color = UNIT_COLOR_PERSON
        self.radius = UNIT_RADIUS_PERSON
        self.move_in = 25
        self.move_period = 25
        self.moving_right = True
        self.move_distance = 20
        Unit.init_b(self, tile)


    def update_target(self):
        pass
        # point_index = Point(x = self.tile.x, y = self.tile.y)
        # global person_move

        # for i in range(self.move_distance):
        #     if self.moving_right:
        #         point_index.x = point_index.x + 1
        #     else:
        #         point_index.x = point_index.x - 1
        #     new_point = point_index.copy()
        #     self.path.append(new_point)
        # self.moving_right = not self.moving_right
        # self.path.print()



class Block(Unit):
    def __init__(self, tile):
        self.name = "block"
        Unit.init_a(self, tile)
        self.color = COLOR_GREY_DARK
        self.radius = UNIT_RADIUS_BLOCK
        Unit.init_b(self, tile)


def create_block_line(tile_1, tile_2) :
    # vertical
    if tile_1.x == tile_2.x and tile_1.y < tile_2.y:
        for i in range(tile_2.y - tile_1.y + 1):
            Block(Point(x = tile_1.x, y = tile_1.y + i))
    # horizontal
    elif tile_1.y == tile_2.y and tile_1.x < tile_2.x:
        pass