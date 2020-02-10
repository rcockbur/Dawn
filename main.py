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
# print("reading map.txt")
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
            if rand <= 80:
                Grass((2*x, 2*y))
                
            elif rand <= 88:
                Deer((2*x, 2*y), False)
            # elif rand <= 71:
            #     Wolf((2*x, 2*y), False)

done = False
paused = False
mouse_pos_start = None

speed_up_factor = 1
speed_up_factor_index = 0
slow_down_factor = 1
slow_down_factor_index = 0

def unit_report():

    s = ""
    i = 0
    for unit_class in (Deer, Wolf):
        i += 1
        if i == 2: 
            s = s + "    "
        num_born = unit_class.monthly_born
        num_died = unit_class.monthly_died_age + unit_class.monthly_died_starved + unit_class.monthly_died_hunted
        diff = num_born - num_died
        if diff >= 0:
            diff_sign = "+"
        else:
            diff_sign = "-"
        diff = abs(diff)
        s = s + unit_class.__name__ 
        count = len(MAP.get_entities_of_type(unit_class))
        if count < 100:
            s = s + " "
            if count < 10:
                s = s + " "
        s = s + "  " + str(count) + " "

        # s = s + " ("
        if diff < 100: s = s + " "
        if diff < 10: s = s + " "
        s = s + diff_sign + str(diff) + ":"
        if num_born < 10: s = s + " "
        s = s + "  +" + str(num_born) 
        
        if num_died < 10: s = s + " "
        s = s + "  -" + str(num_died)
        
        s = s + " "
        if unit_class.monthly_died_age < 10: s = s + " "
        s = s + str(unit_class.monthly_died_age) + "/"
        if unit_class.monthly_died_starved < 10: s = s + " "
        s = s + str(unit_class.monthly_died_starved) + "/"
        if unit_class.monthly_died_hunted < 10: s = s + " "
        s = s + str(unit_class.monthly_died_hunted)
        unit_class.monthly_born = 0
        unit_class.monthly_died_age = 0
        unit_class.monthly_died_hunted = 0
        unit_class.monthly_died_starved = 0
    print(s)

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
                if slow_down_factor > 1:
                    slow_down_factor = slow_down_factor // 2
                    slow_down_factor_index = 0
                    print('Faster', str(1 / slow_down_factor))
                else:
                    speed_up_factor = speed_up_factor * 2
                    speed_up_factor_index = 0
                    print('FASTER', str(speed_up_factor))
            elif event.key == pygame.K_MINUS:
                if speed_up_factor > 1:
                    speed_up_factor = speed_up_factor // 2
                    speed_up_factor_index = 0
                    print('SLOWER', str(speed_up_factor))
                else:
                    slow_down_factor = slow_down_factor * 2
                    slow_down_factor_index = 0
                    print('SLOWER', str(1 / slow_down_factor))
                    
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
        
        slow_down_factor_index += 1
        if slow_down_factor_index == slow_down_factor:
            slow_down_factor_index = 0
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
                    unit_report()
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
    effective_FPS = FPS * speed_up_factor
    if get_debug_performance() and paused == False: 
        print("Logic:",logic_time, "    Graphics:", graphics_time, "    Total:", total_time, "    Available:", 1000//effective_FPS) 
    clock.tick(effective_FPS)

    
print("------------------------ FIN ---------------------------")

