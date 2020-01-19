import pygame
from globals import *
from unit import *

freesansbold_14 = pygame.font.Font('freesansbold.ttf', 14) 

def draw_text_at(font, string, pos):
    text = font.render(string, True, COLOR_GREEN, COLOR_BLACK) 
    textRect = text.get_rect() 
    textRect.topleft = pos
    screen.blit(text, textRect)

def draw_hud():
        #num_deer
    string = "Deer: " + str(len(MAP.get_units_of_type(Deer)))
    draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y))

    if selected_unit[0] is not None:
        string = "class:    " + selected_unit[0].class_name()
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 100))        

        string = "name:   " + selected_unit[0].name
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 120))        

        string = "pos:      (" + str(selected_unit[0].tile.x) + "," + str(selected_unit[0].tile.y) + ")"
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 140))

        if selected_unit[0].path.size() > 0:
            string = "target:  (" + str(selected_unit[0].path.get(-1).x) + "," + str(selected_unit[0].path.get(-1).y) + ")"
            draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 160))   