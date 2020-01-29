from globals import *
from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
import time

print("running pathfinding.py")

rt_2 = sqrt(2)

neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

slow_factor = 1


def heuristic(a, b):
    delta_x = abs(a[0] - b[0])
    delta_y = abs(a[1] - b[1])
    diagonals = min(delta_x, delta_y)
    orthos = abs(delta_x - delta_y)
    r = diagonals * 14 + orthos * 10
    return r


def debug_draw(tup, color, radius, width):
    rect = calculate_rect(tup, radius)
    pygame.draw.rect(screen, color, rect, width)
    pygame.display.flip()

def string_from_point(point):
    return str(point[0]) + "," + str(point[1])

# @measure
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
                
                if debug:
                    debug_draw(neighbor, COLOR_ASTAR_PRIMARY, 1, 0)

                heappush(open_heap, (f_score[neighbor], nodes_checked, neighbor))
        
        if debug:
            if current_node is not start_tile:
                debug_draw(current_node, COLOR_ASTAR_SECONDARY, 1, 0)
                
    print("Path not found")
    for i in obstacle_types:
        print(i)
    return Path()

# RANDOM_TILE_IN_RANGE - go until range, select random at end
# TILE_AT_RANGE        - go until range, select in last round - need to remember previous rounds set
# FIRST_ENTITY_MATCHING- go until found or range
# ALL_ENTITIES_MATCHING

def find_nearby_tile(start_tile, obstacle_types, range, debug):
    open_set = set()
    closed_set = set()
    open_set.add(start_tile)
    iteration_count = 0

    if debug:
        debug_draw(start_tile, COLOR_FIND_TILE_PRIMARY, TILE_RADIUS, 1)

    while(len(open_set) > 0) and iteration_count < range:
        working_set = open_set.copy()
        open_set.clear()
        for tup in working_set:
            closed_set.add(tup)

            if debug:
                if tup is not start_tile and iteration_count < range - 1:
                    debug_draw(tup, COLOR_FIND_TILE_SECONDARY, 1, 0)

            if iteration_count < range - 1:
                for i, j in neighbors:
                    neighbor = (tup[0] + i, tup[1] + j)
                    if 0 <= neighbor[0] < TILE_COUNT_X:
                        if 0 <= neighbor[1] < TILE_COUNT_Y:
                            neighbor_entity = MAP.get_entity_at_tile(neighbor)
                            if type(neighbor_entity) in obstacle_types: continue
                        else: continue
                    else: continue
                    if neighbor in closed_set or neighbor in open_set: continue
                    open_set.add(neighbor)

                    if debug:
                        debug_draw(neighbor, COLOR_FIND_TILE_PRIMARY, 1, 0)

        iteration_count += 1

    # Outro block
    closed_set.remove(start_tile)
    if len(closed_set) > 0:
        chosen_tup = random.choice(tuple(closed_set))

        if debug:
            debug_draw(chosen_tup, COLOR_PATH, 2, 0)
            time.sleep(0.2 * slow_factor)

        return chosen_tup
    else:
        return None


def find_nearby_entity(start_tile, obstacle_types, range, validate, debug):
    open_set = set()
    closed_set = set()
    open_set.add(start_tile)
    iteration_count = 0

    if debug:
        debug_draw(start_tile, COLOR_FIND_ENTITY_PRIMARY, TILE_RADIUS, 1)

    while(len(open_set) > 0) and iteration_count < range:
        working_set = open_set.copy()
        open_set.clear()
        for tup in working_set:
            closed_set.add(tup)
            
            if debug:
                if tup is not start_tile:
                    debug_draw(tup, COLOR_FIND_ENTITY_SECONDARY, 1, 0)

            if iteration_count < range - 1:
                for i, j in neighbors:
                    neighbor = (tup[0] + i, tup[1] + j)
                    if 0 <= neighbor[0] < TILE_COUNT_X:
                        if 0 <= neighbor[1] < TILE_COUNT_Y: pass
                        else: continue
                    else: continue
                        
                    neighbor_entity = MAP.get_entity_at_tile(neighbor)
                    if validate(neighbor_entity):
                        if debug:
                            debug_draw(neighbor, COLOR_PATH, 2, 0)
                            time.sleep(0.2 * slow_factor)
                        return neighbor

                    if type(neighbor_entity) in obstacle_types: continue
                    if neighbor in closed_set or neighbor in open_set: continue
                    open_set.add(neighbor)

                    if debug:
                        debug_draw(neighbor, COLOR_FIND_ENTITY_PRIMARY, 1, 0)
        iteration_count += 1

    return None
        