from globals import *
from point import *
from map import *
from path import *
from unit import *
import time

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, tile=None):
        self.parent = parent
        self.tile = tile

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.tile.x == other.tile.x and self.tile.y == other.tile.y


def astar(start_tile, end_tile):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start_tile)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end_tile)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:
        # time.sleep(0.2)
        # print(len(open_list), " ", len(closed_list))

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # DEBUG
        rect = Unit.calculate_rect(current_node.tile, 2)
        pygame.draw.rect(screen, COLOR_BLUE, rect)
        pygame.display.flip()

        # Found the goal
        if current_node == end_node:
            path = Path([])
            current = current_node
            while current is not None:
                path.append(current.tile.copy())
                current = current.parent
            return path.reverse() # Return reversed path

        # Generate children
        children = []
        for vector in DIRECTION_VECTORS: # Adjacent squares

            # Get node position
            node_tile = current_node.tile + vector

            # Ensure within bounds
            if MAP.tile_within_bounds(node_tile) == False:
                continue

            # Ensure walkable
            unit = MAP.get_unit_at(node_tile)
            if unit is not None:
                continue

            if Node(current_node, node_tile) in closed_list:
                continue

            # Create new node
            new_node = Node(current_node, node_tile)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            skip = False
            for closed_child in closed_list:
                if child == closed_child:
                    skip = True
            if skip:
                continue

                        # Child is already in the open list

            my_node = None
            for open_node in open_list:
                if open_node == child:
                    my_node = open_node
                    break

            if my_node is None:
                child.g = current_node.g + 1
                child.h = abs(child.tile.x - end_node.tile.x) + abs(child.tile.y - end_node.tile.y)
                child.f = child.g + child.h
                child.parent = current_node
                open_list.append(child)

                ##DEBUG
                rect = Unit.calculate_rect(child.tile, 2)
                pygame.draw.rect(screen, COLOR_RED, rect)
                pygame.display.flip()


            else:
                new_g = current_node.g + 1
                if my_node.g > new_g:
                    my_node.g = new_g
                    my_node.parent = current_node



