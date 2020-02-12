from globals import *
# from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
from utility import measure
import time, random
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

# @measure
def astar(start_tile, end_tile, obstacle_types, debug):
    start_time = time.time()
    nodes_checked = 0

    if debug:
        debug_draw(start_tile, COLOR_YELLOW, TILE_RADIUS, 1)

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
                        path = list()
                        path.append(neighbor)
                        if debug: 
                            time.sleep(0.2 * slow_factor)
                        while current_node in came_from:
                            #DEBUG
                            if debug:
                                if current_node is not start_tile:
                                    debug_draw(current_node, COLOR_GREEN, 2, 0)
                                    time.sleep(0.02 * slow_factor)
                            path.append(current_node)
                            current_node = came_from[current_node]
                        if debug: 
                            debug_draw(start_tile, COLOR_GREEN, TILE_RADIUS, 1)
                            time.sleep(0.2 * slow_factor)
                        path.reverse()
                        return path
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
                    debug_draw(neighbor, COLOR_BLUE, 1, 0)

                heappush(open_heap, (f_score[neighbor], nodes_checked, neighbor))
        
        if debug:
            if current_node is not start_tile:
                debug_draw(current_node, COLOR_RED, 1, 0)
                
    print("Path not found")
    return None

def create_path(tile, came_from, debug, debug_color):
    if debug: 
        debug_draw(tile, debug_color, 2, 0)
        time.sleep(0.7 * slow_factor)
    path = list()
    while tile in came_from:
        path.append(tile)
        tile = came_from[tile]
    path.reverse()
    for tile in path:
        if debug:
            debug_draw(tile, debug_color, 2, 0)
            time.sleep(0.02 * slow_factor)                  
    return path

