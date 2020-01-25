import pygame
from globals import *
from block import Block
from unit import Unit, Deer
from map import calculate_rect

print("running draw.py")



freesansbold_12 = pygame.font.Font('freesansbold.ttf', 12) 

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_GREEN, COLOR_BLACK) 
    textRect = text.get_rect() 
    textRect.topleft = pos
    screen.blit(text, textRect)

def draw_hud():
    draw_text_pair((GRID_OFFSET_X, 7),  [ ("Deer", 0),     (str(len(MAP.get_entities_of_type(Deer))), 50) ])

    offset_y = GRID_OFFSET_Y
    for selected_unit in selected_units:
        if isinstance(selected_unit, Unit): 
            offset_y = offset_y + draw_unit_info(selected_unit, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y))
        if isinstance(selected_unit, Block): 
            offset_y = offset_y + draw_block_info(selected_unit, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y))

def draw_text_pair(pos, string_offset_pairs):
    x = pos[0]
    y = pos[1]
    for string_offset_pair in string_offset_pairs:
        string = string_offset_pair[0]
        offset = string_offset_pair[1]
        draw_text_at(freesansbold_12, string, (x + offset, y))
        
            
def draw_unit_info(unit, pos):
    row_x = 50
    draw_text_pair((pos[0], pos[1] + 0),  [ ("name", 0),     (unit.name, row_x) ])
    draw_text_pair((pos[0], pos[1] + 15), [ ("class", 0),    (unit.class_name, row_x) ])
    draw_text_pair((pos[0], pos[1] + 30), [ ("pos", 0),      (unit.get_tile_string(), row_x) ])
    draw_text_pair((pos[0], pos[1] + 45), [ ("kills", 0),    (str(unit.kills), row_x)])
    draw_text_pair((pos[0], pos[1] + 60), [ ("food", 0),     (str(unit.satiation_current), row_x) ])
    draw_text_pair((pos[0], pos[1] + 75), [ ("target", 0),   (unit.get_target_string(), row_x) ])
    draw_text_pair((pos[0], pos[1] + 90), [ ("status", 0),   (unit.get_status_string(), row_x) ])
    return 120  

def draw_block_info(block, pos):
    row_x = 50 
    draw_text_pair((pos[0], pos[1] + 0),  [ ("name", 0),     (block.name, row_x) ])
    draw_text_pair((pos[0], pos[1] + 15), [ ("class", 0),    (block.class_name, row_x) ])
    draw_text_pair((pos[0], pos[1] + 30), [ ("pos", 0),      (block.get_tile_string(), row_x) ])
    return 60

def draw_grid():
    for i in range(TILE_COUNT + 1):
        draw_line((GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), (GRID_SIZE + GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)
        draw_line((i * TILE_SPACING + GRID_OFFSET_X, GRID_OFFSET_Y), (i * TILE_SPACING + GRID_OFFSET_X, GRID_SIZE + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)

def draw_line(point_1, point_2, color, width):
    pygame.draw.line(screen, color, point_1, point_2, width)

def draw_box(corner_1, corner_3):
    color = COLOR_WHITE
    corner_2 = (corner_1[0], corner_3[1])
    corner_4 = (corner_3[0], corner_1[1])
    pygame.draw.line(screen, color, corner_1, corner_2, 1)
    pygame.draw.line(screen, color, corner_1, corner_4, 1)
    pygame.draw.line(screen, color, corner_2, corner_3, 1)
    pygame.draw.line(screen, color, corner_4, corner_3, 1)

def draw_unit(unit):
    if unit.is_selected:
        outter_rect = calculate_rect(unit.tile, unit.radius+2)    
        pygame.draw.rect(screen, COLOR_YELLOW, outter_rect)
    rect = calculate_rect(unit.tile, unit.radius)
    pygame.draw.rect(screen, unit.color, rect)

def draw_path(unit):
    if unit.is_selected:
        if unit.path is not None:
            for point in unit.path.points:
                rect = calculate_rect(point, unit.radius - 4)
                pygame.draw.rect(screen, (155, 155, 0), rect)

def draw_black():
    screen.fill(COLOR_BLACK) 