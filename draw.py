import pygame
from globals import *
from block import Block, Grass
from unit import Unit, Deer, Person, Wolf
from map import calculate_rect
print("running draw.py")

freesansbold_12 = pygame.font.Font('freesansbold.ttf', 12) 

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_TEXT_GREEN, COLOR_BACKGROUND) 
    textRect = text.get_rect() 
    textRect.topleft = pos
    screen.blit(text, textRect)

def draw_text_pair(pos, offset_y, string_offset_pairs):
    x = pos[0]
    y = pos[1] + offset_y
    for string_offset_pair in string_offset_pairs:
        string = string_offset_pair[0]
        offset = string_offset_pair[1]
        draw_text_at(freesansbold_12, string, (x + offset, y))
    return offset_y + 15

def draw_hud():
    draw_text_pair((GRID_OFFSET_X + 0, 7),   0, [ ("Deer:", 0),     (str(len(MAP.get_entities_of_type(Deer))), 100) ])
    draw_text_pair((GRID_OFFSET_X + 200, 7), 0, [ ("Wolves:", 0),     (str(len(MAP.get_entities_of_type(Wolf))), 100) ])
    draw_text_pair((GRID_OFFSET_X + 400, 7), 0, [ ("People:", 0),     (str(len(MAP.get_entities_of_type(Person))), 100) ])
    draw_text_pair((GRID_OFFSET_X + 600, 7), 0, [ ("Sim Ticks:", 0),     (str(sim_tick[0]), 100) ])
    draw_text_pair((GRID_OFFSET_X + 800, 7), 0, [ ("Years:", 0),     (str(sim_tick[0]//TICKS_PER_YEAR), 100) ])

    offset_y = GRID_OFFSET_Y
    for selected_entity in selected_entities:
        if isinstance(selected_entity, Unit): 
            offset_y = offset_y + draw_unit_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
        if isinstance(selected_entity, Block): 
            offset_y = offset_y + draw_block_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
        if isinstance(selected_entity, Grass): 
            offset_y = offset_y + draw_grass_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
                   
def draw_unit_info(unit, pos):
    row_x = 55
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (unit.name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (unit.class_name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (unit.get_tile_string(), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Status", 0),   (unit.get_status_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Target", 0),   (unit.get_target_string(), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Food", 0),     (str(unit.satiation_current), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Age", 0),     (str(unit.age), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Birthday", 0),     (str(unit.birthday), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Hungery", 0),   (unit.get_hungery_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Kills", 0),    (str(unit.kills), row_x)])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Idle", 0),   (str(unit.idle_current), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Move In", 0),   (str(unit.move_current), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Sex", 0),   (unit.get_gender_string(), row_x) ])
    if unit.is_male == False:
        offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Fertile", 0),   (unit.get_fertile_string(), row_x) ])
        offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Due", 0),   (unit.get_pregnant_string(), row_x) ])
    return offset_y + 10

def draw_block_info(block, pos):
    row_x = 50 
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (block.name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (block.class_name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (block.get_tile_string(), row_x) ])
    return offset_y + 15

def draw_grass_info(grass, pos):
    row_x = 50 
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (grass.name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Marked", 0),     (grass.get_marked_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (grass.class_name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (grass.get_tile_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Crop", 0),      (str(grass.crop_current), row_x) ])
    return offset_y + 15

def draw_grid():
    for i in range(TILE_COUNT_X + 1):
        draw_line((i * TILE_SPACING + GRID_OFFSET_X, GRID_OFFSET_Y), (i * TILE_SPACING + GRID_OFFSET_X, GRID_SIZE_Y + GRID_OFFSET_Y), COLOR_GRID, LINE_WIDTH)
        
    for i in range(TILE_COUNT_Y+1):
        draw_line((GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), (GRID_SIZE_X + GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), COLOR_GRID, LINE_WIDTH)
        
def draw_line(pos_1, pos_2, color, width):
    pygame.draw.line(screen, color, pos_1, pos_2, width)

def draw_box(tile_1, tile_3):
    tile_2 = (tile_1[0], tile_3[1])
    tile_4 = (tile_3[0], tile_1[1])
    pygame.draw.line(screen, COLOR_SELECTION_BOX, tile_1, tile_2, 1)
    pygame.draw.line(screen, COLOR_SELECTION_BOX, tile_1, tile_4, 1)
    pygame.draw.line(screen, COLOR_SELECTION_BOX, tile_2, tile_3, 1)
    pygame.draw.line(screen, COLOR_SELECTION_BOX, tile_4, tile_3, 1)

def draw_block(block):
    rect = calculate_rect(block.tile, block.radius)
    pygame.draw.rect(screen, block.color, rect)

def draw_unit(unit):
    rect = calculate_rect(unit.tile, unit.radius)
    pygame.draw.rect(screen, unit.color, rect)
    if unit.is_male == False:
        if unit.pregnant_until is not None:
            outter_rect = calculate_rect(unit.tile, unit.radius)    
            pygame.draw.rect(screen, COLOR_PINK, outter_rect, 1)
        elif unit.is_fertile == True:
            pass
            # outter_rect = calculate_rect(unit.tile, unit.radius)    
            # pygame.draw.rect(screen, COLOR_PINK, outter_rect, 1)
    
        
    if unit.satiation_current < 0:
        if unit.satiation_current > unit.satiation_starving:
            outter_rect = calculate_rect(unit.tile, 2)    
            pygame.draw.rect(screen, COLOR_RED, outter_rect)
        else:
            outter_rect = calculate_rect(unit.tile, 4)    
            pygame.draw.rect(screen, COLOR_RED, outter_rect)

def draw_unit_highlight(unit):
    outter_rect = calculate_rect(unit.tile, unit.radius+1)    
    pygame.draw.rect(screen, COLOR_SELECTION_HIGHLIGHT, outter_rect, 1)

def draw_path(unit):
    if unit.is_selected or get_debug_path():
        if unit.path.size() > 0:
            color = PATH_COLORS[unit.status]
            for point in unit.path.points:
                rect = calculate_rect(point, 2)
                pygame.draw.rect(screen, color, rect)

def draw_black():
    screen.fill(COLOR_BACKGROUND) 