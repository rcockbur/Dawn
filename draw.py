import pygame
from globals import *
from unit import Deer

print("running draw.py")


freesansbold_14 = pygame.font.Font('freesansbold.ttf', 14) 

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_GREEN, COLOR_BLACK) 
    textRect = text.get_rect() 
    textRect.topleft = pos
    screen.blit(text, textRect)

def draw_hud():
        #num_deer
    string = "Deer: " + str(len(MAP.get_units_of_type(Deer)))
    draw_text_at(freesansbold_14, string, (GRID_OFFSET_X, 0))

    if selected_unit[0] is not None:
        string = "class:    " + selected_unit[0].class_name()
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 100))        

        string = "name:   " + selected_unit[0].name
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 120))        

        string = "pos:      " + str(selected_unit[0].tile.x) + "," + str(selected_unit[0].tile.y)
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 140))

        string = "kills:      " + str(selected_unit[0].kills)
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 160))

        string = "food:     " + str(selected_unit[0].satiation_current)
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 180))

        if selected_unit[0].path.size() > 0:
            string = "target:  (" + str(selected_unit[0].path.get(-1).x) + "," + str(selected_unit[0].path.get(-1).y) + ")"
            draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 200))   

def draw_grid():
    for i in range(TILE_COUNT + 1):
        draw_line((GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), (GRID_SIZE + GRID_OFFSET_X, i * TILE_SPACING + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)
        draw_line((i * TILE_SPACING + GRID_OFFSET_X, GRID_OFFSET_Y), (i * TILE_SPACING + GRID_OFFSET_X, GRID_SIZE + GRID_OFFSET_Y), GRID_COLOR, LINE_WIDTH)



def draw_line(point_1, point_2, color, width):
    pygame.draw.line(screen, color, point_1, point_2, width)
