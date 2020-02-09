import os, sys, pygame, random
from globals import *                               #imports point
from map import Map, tile_from_pos, clamp_pos, pos_within_bounds
from block import Block, Grass
from unit import Unit, Deer, Wolf, Person  
from actions import move_to_tile, select_box, clear_selection, stop
from draw import draw_everything, draw_hud, draw_grid, draw_box, draw_unit, draw_path, draw_black, draw_unit_highlight, draw_block
print("running main.py")

pygame.display.set_caption('Dawn') 
clock = pygame.time.Clock()
map_file = open("map.txt", "r")


# create blocks
print("reading map.txt")
# row_index = 0
# for row in map_file:    
#     if row_index < TILE_COUNT_Y:
#         symbol_index = 0
#         for symbol in row.strip(' \t\n\r').split(","):
#             if symbol_index < TILE_COUNT_X:
#                 if symbol == "s":
#                     Block((symbol_index, row_index))
#                 elif symbol == "g":
#                     Grass((symbol_index, row_index))
#             symbol_index = symbol_index + 1
#     row_index = row_index + 1

# create units randomly
for x in range(TILE_COUNT_X//2):
    for y in range(TILE_COUNT_Y//2):
        if MAP.get_entity_at_tile((2*x,2*y)) == None:
            rand = random.randint(0,250)
            if rand <= 50:
                Grass((2*x, 2*y))
                
            # elif rand <= 70:
            #     Deer((2*x, 2*y), False)
            # elif rand <= 71:
            #     Wolf((2*x, 2*y), False)

done = False
paused = False
mouse_pos_start = None

speed_up_factor = 1
speed_up_factor_index = 0

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
            if event.key == pygame.K_p:
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
            elif event.key == pygame.K_k:
                print('kill')
                for entity in selected_entities:
                    entity.die()
            elif event.key == pygame.K_EQUALS:
                speed_up_factor = speed_up_factor * 2
                speed_up_factor_index = 0
                print('FASTER', str(speed_up_factor))
            elif event.key == pygame.K_MINUS:
                if speed_up_factor > 1:
                    speed_up_factor = speed_up_factor // 2
                    speed_up_factor_index = 0
                    print('SLOWER', str(speed_up_factor))
                    
            elif event.key == pygame.K_1:
                toggle_debug_pathfinding()
                print("Debug Pathfinding:", str(get_debug_pathfinding()))
            elif event.key == pygame.K_2:
                toggle_debug_path()
                print("Debug Path:", str(get_debug_path()))
            elif event.key == pygame.K_3:
                toggle_debug_performance()
                print("Debug Perf:", str(get_debug_performance()))
            elif event.key == pygame.K_4:
                toggle_debug_status()
                print("Debug Status:", str(get_debug_status()))

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
        
        # units
        for entity_id in list(MAP.entities):
            if isinstance(MAP.entities[entity_id], Unit) or isinstance(MAP.entities[entity_id], Grass):
                MAP.entities[entity_id].update()
        # dead units
        for unit in dead_units:
            MAP.remove_entity(unit)
        dead_units.clear()

        tick[0] += 1
        tick_of_day[0] += 1
        tick_of_month[0] += 1
        tick_of_year[0] += 1
        if tick_of_day[0] == TICKS_PER_DAY:
            tick_of_day[0] = 0
            day[0] += 1
            day_of_month[0] += 1
            day_of_year[0] += 1
            if day_of_month[0] == DAYS_PER_MONTH:
                tick_of_month[0] = 0
                day_of_month[0] = 0
                month[0] += 1
                month_of_year[0] += 1
                if month_of_year[0] == MONTHS_PER_YEAR:
                    tick_of_year[0] = 0
                    day_of_year[0] = 0
                    month_of_year[0] = 0
                    year[0] += 1

    mid_time = pygame.time.get_ticks()    
    logic_time = mid_time - start_time

    speed_up_factor_index += 1
    if speed_up_factor_index == speed_up_factor:
        speed_up_factor_index = 0
        # draw
        draw_everything(mouse_pos_start, mouse_pos_clamped)
        pygame.display.flip()

    end_time = pygame.time.get_ticks()
    graphics_time = end_time - mid_time
    total_time = end_time - start_time
    if get_debug_performance() and paused == False: 
        print("Logic:",logic_time, "    Graphics:", graphics_time, "    Total:", total_time, "    Available:", 1000//FPS) 
    clock.tick(FPS * speed_up_factor)

    
print("------------------------ FIN ---------------------------")

