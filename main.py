import os, sys, pygame, random
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from block import Block, Grass
from pathfinding import get_path
from unit import Unit, Deer, Wolf, Person  
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

for i in range(1):
    for j in range(1):
        Wolf((65 + 2*i, 5 + 2*j))        
# if True:
#     for x in range(8):
#         for y in range(2):
            # Deer((45 + 2*x, 9 + 2*y))
# for x in range(1):
#     for y in range(1):
#         Deer((35 + 2*x, 44 + 2*y))


done = False
paused = False
mouse_pos_start = None


while not done:
    
    start_time = pygame.time.get_ticks() 
    
    
    mouse_pos = pygame.mouse.get_pos()
    mouse_pos_clamped = clamp_pos(mouse_pos)
    mouse_tile = tile_from_pos(mouse_pos)
    mouse_tile_clamped = tile_from_pos(mouse_pos_clamped)
    if mouse_tile is not None:
        mouse_entity = MAP.get_entity_at_tile(mouse_tile)
    else:
        mouse_entity = None
    mouse_entity_clamped = MAP.get_entity_at_tile(mouse_tile_clamped)

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
            elif event.key == pygame.K_w:
                if mouse_tile is not None and mouse_entity is None:
                    Wolf(mouse_tile)
            elif event.key == pygame.K_d:
                if mouse_tile is not None and mouse_entity is None:
                    Deer(mouse_tile)
            elif event.key == pygame.K_k:
                if mouse_entity is not None:
                    print('kill')
                    mouse_entity.die()
            elif event.key == pygame.K_1:
                toggle_debug_pathfinding()
                print("debug_pathfinding:", str(get_debug_pathfinding()))
            elif event.key == pygame.K_2:
                toggle_debug_path()
                print("debug_path:", str(get_debug_path()))
            elif event.key == pygame.K_3:
                toggle_debug_performance()
                print("debug_performance:", str(get_debug_performance()))

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
        
        # units
        for entity_id in list(MAP.entities):
            if isinstance(MAP.entities[entity_id], Unit) or isinstance(MAP.entities[entity_id], Grass):
                MAP.entities[entity_id].update()
        # dead units
        for unit in dead_units:
            MAP.remove_entity(unit)
        dead_units.clear()
        sim_ticks[0] += 1
    mid_time = pygame.time.get_ticks()    
    logic_time = mid_time - start_time
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
        if isinstance(entity, Unit):
            draw_path(entity)
    draw_hud()
    if mouse_pos_start is not None:
        draw_box(mouse_pos_start, mouse_pos_clamped)

    pygame.display.flip()
    frames[0] = frames[0] + 1
    end_time = pygame.time.get_ticks()
    graphics_time = end_time - mid_time
    total_time = end_time - start_time
    if get_debug_performance() and paused == False: 
        print("Logic:",logic_time, "    Graphics:", graphics_time, "    Total:", total_time, "    Available:", 1000//FPS) 
    clock.tick(FPS)

    
print("------------------------ FIN ---------------------------")

