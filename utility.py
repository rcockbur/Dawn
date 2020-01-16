from globals import *
from random import randint

def weighted_random(pairs):
    boundary_temp = 0
    boundaries = [boundary_temp]
    num_pairs = 0
    for pair in pairs:
        num_pairs+=1
        boundary_temp = boundary_temp + pair[1]
        boundaries.append(boundary_temp)
    if boundaries[num_pairs] > 0:
        chosen_int = randint(0, boundaries[num_pairs]-1)
        for boundary_lower in range(num_pairs):
            boundary_upper = boundary_lower + 1
            if boundaries[boundary_upper] > boundaries[boundary_lower]:
                if boundaries[boundary_upper] > chosen_int >= boundaries[boundary_lower]:
                    return pairs[boundary_lower][0]
        raise RuntimeError("No direction found")
    return None

def tile_get_mid_x(tile_x):
    return GRID_OFFSET_X + tile_x * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1

def tile_get_mid_y(tile_y):
    return GRID_OFFSET_Y + tile_y * TILE_SPACING + TILE_RADIUS + LINE_WIDTH / 2 + 1

def get_tiles_for_line(tile_a, tile_b):
    pass

def ADD(a, b):
    return a + b

def SUB(a, b):
    return a - b

def MUL(a, b):
    return int(a * b)

def DIV(a, b):
    return int(a / b)

def SET(a, b):
    return b


def draw_grid():
    for i in range(TILE_COUNT + 1):
        draw_line((GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), (GRID_SIZE + GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)
        draw_line((i * TILE_SPACING + GRID_OFFSET_X, GRID_OFFSET_Y), (i * TILE_SPACING + GRID_OFFSET_X, GRID_SIZE + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)

def draw_line(point_1, point_2, color, width):
    pygame.draw.line(screen, color, point_1, point_2, width)

def print_debug():
    print("Units:")
    w1.print()
    w2.print()
    map.print()  


