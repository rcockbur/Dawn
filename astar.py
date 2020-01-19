from globals import *
from point import *
from map import *
from path import *
from unit import *
from heapq import *
import time

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


def astar(start_tile, end_tile):
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
            path = Path([])
            while current in came_from:
                path.append(tile_from_tup(current))
                current = came_from[current]
            print("Path found")
            print("Elapsed Time: ", time.time() - start_time)
            return path.reverse()

        close_set.add(current)
        #DEBUG
        if debug:
            rect = Unit.calculate_rect(tile_from_tup(current), 1)
            pygame.draw.rect(screen, COLOR_BLUE, rect)
            pygame.display.flip()

        # update neighbors
        for i, j in neighbors:
            neighbor = current[0] + i, current[1] + j            
            tentative_g_score = gscore[current] + heuristic(current, neighbor)
            if 0 <= neighbor[0] < TILE_COUNT:
                if 0 <= neighbor[1] < TILE_COUNT:
                    if type(MAP.get_unit_at(tile_from_tup(neighbor))) == Block:
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
                    rect = Unit.calculate_rect(tile_from_tup(neighbor), 1)
                    pygame.draw.rect(screen, COLOR_RED, rect)
                    pygame.display.flip()
                
    print("Path not found")
    print("Elapsed Time: ", time.time() - start_time)
    return Path([])
