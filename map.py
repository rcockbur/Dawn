from globals import *       #includes point
import pygame

print("running map.py")

class Map:
    def __init__(self):
        self.grid = list()

        self.entities = dict()

        for i in range(TILE_COUNT):
            self.grid.append(list())
            for j in range(TILE_COUNT):
                self.grid[i].append(None)
        
    def tile_within_bounds(self, pos):
        return pos.x >= 0 and pos.y >= 0 and pos.x < TILE_COUNT and pos.y < TILE_COUNT

    def get_entities(self):
        return self.entities.values()

    def get_entities_of_type(self, _type):
        r = set()
        for entity in self.entities.values():
            if type(entity) == _type:
                r.add(entity)
        return r

    def add_entity_at(self, entity, x, y):
        self.grid[x][y] = entity
        self.entities[entity.id] = entity

    def remove_entity(self, entity):
        if self.get_entity_at(entity.tile) is not None:
            self.grid[entity.tile.x][entity.tile.y] = None
        del self.entities[entity.id]

    def move_entity(self, entity, from_tile, to_tile):
        target_entity = self.grid[to_tile.x][to_tile.y]
        if target_entity is not None and target_entity.is_dead == False:
            print(entity.name, "stomping on", target_entity.name)
        self.grid[from_tile.x][from_tile.y] = None
        self.grid[to_tile.x][to_tile.y] = entity

    def get_entity_at(self, tile):
        if 0 <= tile.x < len(self.grid) and 0 <= tile.y < len(self.grid[0]):
            return self.grid[tile.x][tile.y]
        else:
            return None

    def get_entities_in_box(self, corner_1, corner_3):
        if corner_1.x < corner_3.x:
            low_x = corner_1.x
            high_x = corner_3.x
        else:
            low_x = corner_3.x
            high_x = corner_1.x

        if corner_1.y < corner_3.y:
            low_y = corner_1.y
            high_y = corner_3.y
        else:
            low_y = corner_3.y
            high_y = corner_1.y


        matching_entities = set()
        for entity in self.entities.values():
            if low_x <= entity.tile.x <= high_x:
                if low_y <= entity.tile.y <= high_y:
                    matching_entities.add(entity)
        return matching_entities

    def print(self):
        print("Map Grid Entities:")
        for i in range(TILE_COUNT):
            for j in range(TILE_COUNT):
                if self.grid[i][j] is not None:
                    # self.grid[i][j].print()
                    print("--Entity id: ", self.grid[i][j].id, "  x: ", i, "  y: ", j)
        print("Map Dict Entities:")
        for k, v in self.entities.items():
            v.print()

def clamp_pos(pos):
    x = pos[0]
    y = pos[1]
    if x < GRID_OFFSET_X: 
        x = GRID_OFFSET_X
    elif x > GRID_OFFSET_X + GRID_SIZE:
        x = GRID_OFFSET_X + GRID_SIZE
    if y < GRID_OFFSET_Y: 
        y = GRID_OFFSET_Y
    elif y > GRID_OFFSET_Y + GRID_SIZE:
        y = GRID_OFFSET_Y + GRID_SIZE
    return (x, y)

def tile_from_pos(pos):
    if GRID_OFFSET_X <= pos[0] <= GRID_OFFSET_X + GRID_SIZE and GRID_OFFSET_Y <= pos[1] <= GRID_OFFSET_Y + GRID_SIZE:
        tile_x = int((pos[0] - GRID_OFFSET_X) / TILE_SPACING)
        tile_y = int((pos[1] - GRID_OFFSET_Y) / TILE_SPACING)
        return Point(tile_x, tile_y)
    return None

def pos_within_bounds(pos):
    return GRID_OFFSET_X < pos[0] < GRID_OFFSET_X + GRID_SIZE and GRID_OFFSET_Y < pos[1] < GRID_OFFSET_Y + GRID_SIZE

def calculate_rect(tile, radius):
        pos = Point(tile_get_mid_x(tile.x) - radius, tile_get_mid_y(tile.y) - radius)
        return pygame.Rect(pos.x, pos.y, radius * 2, radius * 2)

def tile_get_mid_x(tile_x):
    return GRID_OFFSET_X + tile_x * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1

def tile_get_mid_y(tile_y):
    return GRID_OFFSET_Y + tile_y * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1