# @measure
def get_path(self, find_closest, wants_to_hunt, wants_to_mate, wants_to_socialize, prefer_food, search_range, idle_range):
    debug = get_debug_pathfinding() and self.is_selected

    if wants_to_hunt and (wants_to_mate or wants_to_socialize):
        raise RuntimeError("wants_to_hunt is true at the same time as mate or social") 

    start_tile = self.tile
    search_range = search_range * 10
    idle_range = idle_range * 10
    activity_color = COLOR_PATH_MOVING

    if wants_to_hunt: 
        activity_color = COLOR_PATH_HUNT
        edibles = list()
    else:
        if wants_to_mate: 
            activity_color = COLOR_PATH_MATE
            mates = list()
        
        if wants_to_socialize: 
            activity_color = COLOR_PATH_SOCIAL
            friends = list()
    

    closed_set = set()
    closed_set_quality = {}
    came_from = {}
    d_score = {start_tile : 0}
    open_heap = []
    enemies = list()
    occupied_tiles = set()
    in_danger = False
    heappush(open_heap, (d_score[start_tile], start_tile))

    if debug:
        draw_function[0]()
        debug_draw(start_tile, activity_color, TILE_RADIUS, 1)
        time.sleep(0.2 * slow_factor)

    while open_heap:
        current_heap_bundle = heappop(open_heap)
        current_d_score = current_heap_bundle[0]
        current_tile = current_heap_bundle[1]
        current_entity = MAP.get_entity_at_tile(current_tile)
        if current_entity is not None and type(current_entity) not in self.__class__.cant_path_to_types:
            occupied_tiles.add(current_tile)
            if wants_to_hunt and self.can_eat(current_entity) and current_entity.can_be_hunted() and current_entity is not self:
                edibles.append(current_entity)
            else:
                if wants_to_mate and type(current_entity) == type(self) and current_entity.can_be_mated_with(): 
                    mates.append(current_entity)
                if wants_to_socialize and type(current_entity) == type(self) and current_entity is not self:
                    friends.append(current_entity)
            if type(current_entity) in self.__class__.avoid_types:
                enemies.append(current_entity)

        closed_set.add(current_tile)
        closed_set_quality[current_tile] = 1

        if current_entity == self or type(current_entity) not in self.__class__.cant_path_over_types:
            for i, j in neighbors:
                neighbor = current_tile[0] + i, current_tile[1] + j

                if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue

                proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
                if proposed_d_score > search_range: continue
                if neighbor in closed_set and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score

                neighbor_entity = MAP.get_entity_at_tile(neighbor) 
                if type(neighbor_entity) in self.__class__.cant_path_to_types: continue # means we cant generate a path to a block that is unpathable. we could have to put an escape            

                if proposed_d_score < d_score.get(neighbor, 0) or neighbor not in [i[1] for i in open_heap]:
                    came_from[neighbor] = current_tile
                    d_score[neighbor] = proposed_d_score
                    heappush(open_heap, (d_score[neighbor], neighbor))

                if debug:
                    debug_draw(neighbor, activity_color, 1, 0)

        if debug:
            if current_tile is not start_tile:
                debug_draw(current_tile, COLOR_CLOSED_SET, 1, 0)

    if len(enemies) > 0: 
        in_danger = True
        modify_quality(closed_set_quality, enemies, debug)


    # return edible
    if wants_to_hunt: edibles = [edible for edible in edibles if closed_set_quality[edible.tile] > 0]
    if wants_to_hunt and len(edibles) > 0:
        prefered_edibles = [edible for edible in edibles if prefer_food(edible)]
        if len(prefered_edibles) > 0: chosen_list = prefered_edibles
        else: chosen_list = edibles
        chosen_list.sort(key=lambda e: d_score[e.tile])
        edible_entity = chosen_list[0]    
        path = create_path(edible_entity.tile, came_from, debug, COLOR_PATH_HUNT)
        if len(path) > 0: path.pop(-1)
        if len(path) == 0: path = None
        return (path, HUNTING, edible_entity, in_danger)

    # return mate
    if wants_to_mate: mates = [mate for mate in mates if closed_set_quality[mate.tile] > 0]
    if wants_to_mate and len(mates) > 0:
        mate = random.choice(mates)
        path = create_path(mate.tile, came_from, debug, COLOR_PATH_MATE)
        if len(path) > 0: path.pop(-1)
        if len(path) == 0: path = None
        return (path, MATING, mate, in_danger)

    # return friend
    if wants_to_socialize: friends = [friend for friend in friends if closed_set_quality[friend.tile] > 0]
    if wants_to_socialize and len(friends) > 0:
        friend = random.choice(friends)
        path = create_path(friend.tile, came_from, debug, COLOR_PATH_SOCIAL)
        if len(path) > 0: path.pop(-1)
        if len(path) == 0: path = None
        return (path, SOCIAL, friend, in_danger)
    
    # return random tile
    closed_set -= {start_tile}
    closed_set -= occupied_tiles
    # closed_set -= dangerous_tiles
    closed_set = [tile for tile in closed_set if d_score[tile] <= idle_range and closed_set_quality[tile] > 0]
    if len(closed_set) > 0:
        chosen_tile = random.choice(closed_set)
        path = create_path(chosen_tile, came_from, debug, activity_color)
        return (path, MOVING, None, in_danger)
    else:
        return (None, STOPPED, None, in_danger)

def modify_quality(closed_set_quality, enemies, debug):
    search_range = 80
    for enemy in enemies:
        closed_set = set()
        d_score = {enemy.tile : 0}
        open_heap = []
        heappush(open_heap, (d_score[enemy.tile], enemy.tile))
        while open_heap:
            current_heap_bundle = heappop(open_heap)
            current_d_score = current_heap_bundle[0]
            current_tile = current_heap_bundle[1]
            current_entity = MAP.get_entity_at_tile(current_tile)
            closed_set.add(current_tile)
            if current_tile in closed_set_quality:
                if debug:
                    debug_draw(current_tile, COLOR_RED, 1, 0)
                    time.sleep(0.1 * slow_factor)
                closed_set_quality[current_tile] = 0
            if type(current_entity) not in static_entity_types:
                for i, j in neighbors:
                    neighbor = current_tile[0] + i, current_tile[1] + j
                    if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue
                    proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
                    if proposed_d_score > search_range: continue
                    if neighbor in closed_set and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score
                    neighbor_entity = MAP.get_entity_at_tile(neighbor) 
                    # if type(neighbor_entity) in static_entity_types: continue # means we cant generate a path to a block that is unpathable. we could have to put an escape            
                    if proposed_d_score < d_score.get(neighbor, 0) or neighbor not in [i[1] for i in open_heap]:
                        d_score[neighbor] = proposed_d_score
                        heappush(open_heap, (d_score[neighbor], neighbor))