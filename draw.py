import pygame
from globals import *
from unit import Deer
from map import calculate_rect

print("running draw.py")



freesansbold_12 = pygame.font.Font('freesansbold.ttf', 12) 

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_GREEN, COLOR_BLACK) 
    textRect = text.get_rect() 
    textRect.topleft = pos
    screen.blit(text, textRect)

def draw_hud():
        #num_deer
    string = "Deer: " + str(len(MAP.get_entities_of_type(Deer)))
    draw_text_at(freesansbold_12, string, (GRID_OFFSET_X, 0))

    offset_y = 5

    for selected_unit in selected_units:

        string = "name:    " + selected_unit.name
        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y))        

        string = "class:     " + selected_unit.class_name        
        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y + 15))        

        string = "pos:       " + str(selected_unit.tile.x) + " , " + str(selected_unit.tile.y)
        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y + 30))

        string = "kills:       " + str(selected_unit.kills)
        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y + 45))

        string = "food:      " + str(selected_unit.satiation_current)
        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y + 60))

        if selected_unit.path.size() > 0:
            string = "target:   " + str(selected_unit.path.get(-1).x) + " , " + str(selected_unit.path.get(-1).y)
        else:
            string = "target:    -"

        draw_text_at(freesansbold_12, string, (GRID_SIZE + GRID_OFFSET_X + 5, offset_y + 75))   

        offset_y = offset_y + 100

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