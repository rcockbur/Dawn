from globals import *
from path import Path
from math import sqrt
from heapq import heappush, heappop
from map import calculate_rect
import time

print("running pathfinding.py")

rt_2 = sqrt(2)
debug_astar = True
debug_flood = True

# debug_astar = True
neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

# def heuristic(a, b):
#     return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def heuristic(a, b):
    delta_x = abs(a[0] - b[0])
    delta_y = abs(a[1] - b[1])
    diagonals = min(delta_x, delta_y)
    orthos = abs(delta_x - delta_y)
    r = diagonals * 14 + orthos * 10
    # print(r)
    return r

def tup_from_tile(tile):
    return (tile.x, tile.y)

def tile_from_tup(tup):
    return Point(x = tup[0], y = tup[1])

def debug_draw(tup, color, radius):
    rect = calculate_rect(tile_from_tup(tup), radius)
    pygame.draw.rect(screen, color, rect)
    pygame.display.flip()

# @measure
def astar(start_tile, end_tile, obstacle_types):
    start_time = time.time()

    start = tup_from_tile(start_tile)
    goal = tup_from_tile(end_tile)

    nodes_checked = 0

    if debug_astar:
        debug_draw(goal, COLOR_BLUE, 2)   

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []
    heappush(oheap, (fscore[start], nodes_checked, start))


    while oheap:
        

        current_heap_bundle = heappop(oheap)
        current_fscore = current_heap_bundle[0]
        time_stamp = current_heap_bundle[1]
        current_node = current_heap_bundle[2]


        # goal found
        if current_node == goal:
            path = Path()
            while current_node in came_from:
                path.append(tile_from_tup(current_node))
                current_node = came_from[current_node]
            # print("Path found")
            # print("Elapsed Time: ", time.time() - start_time)
            return path.reverse()

        close_set.add(current_node)
        # print("current_node ", str(current_fscore), "   ", time_stamp)
        #DEBUG
        if debug_astar:
            if current_node is not start:
                debug_draw(current_node, COLOR_GREEN, 1)

        # update neighbors
        for i, j in neighbors:
            neighbor = current_node[0] + i, current_node[1] + j            
            tentative_g_score = gscore[current_node] + heuristic(current_node, neighbor)
            if 0 <= neighbor[0] < TILE_COUNT:
                if 0 <= neighbor[1] < TILE_COUNT:
                    if type(MAP.get_entity_at(tile_from_tup(neighbor))) in obstacle_types:
                        continue
                else:
                    continue    # array bound y walls
            else:
                continue        # array bound x walls
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[2] for i in oheap]:
                nodes_checked = nodes_checked - 1
                came_from[neighbor] = current_node
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                
                heappush(oheap, (fscore[neighbor], nodes_checked, neighbor))


                #DEBUG
                if debug_astar:
                    debug_draw(neighbor, COLOR_YELLOW, 1)
                    time.sleep(0.02)

                

        if debug_astar:
            if current_node is not start:
                debug_draw(current_node, COLOR_PURPLE, 1)
                
    print("Path not found")
    for i in obstacle_types:
        print(i)
    return Path()


def find_nearby_tile(start_tile, obstacle_types, range):
    open_set = set()
    closed_set = set()
    start_pos = tup_from_tile(start_tile)
    open_set.add(start_pos)
    iteration_count = 0
    while(len(open_set) > 0) and iteration_count < range:
        
        working_set = open_set.copy()
        open_set.clear()
        for tup in working_set:
            closed_set.add(tup)

            # DEBUG
            if debug_flood:
                if tup is not start_pos:
                    debug_draw(tup, COLOR_RED, 1)

            if iteration_count < range - 1:
                for i, j in neighbors:
                    neighbor = (tup[0] + i, tup[1] + j)
                    if 0 <= neighbor[0] < TILE_COUNT:
                        if 0 <= neighbor[1] < TILE_COUNT:
                            if type(MAP.get_entity_at(tile_from_tup(neighbor))) in obstacle_types:
                                continue
                        else:
                            continue
                    else:
                        continue
                    if neighbor in closed_set or neighbor in open_set:
                        continue
                    open_set.add(neighbor)

                    # DEBUG
                    if debug_flood:
                        debug_draw(neighbor, COLOR_YELLOW, 1)
                        # time.sleep(0.01)
        iteration_count += 1

    closed_set.remove(start_pos)
    if len(closed_set) > 0:
        chosen_tup = random.choice(tuple(closed_set))
        return tile_from_tup(chosen_tup)
    else:
        return None