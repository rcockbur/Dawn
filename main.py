print("----------------------- START --------------------------")

import os, sys, pygame, random
from point import Point
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from block import Block
from unit import Unit, Deer, Wolf, Person  
from actions import move_to_tile, select_box, clear_selection, stop
from draw import draw_hud, draw_grid, draw_box, draw_unit, draw_path, draw_black

print("running main.py")

pygame.display.set_caption('Dawn') 

map_file = open("map.txt", "r")

# Create blocks from map.txt
row_index = 0
for row in map_file:    
    if row_index < TILE_COUNT:
        symbol_index = 0
        for symbol in row.strip(' \t\n\r').split(","):
            if symbol_index < TILE_COUNT:
                if symbol == "s":
                    Block(Point(x = symbol_index, y = row_index))
            symbol_index = symbol_index + 1
    row_index = row_index + 1

# Create units
a = Person(Point(x = TILE_COUNT-1, y = TILE_COUNT-1))
b = Person(Point(x = TILE_COUNT-3, y = TILE_COUNT-1))
c = Person(Point(x = TILE_COUNT-5, y = TILE_COUNT-1))
d = Person(Point(x = TILE_COUNT-7, y = TILE_COUNT-1))
e = Person(Point(x = TILE_COUNT-9, y = TILE_COUNT-1))
for i in range(10):
    Deer(Point(x=2,  y=25))        
for i in range(10):
    Wolf(Point(x=49,  y=45))


done = False
paused = False

mouse_pos_start = None

while not done:
    # print("mainloop") 
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_clamped = clamp_pos(mouse_pos)
    mouse_tile = tile_from_pos(mouse_pos)
    mouse_tile_clamped = tile_from_pos(mouse_pos_clamped)

    for event in pygame.event.get():

        # Check exit conditions
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            done = True

        # Check keyboard events
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused       
            elif event.key == pygame.K_ESCAPE:
                clear_selection()
            elif event.key == pygame.K_s:
                stop()

        # Mouse down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_BUTTON and mouse_tile != None and mouse_pos_start == None:
                mouse_pos_start = mouse_pos
                mouse_tile_start = mouse_tile
        # Mouse up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT_BUTTON:
                if mouse_pos_start is not None:
                    select_box(mouse_tile_start, mouse_tile_clamped)
                    mouse_pos_start = None
            if event.button == RIGHT_BUTTON:
                if mouse_tile is not None:
                    move_to_tile(mouse_tile)

    if paused == False:

        dead_units.clear()

        # update units
        for entity_id in list(MAP.entities):
            if isinstance(MAP.entities[entity_id], Unit):
                MAP.entities[entity_id].update()
        for entity_id in list(MAP.entities):
            if isinstance(MAP.entities[entity_id], Unit):
                MAP.entities[entity_id].update_2()

        for unit in dead_units:
            MAP.remove_entity(unit)

        # draw background
        draw_black()
        draw_grid()              

        # draw units
        for entity in MAP.get_entities():
            draw_unit(entity)
        for entity in MAP.get_entities():
            draw_path(entity)

        # draw UI panels
        draw_hud()

        if mouse_pos_start is not None:
            draw_box(mouse_pos_start, mouse_pos_clamped)

        # flip
        pygame.display.flip()

        frames[0] = frames[0] + 1

print("------------------------ FIN ---------------------------")

