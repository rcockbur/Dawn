import os, sys, pygame, random
from globals import *
from unit import Unit, Person
from block import Block
from pathfinding import astar


print("running actions.py")

def filter_selection(entities):
    person_selected = False
    for selected_entity in entities:
        if type(selected_entity) is Person:
            person_selected = True

    non_person_unit_selected = False
    for selected_entity in entities:
        if isinstance(selected_entity, Unit) and not isinstance(selected_entity, Person):
            non_person_unit_selected = True

    removed_entities = set()
    if person_selected:
        for selected_entity in entities:
            if type(selected_entity) is not Person:
                removed_entities.add(selected_entity)
        
    elif non_person_unit_selected:
        for selected_entity in entities:
            if not isinstance(selected_entity, Unit):
                removed_entities.add(selected_entity)

    entities -= removed_entities


def move_to_tile(tile):
    # print("move_to_tile")
    if len(selected_units) > 0:
        dest_unit = MAP.get_entity_at(tile)
        for selected_unit in selected_units:
            # if type(dest_unit) not in selected_unit.block_pathing_types:
            if selected_unit.is_manual and type(dest_unit) not in [Block]:
                path = astar(selected_unit.tile, tile, selected_unit.block_pathing_types, False)
                selected_unit.path = path


def select_box(corner_1, corner_3):
    clear_selection()
    entities = MAP.get_entities_in_box(corner_1, corner_3)
    filter_selection(entities)
    # print(len(entities), "in", corner_1.x, corner_1.y, "    ", corner_3.x, corner_3.y)
    for unit in entities:
        unit.select()
        selected_units.add(unit)
        # print("Selected:", unit.name)

def clear_selection():
    if len(selected_units) > 0:
        for unit in selected_units:
            unit.deselect()
        selected_units.clear()

def stop():
    for selected_unit in selected_units:
        selected_unit.path.clear()

