from globals import *
from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
import time, random
from utility import measure, print_point

print("running pathfinding.py")

rt_2 = sqrt(2)

neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

slow_factor = 1


def heuristic(a, b):
    delta_x = abs(a[0] - b[0])
    delta_y = abs(a[1] - b[1])
    diagonals = min(delta_x, delta_y)
    orthos = abs(delta_x - delta_y)
    return diagonals * 14 + orthos * 10
    


def debug_draw(tup, color, radius, width):
    rect = calculate_rect(tup, radius)
    pygame.draw.rect(screen, color, rect, width)
    pygame.display.flip()

def string_from_point(point):
    return str(point[0]) + "," + str(point[1])

@measure
def astar(start_tile, end_tile, obstacle_types, debug):
    start_time = time.time()
    nodes_checked = 0

    if debug:
        debug_draw(end_tile, COLOR_PATH, 2, 0)   
        debug_draw(start_tile, COLOR_ASTAR_PRIMARY, TILE_RADIUS, 1)

    closed_set = set()
    came_from = {}
    g_score = {start_tile : 0}
    f_score = {start_tile:heuristic(start_tile, end_tile)}
    open_heap = []
    heappush(open_heap, (f_score[start_tile], nodes_checked, start_tile))

    while open_heap:
        current_heap_bundle = heappop(open_heap)
        current_f_score = current_heap_bundle[0]
        time_stamp = current_heap_bundle[1]
        current_node = current_heap_bundle[2]
        closed_set.add(current_node)

        # update neighbors
        for i, j in neighbors:
            neighbor = current_node[0] + i, current_node[1] + j            
            proposed_g_score = g_score[current_node] + heuristic(current_node, neighbor)
            if 0 <= neighbor[0] < TILE_COUNT_X:
                if 0 <= neighbor[1] < TILE_COUNT_Y:
                    # Outro block
                    if neighbor == end_tile:
                        path = Path()
                        path.append(neighbor)
                        if debug: 
                            time.sleep(0.2 * slow_factor)
                        while current_node in came_from:
                            #DEBUG
                            if debug:
                                if current_node is not start_tile:
                                    debug_draw(current_node, COLOR_PATH, 2, 0)
                                    time.sleep(0.02 * slow_factor)
                            path.append(current_node)
                            current_node = came_from[current_node]
                        if debug: 
                            debug_draw(start_tile, COLOR_PATH, TILE_RADIUS, 1)
                            time.sleep(0.2 * slow_factor)
                        return path.reverse()  
                    if type(MAP.get_entity_at_tile(neighbor)) in obstacle_types: continue
                else: continue # out of bounds y         
            else: continue # out of bounds x
            if neighbor in closed_set and proposed_g_score >= g_score.get(neighbor, 0):
                continue
            if  proposed_g_score < g_score.get(neighbor, 0) or neighbor not in [i[2] for i in open_heap]:
                nodes_checked = nodes_checked - 1
                came_from[neighbor] = current_node
                g_score[neighbor] = proposed_g_score
                f_score[neighbor] = proposed_g_score + heuristic(neighbor, end_tile)
                
                if debug and proposed_d_score >= tile_range:
                    debug_draw(neighbor, COLOR_ASTAR_PRIMARY, 1, 0)

                heappush(open_heap, (f_score[neighbor], nodes_checked, neighbor))
        
        if debug:
            if current_node is not start_tile:
                debug_draw(current_node, COLOR_ASTAR_SECONDARY, 1, 0)
                
    print("Path not found")
    for i in obstacle_types:
        print(i)
    return Path()



def create_path(tile, came_from, debug, debug_color):
    if debug: 
        debug_draw(tile, debug_color, 2, 0)
        time.sleep(0.7 * slow_factor)
    path = Path()
    # path.append(tile)

    while tile in came_from:
        path.append(tile)
        tile = came_from[tile]

    path = path.reverse()
    for tile in path.points:
        if debug:
            debug_draw(tile, debug_color, 2, 0)
            time.sleep(0.02 * slow_factor)                  

    return path

def choose_random(set):
    return random.choice(set)


