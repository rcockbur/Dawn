import os, sys, pygame, random
from globals import *
from map import Map
from unit import *
from point import *
from astar import *

print("PROGRAM START")
pygame.display.set_caption('Dawn') 



f = open("map.txt", "r")

row_index = 0
for row in f:
    
    if row_index < TILE_COUNT:
        symbol_index = 0
        for symbol in row.strip(' \t\n\r').split(","):
            if symbol_index < TILE_COUNT:
                if symbol == "s":
                    Block(Point(x = symbol_index, y = row_index))
            symbol_index = symbol_index + 1
    row_index = row_index + 1


ross = Person(Point(x = TILE_COUNT-1, y = TILE_COUNT-1))

for i in range(100):
    Deer(Point(x=20,  y=35))        

for i in range(10):
    Wolf(Point(x=59,  y=45))

# Bear(Point(x=60,  y=60))

frames = 0
seconds = 0
minutes = 0

done = False
print("MAIN LOOP STARTING")
print("-------")

# --------------------------------------------
#                  Main Loop
# --------------------------------------------
while not done:
    if seconds > PROGRAM_DURATION: done = True
        
    for event in pygame.event.get():

        # Get Input
        if event.type == pygame.QUIT: done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                done = True
            elif event.key == pygame.K_KP1:
                w1.move_by(-1, 1)
            elif event.key == pygame.K_KP2:
                w1.move_by(0, 1)
            elif event.key == pygame.K_KP3:
                w1.move_by(1, 1)
            elif event.key == pygame.K_KP4:
                w1.move_by(-1, 0)
            elif event.key == pygame.K_KP5:
                w1.move_by(0, 0)
            elif event.key == pygame.K_KP6:
                w1.move_by(1, 0)
            elif event.key == pygame.K_KP7:
                w1.move_by(-1, -1)
            elif event.key == pygame.K_KP8:
                w1.move_by(0, -1)
            elif event.key == pygame.K_KP9:
                w1.move_by(1, -1)
            elif event.key == pygame.K_p:
                print_debug()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            
            
            #spawn deer
            if GRID_OFFSET_X < pos[0] < GRID_OFFSET_X + GRID_SIZE and GRID_OFFSET_Y < pos[1] < GRID_OFFSET_Y + GRID_SIZE:
                tile_x = int((pos[0] - GRID_OFFSET_X) / TILE_SPACING)
                tile_y = int((pos[1] - GRID_OFFSET_Y) / TILE_SPACING)
                tile = Point(tile_x, tile_y)
                # print("Pathing from", ross.tile.str(),"to", tile.str())
                if type(MAP.get_unit_at(tile)) != Block:
                    path = astar(ross.tile, tile)
                    ross.path = path
                # Deer(Point(x=tile_x,  y=tile_y)) 

    frames = frames + 1

    # update units
    if frames % 2 == 0:
        for unit_id in list(MAP.units):
            if type(MAP.units[unit_id]) is not Block:
                MAP.units[unit_id].update()
                
        # print("---------")  

    # print time
    if frames % FRAMES_PER_SECOND == 0:
        seconds = seconds + 1
        if seconds % SECONDS_PER_MINUTE == 0:
            minutes = minutes + 1
        # print("(", minutes,":",seconds, ")")

    # draw
    screen.fill(COLOR_BLACK) # black
    draw_grid()              # grid
    for unit in MAP.get_units():
        unit.draw()          # units

    font = pygame.font.Font('freesansbold.ttf', 14) 
    num_deer = len(MAP.get_units_of_type(Deer))
    text = font.render(str(num_deer) + ' Deer', True, COLOR_GREEN, COLOR_BLACK) 
    textRect = text.get_rect()  
    textRect.topleft = (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y) 

    screen.blit(text, textRect) 

    # flip
    pygame.display.flip()

    


print("QUIT")