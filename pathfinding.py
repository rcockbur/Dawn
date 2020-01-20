from globals import *
from point import *
from map import *
from path import *
from heapq import *
import time

print("running pathfinding.py")

rt_2 = sqrt(2)
debug = False
# debug = True
neighbors = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]

def heuristic(a, b):
    return sqrt((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2)

def tup_from_tile(tile):
    return (tile.x, tile.y)

def tile_from_tup(tup):
    return Point(x = tup[0], y = tup[1])

# @measure
def astar(start_tile, end_tile, obstacle_types):
    start_time = time.time()

    start = tup_from_tile(start_tile)
    goal = tup_from_tile(end_tile)

    close_set = set()
    came_from = {}
    gscore = {start:0}
    fscore = {start:heuristic(start, goal)}
    oheap = []
    heappush(oheap, (fscore[start], start))

    while oheap:
        current = heappop(oheap)[1]

        # goal found
        if current == goal:
            path = Path()
            while current in came_from:
                path.append(tile_from_tup(current))
                current = came_from[current]
            # print("Path found")
            # print("Elapsed Time: ", time.time() - start_time)
            return path.reverse()

        close_set.add(current)
        #DEBUG
        if debug:
            rect = Map.calculate_rect(tile_from_tup(current), 1)
            pygame.draw.rect(screen, COLOR_BLUE, rect)
            pygame.display.flip()

        # update neighbors
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < TILE_COUNT:
                if 0 <= neighbor[1] < TILE_COUNT:
                    if type(MAP.get_unit_at(tile_from_tup(neighbor))) in obstacle_types:
                        continue
                else:
                    continue    # array bound y walls
            else:
                continue        # array bound x walls
                
            if neighbor in close_set and tentative_g_score >= gscore.get(neighbor, 0):
                continue
                
            if  tentative_g_score < gscore.get(neighbor, 0) or neighbor not in [i[1]for i in oheap]:
                came_from[neighbor] = current
                gscore[neighbor] = tentative_g_score
                fscore[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heappush(oheap, (fscore[neighbor], neighbor))

                #DEBUG
                if debug:
                    rect = Map.calculate_rect(tile_from_tup(neighbor), 1)
                    pygame.draw.rect(screen, COLOR_RED, rect)
                    pygame.display.flip()
                
    print("Path not found")
    for i in obstacle_types:
        print(i)
    return Path()


def find_nearby_tile(tile, obstacle_types):
    open_set = set()
    closed_set = set()
    search_distance = 10
    open_set.add(tup_from_tile(tile))
    iteration_count = 0
    while(len(open_set) > 0) and iteration_count < search_distance:
        
        working_set = open_set.copy()
        open_set.clear()
        for tup in working_set:
            closed_set.add(tup)

            # DEBUG
            if debug:
                rect = Map.calculate_rect(tile_from_tup(tup), 1)
                pygame.draw.rect(screen, COLOR_BLUE, rect)
                pygame.display.flip()

            if iteration_count < search_distance - 1:
                for i, j in neighbors:
                    neighbor = (tup[0] + i, tup[1] + j)
                    if 0 <= neighbor[0] < TILE_COUNT:
                        if 0 <= neighbor[1] < TILE_COUNT:
                            if type(MAP.get_unit_at(tile_from_tup(neighbor))) in obstacle_types:
                                continue
                        else:
                            continue
                    else:
                        continue
                    if neighbor in closed_set or neighbor in open_set:
                        continue
                    open_set.add(neighbor)

                    # DEBUG
                    if debug:
                        rect = Map.calculate_rect(tile_from_tup(neighbor), 1)
                        pygame.draw.rect(screen, COLOR_RED, rect)
                        pygame.display.flip()
        iteration_count += 1

    closed_set.remove(tup_from_tile(tile))
    if len(closed_set) > 0:
        chosen_tup = random.choice(tuple(closed_set))
        return tile_from_tup(chosen_tup)
    else:
        return None