print("----------------------- START --------------------------")

import os, sys, pygame, random
# from point import Point
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from block import Block, Grass
from unit import Unit, Deer, Wolf, Person  
from actions import move_to_tile, select_box, clear_selection, stop
from draw import draw_hud, draw_grid, draw_box, draw_unit, draw_path, draw_black, draw_unit_highlight, draw_block

print("running main.py")



pygame.display.set_caption('Dawn') 

map_file = open("map.txt", "r")

# Create blocks from map.txt
row_index = 0
for row in map_file:    
    if row_index < TILE_COUNT_Y:
        symbol_index = 0
        for symbol in row.strip(' \t\n\r').split(","):
            if symbol_index < TILE_COUNT_X:
                if symbol == "s":
                    Block((symbol_index, row_index))
                elif symbol == "g":
                    Grass((symbol_index, row_index))
            symbol_index = symbol_index + 1
    row_index = row_index + 1

# Create units
# d = Person((69, 66))
# a = Person((70, 66))
# b = Person((71, 66))
# c = Person((72, 66))


# for i in range(1):
#     for j in range(1):
#         Wolf((65 + i, 5 + j))        
for x in range(4):
    for y in range(4):
        Deer((35 + x, 44 + y))


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
            if isinstance(MAP.entities[entity_id], Unit) or isinstance(MAP.entities[entity_id], Grass):
                MAP.entities[entity_id].update()

        for unit in dead_units:
            MAP.remove_entity(unit)
        sim_ticks[0] += 1

    # draw background
    draw_black()
    draw_grid()              

    # draw units
    for entity in MAP.get_entities():
        if isinstance(entity, Unit):
            draw_unit(entity)
        else:
            draw_block(entity)
    for entity in MAP.get_entities():
        if entity.is_selected == True:
            draw_unit_highlight(entity)
    for entity in MAP.get_entities():
        if hasattr(entity, 'path'):
            draw_path(entity)

    # draw UI panels
    draw_hud()

    if mouse_pos_start is not None:
        draw_box(mouse_pos_start, mouse_pos_clamped)

    # flip
    pygame.display.flip()

    frames[0] = frames[0] + 1

print("------------------------ FIN ---------------------------")

