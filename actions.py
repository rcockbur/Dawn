# import os, sys, pygame, random
from globals import *

from map import Map
import pathfinding
from unit import *

print("running actions.py")

def path_to(tile):
    if type(selected_unit[0]) is Person:
        unit = MAP.get_unit_at(tile)
        if type(unit) not in selected_unit[0].block_target_types:
            path = pathfinding.astar(selected_unit[0].tile, tile, selected_unit[0].block_pathing_types)
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