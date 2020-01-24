import os, sys, pygame, random
from globals import *
from unit import Person
from block import Block
from pathfinding import astar


print("running actions.py")

def move_to_tile(tile):
    print("move_to_tile")
    if len(selected_units) > 0:
        dest_unit = MAP.get_entity_at(tile)
        for selected_unit in selected_units:
            # if type(dest_unit) not in selected_unit.block_pathing_types:
            if selected_unit.is_manual and type(dest_unit) not in [Block]:
                path = astar(selected_unit.tile, tile, selected_unit.block_pathing_types)
                selected_unit.path = path

def select_tile(tile):
    clear_selection()

    unit = MAP.get_entity_at(tile)
    if unit is not None:
        unit.select()
        selected_units.add(unit)
        print("Selected:", unit.name)

def select_box(corner_1, corner_3):
    clear_selection()

    units = MAP.get_entities_in_box(corner_1, corner_3)
    print(len(units), "in", corner_1.x, corner_1.y, "    ", corner_3.x, corner_3.y)
    for unit in units:
        if type(unit) is Person:
            unit.select()
            selected_units.add(unit)
            print("Selected:", unit.name)

def clear_selection():
    if len(selected_units) > 0:
        for unit in selected_units:
            unit.deselect()
        selected_units.clear()

def stop():
    for selected_unit in selected_units:
        selected_unit.path.clear()