# @measure
def get_path(self, find_closest):
    debug = get_debug_pathfinding() and self.is_selected

    idle_range = self.move_range_idle * 10
    hunt_range = self.move_range_hunt * 10
    mate_range = self.move_range_mate * 10

    start_tile = self.tile

    # 100 to -200
    eat_chance = (100 * (self.satiation_current - self.satiation_full)) // (0 - self.satiation_full) # ranges from 0 to 99 
    wants_to_hunt = self.can_eat() and random.randint(0, 99) <= eat_chance
    wants_to_mate = self.can_mate()

    if wants_to_hunt:
        if self.satiation_current < 0 and day[0] > self.last_scanned_at + 400:
            entity_range = hunt_range * 3
            tile_range = hunt_range
            self.last_scanned_at = day[0]
        else:
            entity_range = hunt_range
            tile_range = hunt_range

    elif wants_to_mate:
        if self.is_wolf and day[0] > self.last_scanned_at + 400:
            entity_range = mate_range * 4
            tile_range = mate_range * 3
            self.last_scanned_at = day[0]
        elif not self.is_wolf and day[0] > self.last_scanned_at + 400:
            entity_range = mate_range * 2
            tile_range = mate_range
            self.last_scanned_at = day[0]
        
        else:
            entity_range = mate_range
            tile_range = mate_range

    else:
        entity_range = idle_range
        tile_range = idle_range

    activity_color = COLOR_YELLOW
    if wants_to_mate: activity_color = COLOR_PINK
    if wants_to_hunt: activity_color = COLOR_RED

    status = MOVING
    if wants_to_mate: status = MATING
    if wants_to_hunt: status = HUNTING

    if debug:
        draw_function[0]()
        debug_draw(start_tile, activity_color, TILE_RADIUS, 1)
        time.sleep(0.2 * slow_factor)

    closed_set = set()
    came_from = {}
    d_score = {start_tile : 0}
    open_heap = []
    edible_entities = set()
    potential_mates = set()
    occupied_tiles = set()
    heappush(open_heap, (d_score[start_tile], start_tile))

    while open_heap:
        current_heap_bundle = heappop(open_heap)
        current_d_score = current_heap_bundle[0]
        current_tile = current_heap_bundle[1]
        current_entity = MAP.get_entity_at_tile(current_tile)
        if current_entity is not None and type(current_entity) not in self.cant_path_to_types:
            occupied_tiles.add(current_tile)
            if wants_to_hunt and type(current_entity) in self.eat_types and current_entity.can_be_hunted():
                edible_entities.add(current_entity)
                break
            elif wants_to_mate and type(current_entity) == type(self) and current_entity.can_be_mated_with(): 
                potential_mates.add(current_entity)
                break

        closed_set.add(current_tile)

        if current_entity == self or type(current_entity) not in self.cant_path_over_types:
            for i, j in neighbors:
                neighbor = current_tile[0] + i, current_tile[1] + j

                if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue

                proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
                if proposed_d_score > entity_range: continue
                if neighbor in closed_set and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score

                neighbor_entity = MAP.get_entity_at_tile(neighbor) 
                if type(neighbor_entity) in self.cant_path_to_types: continue # means we cant generate a path to a block that is unpathable. we could have to put an escape            

                if proposed_d_score < d_score.get(neighbor, 0) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current_tile
                    d_score[neighbor] = proposed_d_score
                    heappush(open_heap, (d_score[neighbor], neighbor))

                if debug:
                    debug_draw(neighbor, activity_color, 1, 0)

        if debug:
            if current_tile is not start_tile:
                debug_draw(current_tile, COLOR_CLOSED_SET, 1, 0)
    
    # return food
    if wants_to_hunt and len(edible_entities) > 0:
        edible_entity = random.choice(tuple(edible_entities))
        path = create_path(edible_entity.tile, came_from, debug, COLOR_PATH_HUNT)
        return (path, status, edible_entity)

    # return mate
    elif wants_to_mate and len(potential_mates) > 0:
        mate = random.choice(tuple(potential_mates))
        path = create_path(mate.tile, came_from, debug, COLOR_PATH_MATE)
        return (path, status, mate)
    
    # return random tile
    closed_set -= occupied_tiles
    closed_set = set(filter(lambda tile : d_score[tile] <= tile_range, closed_set)) 
    if len(closed_set) > 0:
        chosen_tile = random.choice(tuple(closed_set))
        path = create_path(chosen_tile, came_from, debug, activity_color)
        return (path, status, None)
    else:
        return (Path(), STOPPED, None)