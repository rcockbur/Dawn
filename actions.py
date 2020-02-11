import os, sys, pygame, random
from globals import *
from unit import Unit, Person, Wolf
from block import Block, Grass
from pathfinding import astar
from ability import Move, Eat
print("running actions.py")

def filter_selection(entities):
    removed_entities = set()
    person_selected = False
    unit_selected = False
    grass_selected = False
    wolf_selected = False

    for selected_entity in entities:
        if type(selected_entity) is Person:
            person_selected = True
        if isinstance(selected_entity, Unit):
            unit_selected = True
        if isinstance(selected_entity, Wolf):
            wolf_selected = True
        if isinstance(selected_entity, Grass):
            grass_selected = True
    
    if person_selected:
        for selected_entity in entities:
            if type(selected_entity) is not Person:
                removed_entities.add(selected_entity)

    elif wolf_selected:
        for selected_entity in entities:
            if not isinstance(selected_entity, Wolf):
                removed_entities.add(selected_entity)
        
    elif unit_selected:
        for selected_entity in entities:
            if not isinstance(selected_entity, Unit):
                removed_entities.add(selected_entity)

    elif grass_selected:
        for selected_entity in entities:
            if not isinstance(selected_entity, Grass):
                removed_entities.add(selected_entity)

    entities -= removed_entities

def move_to_tile(tile):
    if len(selected_entities) > 0:
        dest_entity = MAP.get_entity_at_tile(tile)
        for selected_entity in selected_entities:
            if selected_entity.__class__.is_manual:

                if type(dest_entity) in selected_entity.__class__.eat_types:
                    ability = Eat
                elif dest_entity is None:
                    ability = Move
                else:
                    ability = None
                if ability is not None:
                    path = astar(selected_entity.tile, tile, selected_entity.__class__.cant_path_over_types, get_debug_pathfinding())
                    if path is not None:
                        selected_entity.ability_list.clear()
                        new_ability = ability(selected_entity, path, dest_entity)
                        selected_entity.ability_list.append(new_ability)

def select_box(corner_1, corner_3, shift_down):
    if not shift_down: clear_selection()
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

