import os, sys, pygame, random
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from unit import Unit, Deer, Wolf, Person  
from block import Block, Grass
from actions import move_to_tile, select_box, clear_selection, stop, load_map_file
from draw import draw_everything, draw_hud, draw_grid, draw_box, draw_unit, draw_path, draw_black, draw_unit_highlight, draw_block
from utility import unit_report
print("running main.py")

# load_map_file("map.txt")

# create units randomly
for x in range(TILE_COUNT_X//2):
    for y in range(TILE_COUNT_Y//2):
        if MAP.get_entity_at_tile((2*x,2*y)) == None:
            rand = random.randint(0,250)
            if rand <= 40:
                Grass((2*x, 2*y))
            elif rand <= 50:
                Deer((2*x, 2*y), False)
            # elif rand <= 96:
            #     Wolf((2*x, 2*y), False)

done = False
paused = False
mouse_pos_start = None
speed_up_factor_index = 0
slow_down_factor_index = 0

while not done:
    start_time = pygame.time.get_ticks() 
    keys=pygame.key.get_pressed()
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
            if event.key == pygame.K_SPACE:
                paused = not paused       
            elif event.key == pygame.K_ESCAPE:
                clear_selection()
            elif event.key == pygame.K_s:
                stop()
            elif event.key == pygame.K_w:
                if mouse_tile is not None and mouse_entity is None:
                    Wolf(mouse_tile, False)
            elif event.key == pygame.K_d:
                if mouse_tile is not None and mouse_entity is None:
                    Deer(mouse_tile, False)
            elif event.key == pygame.K_h:
                if mouse_tile is not None and mouse_entity is None:
                    Person(mouse_tile, False)
            elif event.key == pygame.K_g:
                if mouse_tile is not None and mouse_entity is None:
                    Grass(mouse_tile)
            elif event.key == pygame.K_b:
                if mouse_tile is not None and mouse_entity is None:
                    Block(mouse_tile)
            elif event.key == pygame.K_DELETE:
                print('Delete')
                for entity in selected_entities:
                    entity.destroy()
            elif event.key == pygame.K_EQUALS:
                if slow_down_factor[0] > 1:
                    slow_down_factor[0] = slow_down_factor[0] // 2
                    slow_down_factor_index = 0
                else:
                    speed_up_factor[0] = speed_up_factor[0] * 2
                    speed_up_factor_index = 0
            elif event.key == pygame.K_MINUS:
                if speed_up_factor[0] > 1:
                    speed_up_factor[0] = speed_up_factor[0] // 2
                    speed_up_factor_index = 0
                else:
                    slow_down_factor[0] = slow_down_factor[0] * 2
                    slow_down_factor_index = 0
            elif event.key == pygame.K_1:
                toggle_debug_pathfinding()
                print("Show Pathfinding:", str(get_debug_pathfinding()))
            elif event.key == pygame.K_2:
                toggle_debug_path()
                print("Show Paths:", str(get_debug_path()))
            elif event.key == pygame.K_3:
                toggle_debug_performance()
                print("Show Performance:", str(get_debug_performance()))
            elif event.key == pygame.K_4:
                toggle_debug_status()
                print("Show Unit Overlay:", str(get_debug_status()))
            elif event.key == pygame.K_5:
                toggle_debug_unit_report()
                print("Monthly Unit Report:", str(get_debug_unit_report()))
        # Mouse down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == LEFT_BUTTON and mouse_tile != None and mouse_pos_start == None:
                mouse_pos_start = mouse_pos
                mouse_tile_start = mouse_tile
        # Mouse up
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == LEFT_BUTTON:
                if mouse_pos_start is not None:
                    select_box(mouse_tile_start, mouse_tile_clamped, keys[pygame.K_LSHIFT])
                    mouse_pos_start = None
            if event.button == RIGHT_BUTTON:
                if mouse_tile is not None:
                    move_to_tile(mouse_tile)
    if paused == False:        
        slow_down_factor_index += 1
        if slow_down_factor_index == slow_down_factor[0]:
            slow_down_factor_index = 0
            # units
            for entity_id in list(MAP.entities):
                if isinstance(MAP.entities[entity_id], Unit) or isinstance(MAP.entities[entity_id], Grass):
                    MAP.entities[entity_id].update()
            # dead units
            for unit in destroyed_units:
                MAP.remove_entity(unit)
            destroyed_units.clear()

            current_date[DT_HOUR] += 1
            current_date[DT_HOUR_OD] += 1
            current_date[DT_HOUR_OM] += 1
            current_date[DT_HOUR_OY] += 1
            if current_date[DT_HOUR_OD] == HOURS_PER_DAY:
                current_date[DT_HOUR_OD] = 0
                current_date[DT_DAY] += 1
                current_date[DT_DAY_OM] += 1
                current_date[DT_DAY_OY] += 1
                if current_date[DT_DAY_OM] == DAYS_PER_MONTH:
                    current_date[DT_HOUR_OM] = 0
                    current_date[DT_DAY_OM] = 0
                    current_date[DT_MONTH] += 1
                    current_date[DT_MONTH_OY] += 1
                    if get_debug_unit_report(): unit_report((Deer, Wolf))
                    if current_date[DT_MONTH_OY] == MONTHS_PER_YEAR:
                        current_date[DT_HOUR_OY] = 0
                        current_date[DT_DAY_OY] = 0
                        current_date[DT_MONTH_OY] = 0
                        current_date[DT_YEAR] += 1

    mid_time = pygame.time.get_ticks()    
    logic_time = mid_time - start_time
    speed_up_factor_index += 1
    if speed_up_factor_index == speed_up_factor[0]:
        speed_up_factor_index = 0
        draw_everything(mouse_pos_start, mouse_pos_clamped)
        pygame.display.flip()

    end_time = pygame.time.get_ticks()
    graphics_time = end_time - mid_time
    total_time = end_time - start_time
    effective_FPS = FPS * speed_up_factor[0]
    if get_debug_performance() and paused == False: 
        print("Logic:",logic_time, "    Graphics:", graphics_time, "    Total:", total_time, "    Available:", 1000//effective_FPS) 
    clock.tick(effective_FPS)
print("------------------------ FIN ---------------------------")

