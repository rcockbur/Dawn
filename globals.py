import pygame
import random
import os
import ctypes

print("running globals.py 1")

NoneType = type(None)
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (0,0)
user32 = ctypes.windll.user32

WINDOW_WIDTH = user32.GetSystemMetrics(0)
WINDOW_HEIGHT = user32.GetSystemMetrics(1)

g = dict()

random.seed()
pygame.init()

screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

draw_function = [0]

FPS = 30
frames = [0]
sim_tick = [0]
TICKS_PER_YEAR = 1000

selected_entities = set()
dead_units = set()

debug_pathfinding = False #or True
debug_path = False        #or True
debug_performance = False #or True
debug_status = False       or True

GRID_OFFSET_X = 10
GRID_OFFSET_Y = 25
TILE_COUNT_X = 140
TILE_COUNT_Y = 116
LINE_WIDTH = 1
TILE_RADIUS = 4
LEFT_BUTTON = 1
MIDDLE_BUTTON = 2
RIGHT_BUTTON = 3

STOPPED = 0
MOVING = 1
HUNTING = 2
MATING = 3


TILE_SPACING = TILE_RADIUS * 2 + LINE_WIDTH
GRID_SIZE_X = TILE_COUNT_X * TILE_SPACING
GRID_SIZE_Y = TILE_COUNT_Y * TILE_SPACING
UNIT_RADIUS_BLOCK = UNIT_RADIUS_DEER = UNIT_RADIUS_WOLF = UNIT_RADIUS_PERSON = TILE_RADIUS

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
COLOR_SELECTION_HIGHLIGHT = (150, 190, 0)
COLOR_SELECTION_BOX = COLOR_WHITE
COLOR_BACKGROUND = COLOR_BLACK
COLOR_DEER = (100, 40, 0)               # brown
COLOR_DEER_HUNGERY = (160, 70, 0)       # red-ish brown
COLOR_WOLF = (170, 170, 170)            # grey
COLOR_WOLF_HUNGERY = (255, 225, 225)    # light red
COLOR_PERSON = (0, 0, 100)              # dull blue
COLOR_PERSON_HUNGERY = (0, 0, 255)      # bright blue
COLOR_OPEN_HEAP = COLOR_RED
COLOR_CLOSED_SET = COLOR_BLUE
COLOR_PATH_MOVING = COLOR_YELLOW
COLOR_PATH_HUNT = COLOR_RED
COLOR_PATH_MATE = COLOR_PINK
COLOR_PATH_SELECTED = COLOR_YELLOW

PATH_COLORS = { MOVING : COLOR_PATH_MOVING, MATING : COLOR_PATH_MATE, HUNTING : COLOR_PATH_HUNT }

def toggle_debug_pathfinding():
    global debug_pathfinding
    debug_pathfinding = not debug_pathfinding

def get_debug_pathfinding():
    global debug_pathfinding
    return debug_pathfinding

def toggle_debug_path():
    global debug_path
    debug_path = not debug_path

def get_debug_path():
    global debug_path
    return debug_path

def toggle_debug_performance():
    global debug_performance
    debug_performance = not debug_performance

def get_debug_performance():
    global debug_performance
    return debug_performance

def toggle_debug_status():
    global debug_status
    debug_status = not debug_status

def get_debug_status():
    global debug_status
    return debug_status

from map import Map # Any file which imports globals also imports both Map and MAP from map.py
print("running globals.py 2")
MAP = Map()

