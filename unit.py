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


    def __init__(self, tile):
        self.id = Unit.new_id()
        self.tile = tile
        self.path = Path(list())
        self.target = None
        self.update_pos()
        self.update_rect()

        MAP.add_unit_at(self, tile.x, tile.y)
        return self


    def update(self):   
        if self.path.size() == 0:
            self.update_target()
        if self.path.size() > 0:
            self.move_to(self.path.pop())


    def update_target(self):
        raise NotImplementedError()


    def update_pos(self):
        x = tile_get_mid_x(self.tile.x) - self.radius
        y = tile_get_mid_y(self.tile.y) - self.radius

        self.pos = Point(x=x, y=y)


    def set_path(self, path):
        self.path = path
        

    def update_rect(self):
        self.rect = pygame.Rect(self.pos.x, self.pos.y, self.radius * 2, self.radius * 2)


    def move_by(self, vector):
        target = self.tile + vector
        self.move_to(target)


    def move_to(self, target):
        if MAP.pos_within_bounds(target):
            old_tile = self.tile.copy()
            self.tile = target.copy()
            MAP.move_unit(self, old_tile, self.tile)
            self.update_pos()
            self.update_rect()
            

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        if self.path is not None:
            self.draw_path()


    def draw_path(self):
        # print(self.path.points)
        for point in self.path.points:
            rect = pygame.Rect(point.x, point.y, 3, 3)
            pygame.draw.rect(screen, COLOR_PINK, rect)


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
            if not MAP.pos_within_bounds(new_tile) or type(MAP.get_unit_at(new_tile)) in unitTypes:
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


class Block(Unit):
    def __init__(self, tile):
        self.color = COLOR_GREY_DARK
        self.radius = UNIT_RADIUS_BLOCK
        Unit.__init__(self, tile)

        
class Deer(Unit):
    def __init__(self, tile):
        self.color = UNIT_COLOR_DEER
        self.radius = UNIT_RADIUS_DEER
        self.target = None
        Unit.__init__(self, tile)


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
        self.color = UNIT_COLOR_WOLF
        self.radius = UNIT_RADIUS_WOLF
        self.satiation = 0
        Unit.__init__(self, tile)


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
        self.color = COLOR_GREY_LIGHT
        self.radius = UNIT_RADIUS_WOLF
        Unit.__init__(self, tile)
        self.path = list()
        self.add_path()


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


def create_block_line(tile_1, tile_2) :
    # vertical
    if tile_1.x == tile_2.x and tile_1.y < tile_2.y:
        for i in range(tile_2.y - tile_1.y + 1):
            Block(Point(x = tile_1.x, y = tile_1.y + i))
    # horizontal
    elif tile_1.y == tile_2.y and tile_1.x < tile_2.x:
        pass