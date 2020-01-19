import os, sys, pygame, random
from globals import *
from map import Map
from unit import *
from point import *
from actions import *
from draw import draw_text_at


print("PROGRAM START")
pygame.display.set_caption('Dawn') 
freesansbold_14 = pygame.font.Font('freesansbold.ttf', 14) 

LEFT = 1
RIGHT = 3




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

# print(ROSS)
ross = Person(Point(x = TILE_COUNT-1, y = TILE_COUNT-1))
a = Person(Point(x = TILE_COUNT-3, y = TILE_COUNT-1))
b = Person(Point(x = TILE_COUNT-5, y = TILE_COUNT-1))
c = Person(Point(x = TILE_COUNT-7, y = TILE_COUNT-1))


for i in range(100):
    Deer(Point(x=20,  y=35))        

for i in range(10):
    Wolf(Point(x=49,  y=45))

# Bear(Point(x=60,  y=60))

frames = 0
seconds = 0
minutes = 0

done = False
print("MAIN LOOP STARTING")

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

                if event.button == LEFT:
                    select_tile(tile)

                if event.button == RIGHT:
                    print("Pathing from", ross.tile.str(),"to", tile.str())
                    path_to(tile)
                    
                
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

    #num_deer
    string = "Deer: " + str(len(MAP.get_units_of_type(Deer)))
    draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y))

    # print(selected_unit[0])
    if selected_unit[0] is not None:
        string = "class:    " + selected_unit[0].class_name()
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 100))        

        string = "name:   " + selected_unit[0].name
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 120))        

        string = "pos:      (" + str(selected_unit[0].tile.x) + "," + str(selected_unit[0].tile.y) + ")"
        draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 140))

        if selected_unit[0].path.size() > 0:
            string = "Target: (" + str(selected_unit[0].path.get(-1).x) + "," + str(selected_unit[0].path.get(-1).y) + ")"
            draw_text_at(freesansbold_14, string, (GRID_SIZE + GRID_OFFSET_X + 5, GRID_OFFSET_Y + 160))            

    # flip
    pygame.display.flip()

    


print("QUIT")