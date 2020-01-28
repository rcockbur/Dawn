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
    will_draw = debug_pathfinding
    if len(selected_entities) > 0:
        dest_unit = MAP.get_entity_at_tile(tile)
        for selected_entity in selected_entities:
            # if type(dest_unit) not in selected_entity.block_pathing_types:
            if selected_entity.is_manual and type(dest_unit) not in [Block]:
                path = astar(selected_entity.tile, tile, selected_entity.block_pathing_types, will_draw)
                will_draw = False
                selected_entity.path = path


def select_box(corner_1, corner_3):
    clear_selection()
    entities = MAP.get_entities_in_box(corner_1, corner_3)
    filter_selection(entities)
    for unit in entities:
        unit.select()
        selected_entities.add(unit)
        # print("Selected:", unit.name)

def clear_selection():
    if len(selected_entities) > 0:
        for unit in selected_entities:
            unit.deselect()
        selected_entities.clear()

def stop():
    for selected_entity in selected_entities:
        selected_entity.path.clear()

