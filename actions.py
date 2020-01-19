# import os, sys, pygame, random
from globals import *

from map import Map
from astar import *
from unit import *

selected_unit = [None]

def path_to(tile):
    if type(selected_unit[0]) is Person and type(MAP.get_unit_at(tile)) != Block:
        path = astar(selected_unit[0].tile, tile)
        selected_unit[0].path = path

def select_tile(tile):
    global selected_unit
    if selected_unit[0] is not None:
        selected_unit[0].deselect()
        selected_unit[0] = None

    unit = MAP.get_unit_at(tile)
    if unit is not None:
        
        unit.select()
        selected_unit[0] = unit
        print("Selected:", unit.name)