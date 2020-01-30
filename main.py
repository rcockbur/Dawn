import os, sys, pygame, random
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from block import Block, Grass
from unit import Unit, Deer, Wolf, Person  
# from pathfinding import find_nearby_tile
from actions import move_to_tile, select_box, clear_selection, stop
from draw import draw_hud, draw_grid, draw_box, draw_unit, draw_path, draw_black, draw_unit_highlight, draw_block
print("running main.py")

pygame.display.set_caption('Dawn') 
clock = pygame.time.Clock()
map_file = open("map.txt", "r")

print("reading map.txt")
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

for i in range(2):
    for j in range(1):
        Wolf((65 + 2*i, 5 + 2*j))        
for x in range(4):
    for y in range(4):
        # tile = find_nearby_tile
        Deer((35 + 2*x, 44 + 2*y))

done = False
paused = False
mouse_pos_start = None
time_stamp = pygame.time.get_ticks() 

while not done:
    
    if debug_performance: print("Performance:",str(pygame.time.get_ticks() - time_stamp), "/", 1000//FPS, "ms used" ) 
    
    time_stamp = pygame.time.get_ticks()    
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_clamped = clamp_pos(mouse_pos)
    mouse_tile = tile_from_pos(mouse_pos)
    mouse_tile_clamped = tile_from_pos(mouse_pos_clamped)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            done = True
        # Keyboard
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
        # units
        for entity_id in list(MAP.entities):
            if isinstance(MAP.entities[entity_id], Unit) or isinstance(MAP.entities[entity_id], Grass):
                MAP.entities[entity_id].update()
        # dead units
        for unit in dead_units:
            MAP.remove_entity(unit)
        sim_ticks[0] += 1
    
    # draw
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
        if hasattr(entity, 'path'):
            draw_path(entity)
    draw_hud()
    if mouse_pos_start is not None:
        draw_box(mouse_pos_start, mouse_pos_clamped)

    pygame.display.flip()
    frames[0] = frames[0] + 1
    clock.tick(FPS)
    
print("------------------------ FIN ---------------------------")

