from globals import *
# from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
from utility import measure, weighted_random
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
                            time.sleep(0.2)
                        while current_node in came_from:
                            #DEBUG
                            if debug:
                                if current_node is not start_tile:
                                    debug_draw(current_node, COLOR_GREEN, 2, 0)
                                    time.sleep(0.02)
                            path.append(current_node)
                            current_node = came_from[current_node]
                        if debug: 
                            debug_draw(start_tile, COLOR_GREEN, TILE_RADIUS, 1)
                            time.sleep(0.2)
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

# @measure
def create_path(tile, came_from, debug, debug_color):
    if debug: 
        debug_draw(tile, debug_color, 2, 0)
        time.sleep(0.7)
    path = list()
    while tile in came_from:
        path.append(tile)
        tile = came_from[tile]
    path.reverse()
    for tile in path:
        if debug:
            debug_draw(tile, debug_color, 2, 0)
            time.sleep(0.02)                  
    return path

# @measure
def get_path(self, find_closest, wants_to_hunt, wants_to_mate, wants_to_socialize, prefer_food, outer_range, inner_range):
    debug = get_debug_pathfinding() and self.is_selected

    if wants_to_hunt and (wants_to_mate or wants_to_socialize):
        raise RuntimeError("wants_to_hunt is true at the same time as mate or social") 

    start_tile = self.tile
    outer_range = 100
    middle_range = 50
    inner_range = 40
    activity_color = COLOR_WHITE

    
    edibles = list()
    prefered_edibles = list()
    mates = list()        
    friends = list()
    can_mate = self.can_mate()
    my_type = type(self)
    can_eat = self.sat_current < self.sat_full
    
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
        time.sleep(0.2)


    while open_heap:
        current_heap_bundle = heappop(open_heap)
        current_d_score = current_heap_bundle[0]
        current_tile = current_heap_bundle[1]
        current_entity = MAP.get_entity_at_tile(current_tile)
        current_entity_type = type(current_entity)
        if current_entity is not None and current_entity_type not in self.__class__.cant_path_to_types and current_tile is not start_tile:
            occupied_tiles.add(current_tile)
            if current_entity_type in self.__class__.avoid_types:
                enemies.append(current_entity)
                if debug:
                    outter_rect = calculate_rect(current_entity.tile, TILE_RADIUS)    
                    pygame.draw.rect(screen, COLOR_ENEMY, outter_rect, 1)
            if can_eat and self.can_eat_entity(current_entity) and current_entity.can_be_hunted():
                if prefer_food(current_entity):
                    edibles.append(current_entity)
                    if debug:
                        outter_rect = calculate_rect(current_entity.tile, TILE_RADIUS)    
                        pygame.draw.rect(screen, COLOR_PATH_HUNT, outter_rect, 1)
                elif current_d_score <= middle_range:
                    prefered_edibles.append(current_entity)
                    if debug:
                        outter_rect = calculate_rect(current_entity.tile, TILE_RADIUS)    
                        pygame.draw.rect(screen, COLOR_PATH_HUNT, outter_rect, 1)
            else:
                if can_mate and current_entity_type == my_type and current_entity.can_be_mated_with() and current_d_score <= middle_range: 
                    mates.append(current_entity)
                    if debug:
                        outter_rect = calculate_rect(current_entity.tile, TILE_RADIUS)    
                        pygame.draw.rect(screen, COLOR_PATH_MATE, outter_rect, 1)
                if current_entity_type == my_type and current_d_score <= middle_range:
                    friends.append(current_entity)
                    if debug:
                        outter_rect = calculate_rect(current_entity.tile, TILE_RADIUS)    
                        pygame.draw.rect(screen, COLOR_PATH_SOCIAL, outter_rect, 1)
            

        # closed_set.add(current_tile)
        closed_set_quality[current_tile] = 10

        if current_entity == self or type(current_entity) not in self.__class__.cant_path_over_types:
            for i, j in neighbors:
                neighbor = current_tile[0] + i, current_tile[1] + j

                if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue

                proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
                if proposed_d_score > outer_range: continue
                if neighbor in closed_set_quality and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score

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
                pygame.event.pump()

    if len(enemies) > 0: 
        in_danger = True
        modify_quality(closed_set_quality, enemies, debug)

    if debug: print("back from modify")
    closed_set_quality.pop(start_tile)

    # return edible - closest. prefered have priority
    if wants_to_hunt: 
        prefered_edibles = [edible for edible in prefered_edibles if closed_set_quality[edible.tile] > 0]
        edibles = [edible for edible in edibles if closed_set_quality[edible.tile] > 0]
        if (len(edibles) > 0 or len(prefered_edibles) > 0):
            # prefered_edibles = [edible for edible in edibles if prefer_food(edible)]
            if len(prefered_edibles) > 0: chosen_list = prefered_edibles
            else: chosen_list = edibles
            return calc_path_info(self, came_from, closed_set_quality, chosen_list, COLOR_PATH_HUNT, HUNTING) + [in_danger]

    # return mate - random
    if wants_to_mate: 
        mates = [mate for mate in mates if closed_set_quality[mate.tile] > 0]
        if len(mates) > 0:
            return calc_path_info(self, came_from, closed_set_quality, mates, COLOR_PATH_MATE, MATING) + [in_danger]

    # return friend - random
    if wants_to_socialize: 
        friends = [friend for friend in friends if closed_set_quality[friend.tile] > 0]
        if len(friends) > 0:
            return calc_path_info(self, came_from, closed_set_quality, friends, COLOR_PATH_SOCIAL, SOCIAL) + [in_danger]
    
    # return random tile
    [closed_set_quality.pop(key) for key in occupied_tiles]
    bad_keys = { key for key in closed_set_quality.keys() if d_score[key] > inner_range or closed_set_quality[key] == 0 }
    [closed_set_quality.pop(key) for key in bad_keys]
    if len(closed_set_quality) > 0:
        # chosen_tile = random.choice(closed_set_quality.keys())
        chosen_tile = weighted_random(closed_set_quality)
        if self.is_selected: print("chose", str(chosen_tile), "with quality", closed_set_quality[chosen_tile])
        # print(str(chosen_tile))
        if chosen_tile is not None:
            path = create_path(chosen_tile, came_from, debug, activity_color)
            return (path, MOVING, None, in_danger)
        else:
            return (None, STOPPED, None, in_danger)    
    else:
        return (None, STOPPED, None, in_danger)

