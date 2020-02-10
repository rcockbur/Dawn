import pygame
from globals import *
from block import Block, Grass
from unit import Unit, Deer, Person, Wolf
from map import calculate_rect
print("running draw.py")



# freesansbold_12 = pygame.font.Font('freesansbold.ttf', 12) 
FONT_SIZE = 16
freesansbold_12 = pygame.font.SysFont('Monospace', FONT_SIZE) 


def draw_everything(mouse_pos_start = None, mouse_pos_clamped = None):
    draw_black()
    draw_grid()              
    for entity in MAP.get_entities():
        if isinstance(entity, Unit):
            draw_unit(entity)
        else:
            draw_block(entity)
    for entity in MAP.get_entities():
        if entity.is_selected == True:
            draw_unit_highlight(entity)
    for entity in MAP.get_entities():
        if isinstance(entity, Unit):
            draw_path(entity)
    draw_hud()
    if mouse_pos_start is not None:
        draw_box(mouse_pos_start, mouse_pos_clamped)

draw_function[0] = draw_everything

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_WHITE, COLOR_BACKGROUND) 
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
    return offset_y + FONT_SIZE

def full_crop(grass):
    return grass.crop_current >= grass.crop_max

def draw_hud():
    Y = 8
    draw_text_pair((GRID_OFFSET_X + 5, Y),   0, [ ("Grass:", 0),     (str(len(list(filter(full_crop, MAP.get_entities_of_type(Grass))))) + "/" + str(len(MAP.get_entities_of_type(Grass))), 80) ])
    draw_text_pair((GRID_OFFSET_X + 250, Y), 0, [ ("Deer:", 0),     (str(len(MAP.get_entities_of_type(Deer))), 70) ])
    draw_text_pair((GRID_OFFSET_X + 450, Y), 0, [ ("Wolves:", 0),     (str(len(MAP.get_entities_of_type(Wolf))), 95) ])
    draw_text_pair((GRID_OFFSET_X + 650, Y), 0, [ ("People:", 0),     (str(len(MAP.get_entities_of_type(Person))), 95) ])
    draw_text_pair((GRID_OFFSET_X + 850, Y), 0, [ ("Date:", 0),     (get_date_string(), 125) ])
    s = str(tick_of_day[0]) + ":00"
    if tick_of_day[0] < 10: s = "0" + s
    draw_text_at(freesansbold_12, s, (GRID_OFFSET_X + 910, Y))
    # draw_text_at(freesansbold_12, str(year[0]), (GRID_OFFSET_X + 800, 7))

    offset_y = GRID_OFFSET_Y
    for selected_entity in selected_entities:
        if isinstance(selected_entity, Unit): 
            offset_y = offset_y + draw_unit_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
        if isinstance(selected_entity, Block): 
            offset_y = offset_y + draw_block_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
        if isinstance(selected_entity, Grass): 
            offset_y = offset_y + draw_grass_info(selected_entity, (GRID_SIZE_X + GRID_OFFSET_X + 5, offset_y))
                   
def draw_unit_info(unit, pos):
    row_x = 110
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (unit.name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (unit.class_name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (unit.get_tile_string(), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Status", 0),   (unit.get_status_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Target", 0),   (unit.get_target_string(), row_x) ])
    
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Age", 0),     (str(unit.age), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Birthday", 0),     (unit.get_birthday_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Hungery", 0),   (unit.get_hungery_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Kills", 0),    (str(unit.kills), row_x)])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Idle", 0),   (str(unit.idle_current), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Move In", 0),   (str(unit.move_current), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Sex", 0),   (unit.get_sex_string(), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Food", 0),     (unit.get_food_string(), row_x) ])
    if unit.is_male == False:
        # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Fertile", 0),   (unit.get_fertile_string(), row_x) ])
        offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Due", 0),   (unit.get_pregnant_string(), row_x) ])
    return offset_y + FONT_SIZE

def draw_block_info(block, pos):
    row_x = 110
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (block.name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (block.class_name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (block.get_tile_string(), row_x) ])
    return offset_y + FONT_SIZE

def draw_grass_info(grass, pos):
    row_x = 110
    offset_y = 0
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Name", 0),     (grass.name, row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Marked", 0),     (grass.get_marked_string(), row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Class", 0),    (grass.class_name, row_x) ])
    # offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Tile", 0),      (grass.get_tile_string(), row_x) ])
    offset_y = draw_text_pair((pos[0], pos[1]), offset_y, [ ("Crop", 0),      (str(grass.crop_current), row_x) ])
    return offset_y + FONT_SIZE

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
    if get_debug_status():
        if unit.is_male == False:
            if unit.pregnant_until is not None:
                outter_rect = calculate_rect(unit.tile, unit.radius)    
                pygame.draw.rect(screen, COLOR_BABY_BLUE, outter_rect, 1)
            elif unit.is_fertile == True:
                outter_rect = calculate_rect(unit.tile, unit.radius)    
                pygame.draw.rect(screen, COLOR_PINK, outter_rect, 1)
        
            
        if unit.satiation_current <= unit.satiation_hungery:
            if unit.satiation_current > unit.satiation_starving:
                outter_rect = calculate_rect(unit.tile, 2)    
                pygame.draw.rect(screen, COLOR_RED, outter_rect)
            else:
                outter_rect = calculate_rect(unit.tile, 4)    
                pygame.draw.rect(screen, COLOR_RED, outter_rect)

def draw_unit_highlight(unit):
    outter_rect = calculate_rect(unit.tile, unit.radius+2)    
    pygame.draw.rect(screen, COLOR_SELECTION_HIGHLIGHT, outter_rect, 1)

def draw_path(unit):
    if unit.is_selected or get_debug_path():
        for ability in unit.ability_list:
            if hasattr(ability, 'path'):
                path = ability.path
            elif hasattr(ability.approach, 'path'):
                path = ability.approach.path
            else:
                path = None
            
            if path is not None:
                for point in path.points:
                    rect = calculate_rect(point, 2)
                    pygame.draw.rect(screen, ability.color, rect)

def draw_black():
    screen.fill(COLOR_BACKGROUND) 