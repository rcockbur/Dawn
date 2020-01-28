from globals import *       #includes point
import pygame

print("running map.py")

class Map:
    def __init__(self):
        self.grid = list()

        self.entities = dict()

        for i in range(TILE_COUNT_X):
            self.grid.append(list())
            for j in range(TILE_COUNT_Y):
                self.grid[i].append(None)
        
    def tile_within_bounds(self, pos):
        return pos[0] >= 0 and pos[1] >= 0 and pos[0] < TILE_COUNT_X and pos[1] < TILE_COUNT_Y

    def get_entities(self):
        return self.entities.values()

    def get_entities_of_type(self, _type):
        r = set()
        for entity in self.entities.values():
            if type(entity) == _type:
                r.add(entity)
        return r

    def add_entity_at_tile(self, entity, tile):
        self.grid[tile[0]][tile[1]] = entity
        self.entities[entity.id] = entity

    def remove_entity(self, entity):
        # print("death of", entity.name)
        if self.get_entity_at_tile(entity.tile) is not None:
            self.grid[entity.tile[0]][entity.tile[1]] = None
        del self.entities[entity.id]
        if entity in selected_entities:
            selected_entities.remove(entity)

    def move_entity(self, entity, from_tile, to_tile):
        target_entity = self.grid[to_tile[0]][to_tile[1]]
        if target_entity is not None and target_entity.is_dead == False:
            print(entity.name, "stomping on", target_entity.name)
        self.grid[from_tile[0]][from_tile[1]] = None
        self.grid[to_tile[0]][to_tile[1]] = entity

    def get_entity_at_tile(self, tile):
        if 0 <= tile[0] < len(self.grid) and 0 <= tile[1] < len(self.grid[0]):
            return self.grid[tile[0]][tile[1]]
        else:
            return None

    def get_entities_in_box(self, corner_1, corner_3):
        if corner_1[0] < corner_3[0]:
            low_x = corner_1[0]
            high_x = corner_3[0]
        else:
            low_x = corner_3[0]
            high_x = corner_1[0]

        if corner_1[1] < corner_3[1]:
            low_y = corner_1[1]
            high_y = corner_3[1]
        else:
            low_y = corner_3[1]
            high_y = corner_1[1]


        matching_entities = set()
        for entity in self.entities.values():
            if low_x <= entity.tile[0] <= high_x:
                if low_y <= entity.tile[1] <= high_y:
                    matching_entities.add(entity)
        return matching_entities

    def print(self):
        print("Map Grid Entities:")
        for i in range(TILE_COUNT_X):
            for j in range(TILE_COUNT_Y):
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
    elif x > GRID_OFFSET_X + GRID_SIZE_X:
        x = GRID_OFFSET_X + GRID_SIZE_X
    if y < GRID_OFFSET_Y: 
        y = GRID_OFFSET_Y
    elif y > GRID_OFFSET_Y + GRID_SIZE_Y:
        y = GRID_OFFSET_Y + GRID_SIZE_Y
    return (x, y)

def tile_from_pos(pos):
    if GRID_OFFSET_X <= pos[0] <= GRID_OFFSET_X + GRID_SIZE_X and GRID_OFFSET_Y <= pos[1] <= GRID_OFFSET_Y + GRID_SIZE_Y:
        tile_x = int((pos[0] - GRID_OFFSET_X) / TILE_SPACING)
        tile_y = int((pos[1] - GRID_OFFSET_Y) / TILE_SPACING)
        return (tile_x, tile_y)
    return None

def pos_within_bounds(pos):
    return GRID_OFFSET_X < pos[0] < GRID_OFFSET_X + GRID_SIZE_X and GRID_OFFSET_Y < pos[1] < GRID_OFFSET_Y + GRID_SIZE_Y

def calculate_rect(tile, radius):
        pos = (tile_get_mid_x(tile[0]) - radius, tile_get_mid_y(tile[1]) - radius)
        return pygame.Rect(pos[0], pos[1], radius * 2, radius * 2)

def tile_get_mid_x(tile_x):
    return GRID_OFFSET_X + tile_x * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1

def tile_get_mid_y(tile_y):
    return GRID_OFFSET_Y + tile_y * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1


