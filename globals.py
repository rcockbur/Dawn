import pygame
import random
from point import Point, Vector  

# Any file which imports globals, also imports Point and Vector, as well as Map (below)

print("running globals.py 1")


NoneType = type(None)

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800

COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_PINK = (255, 0, 255)
COLOR_TEAL = (0, 255, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GREY_LIGHT = (191, 191, 191)
COLOR_GREY = (122, 122, 122) 
COLOR_GREY_DARK = (84, 84, 84)
COLOR_GREY_VDARK = (32, 32, 32) # grid
COLOR_BROWN = (100, 40, 0)
COLOR_BROWN_LIGHT = (140, 65, 0)
GRID_COLOR = COLOR_GREY_VDARK

GRID_OFFSET_X = 12
GRID_OFFSET_Y = 15
TILE_COUNT = 50

LINE_WIDTH = 1
TILE_RADIUS = 6
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

NORTH = 0
NORTH_EAST = 1
EAST = 2
SOUTH_EAST = 3
SOUTH = 4
SOUTH_WEST = 5
WEST = 6
NORTH_WEST = 7


DIRECTIONS = [NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST]
DIRECTION_VECTORS = [Vector(0,-1), Vector(1,-1), Vector(1,0), Vector(1,1), Vector(0,1), Vector(-1,1), Vector(-1,0), Vector(-1,-1)]
DIRECTION_NAMES = ["NORTH", "NORTH_EAST", "EAST", "SOUTH_EAST", "SOUTH", "SOUTH_WEST", "WEST", "NORTH_WEST"]

screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

frames = [0]
seconds = [0]
minutes = [0]

selected_units = set()

from map import Map

print("running globals.py 2")

MAP = Map()
random.seed()
pygame.init()


