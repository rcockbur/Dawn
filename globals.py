import pygame
import random
import os
# from point import Point, Vector  

# Any file which imports globals, also imports Point and Vector, as well as Map (below)

print("running globals.py 1")
# os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (250,50)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)

random.seed()
pygame.init()

NoneType = type(None)

WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 865

WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080

debug_search_tile = False #or True
debug_search_food = False #or True
debug_pathfinding = False #or True
debug_path = False


screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

# statuses
IDLE = 0
MOVING = 1


COLOR_RED = (255, 0, 0)
COLOR_RED_DARK = (127, 0, 0)

COLOR_GREEN = (0, 255, 0)
COLOR_GREEN_DARK = (0, 127, 0)

COLOR_BLUE = (0, 0, 255)
COLOR_BLUE_DARK = (0, 0, 127)

COLOR_YELLOW = (255, 255, 0)
COLOR_YELLOW_DARK = (127, 127, 0)

COLOR_PURPLE = (255, 0, 255)
COLOR_PINK = (255, 0, 255)
COLOR_TEAL = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY_LIGHT = (191, 191, 191)
COLOR_GREY = (122, 122, 122) 
COLOR_GREY_DARK = (64, 64, 64)
COLOR_GREY_VDARK = (32, 32, 32) # grid
COLOR_BROWN = (100, 40, 0)
COLOR_BROWN_LIGHT = (140, 65, 0)

COLOR_GRID = COLOR_GREY_VDARK
COLOR_BLOCK = COLOR_GREY_DARK
COLOR_TEXT_GREEN = COLOR_GREEN
COLOR_SELECTION_HIGHLIGHT = COLOR_YELLOW
COLOR_SELECTION_BOX = COLOR_WHITE
COLOR_BACKGROUND = COLOR_BLACK

COLOR_DEER = (100, 40, 0)               # brown
COLOR_DEER_HUNGERY = (160, 70, 0)       # red-ish brown
COLOR_WOLF = (170, 170, 170)            # grey
COLOR_WOLF_HUNGERY = (255, 225, 225)    # light red
COLOR_PERSON = (0, 0, 100)            # blue
COLOR_PERSON_HUNGERY = (0, 0, 255)   # purple

COLOR_PATH = COLOR_BLUE
COLOR_ASTAR_PRIMARY = COLOR_GREEN
COLOR_ASTAR_SECONDARY = COLOR_GREEN_DARK
COLOR_FIND_TILE_PRIMARY = COLOR_YELLOW
COLOR_FIND_TILE_SECONDARY = COLOR_YELLOW_DARK
COLOR_FIND_ENTITY_PRIMARY = COLOR_RED
COLOR_FIND_ENTITY_SECONDARY = COLOR_RED_DARK


GRID_OFFSET_X = 10
GRID_OFFSET_Y = 25
TILE_COUNT = 75

LINE_WIDTH = 1
TILE_RADIUS = 5
TILE_SPACING = TILE_RADIUS * 2 + LINE_WIDTH
GRID_SIZE = TILE_COUNT * TILE_SPACING


UNIT_RADIUS_DEER = TILE_RADIUS
UNIT_RADIUS_WOLF = TILE_RADIUS
UNIT_RADIUS_PERSON = TILE_RADIUS
UNIT_RADIUS_BLOCK = TILE_RADIUS

SECONDS_PER_MINUTE = 60
FRAMES_PER_SECOND = 100

LEFT_BUTTON = 1
RIGHT_BUTTON = 3





frames = [0]
sim_ticks = [0]

selected_entities = set()
dead_units = set()

from map import Map

print("running globals.py 2")

MAP = Map()



