from globals import *
from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
import time
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
                
                if debug and proposed_d_score >= min_range:
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
    path.append(tile)

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

# RANDOM_TILE - including a min and max range, select and return a random tile
# FIRST_ENTITY_MATCHING- go until range, or until found, return an entity or none
# ALL_ENTITIES_MATCHING-  return a tuple containing each entity

# @measure
def get_path(start_tile, min_range, max_range, obstacle_types, validate_entity, choose_entity, debug, debug_color):
    min_range = min_range * 10
    max_range = max_range * 10
    find_entity = validate_entity is not None

    if debug:
        debug_draw(start_tile, COLOR_YELLOW, TILE_RADIUS, 1)
        time.sleep(0.2 * slow_factor)
    closed_set = set()
    came_from = {}
    d_score = {start_tile : 0}
    open_heap = []
    matching_entities = set()
    tiles_checked = 0
    heappush(open_heap, (d_score[start_tile], tiles_checked, start_tile))

    while open_heap:
        current_heap_bundle = heappop(open_heap)
        current_d_score = current_heap_bundle[0]
        # time_stamp = current_heap_bundle[1]
        current_tile = current_heap_bundle[2]
        current_entity = MAP.get_entity_at_tile(current_tile)
        if find_entity:
            if validate_entity(current_entity): 
                # print("valid entity found")
                matching_entities.add(current_entity)

        closed_set.add(current_tile)

        for i, j in neighbors:
            neighbor = current_tile[0] + i, current_tile[1] + j

            if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue

            proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
            if proposed_d_score > max_range: continue
            if neighbor in closed_set and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score

            neighbor_entity = MAP.get_entity_at_tile(neighbor) 
            if type(neighbor_entity) in obstacle_types: continue # means we cant generate a path to a block that is unpathable. we could have to put an escape            

            if proposed_d_score < d_score.get(neighbor, 0) or neighbor not in [i[2] for i in open_heap]:
                # tiles_checked = tiles_checked - 1
                came_from[neighbor] = current_tile
                d_score[neighbor] = proposed_d_score
                heappush(open_heap, (d_score[neighbor], tiles_checked, neighbor))


                if debug and proposed_d_score > min_range:
                    debug_draw(neighbor, COLOR_OPEN_HEAP, 1, 0)

        if debug:
            if current_tile is not start_tile and current_d_score > min_range:
                debug_draw(current_tile, COLOR_CLOSED_SET, 1, 0)
    
    if find_entity == True:
        if len(matching_entities) > 0:
            matching_entity = choose_entity(tuple(matching_entities))
            path = create_path(matching_entity.tile, came_from, debug, debug_color)
            return path
        
    
    closed_set = set(filter(lambda tile : d_score[tile] > min_range, closed_set))
    if len(closed_set) > 0:
        chosen_tile = random.choice(tuple(closed_set))
        path = create_path(chosen_tile, came_from, debug, COLOR_PATH_IDLE)
        return path
    else:
        return Path()