def calc_path_info(unit, came_from, closed_set_quality, entities, color, status):
    debug = get_debug_pathfinding() and unit.is_selected
    filtered_quality = { tile: closed_set_quality[tile] for tile in [e.tile for e in entities] }  
    chosen_tile = weighted_random(filtered_quality)
    if unit.is_selected: print("chose", str(chosen_tile), "with quality", closed_set_quality[chosen_tile])
    chosen_entity = MAP.get_entity_at_tile(chosen_tile)
    path = create_path(chosen_tile, came_from, debug, color)
    if len(path) > 0: path.pop(-1)
    if len(path) == 0: path = None
    return [path, status, chosen_entity]

# @measure
def modify_quality(closed_set_quality, enemies, debug):
    outer_range = 60
    closed_set = set()
    open_heap = []
    d_score = dict()
    for enemy in enemies:
        d_score[enemy.tile] = 0
        heappush(open_heap, (0, enemy.tile))

    while open_heap:
        if debug: print(str(len(open_heap)))
        current_heap_bundle = heappop(open_heap)
        current_d_score = current_heap_bundle[0]
        current_tile = current_heap_bundle[1]
        current_entity = MAP.get_entity_at_tile(current_tile)
        closed_set.add(current_tile)
        if current_tile in closed_set_quality:
            if debug:
                debug_draw(current_tile, COLOR_RED, 1, 0)
                pygame.event.pump()
                time.sleep(0.02)
            closeness = min(((outer_range - current_d_score) + 45) // 10, 10)
            closed_set_quality[current_tile] = max(closed_set_quality[current_tile] - closeness , 0)
        if type(current_entity) not in static_entity_types:
            for i, j in neighbors:
                neighbor = current_tile[0] + i, current_tile[1] + j
                if not (0 <= neighbor[0] < TILE_COUNT_X and 0 <= neighbor[1] < TILE_COUNT_Y): continue
                proposed_d_score = d_score[current_tile] + heuristic(current_tile, neighbor)
                if proposed_d_score >= outer_range: continue
                if neighbor in closed_set and d_score[neighbor] <= proposed_d_score: continue # skip if we already checked it and dont have a better score
                neighbor_entity = MAP.get_entity_at_tile(neighbor) 
                # if type(neighbor_entity) in static_entity_types: continue # means we cant generate a path to a block that is unpathable. we could have to put an escape            
                if proposed_d_score < d_score.get(neighbor, 0) or neighbor not in [i[1] for i in open_heap]:
                    d_score[neighbor] = proposed_d_score
                    heappush(open_heap, (d_score[neighbor], neighbor))