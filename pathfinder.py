# My first attempt at implementng an A* (a star) pathfinding algorithm

import pygame, sys, random, math
from pygame.locals import *

pygame.init()


def get_path_from_gridStartGoal(grid, start, goal):

    start.g_score = 0
    open_list = [start]
    closed_list = []
    add_to_open = get_neighbors(grid, open_list, closed_list, start)
    for cell in add_to_open:
        cell.parent = start
    open_list.extend(add_to_open)
    open_list.remove(start)
    closed_list = [start]

    active_cell = start

    while active_cell != goal and open_list:
        for cell in open_list:
            cell.h_score = int(math.hypot( goal.coords[0] - cell.coords[0],
                                       goal.coords[1] - cell.coords[1] ))
            cell.f_score = cell.g_score + cell.h_score
        open_list.sort(key=lambda cell: cell.f_score) # sorts by f_score
        active_cell = open_list.pop(0) # pops cell with lowest f_score
        closed_list.append(active_cell)
        open_list.extend(get_neighbors(grid, open_list, closed_list, active_cell))
    if active_cell != goal:
        return [start]
    path = [goal]
    paint = goal
    while paint != start:
        path.append(paint.parent)
        paint = paint.parent
    path.reverse() # so that the path list is ordered from start to goal
    return path
        




# take a cell and return a list of the open surrounding cells
def get_neighbors(grid, open_list, closed_list, base, cutting_illegal=True):
    potentials = ((-1,-1), (0,-1), (1,-1), (-1,0), (1,0), (-1,1), (0,1), (1,1))
    gridWidth = len(grid)-1     # This stuff could be calculated once until grid changes?
    gridHeight = len(grid[0])-1 #
    neighbors = []
    for (i,j) in potentials:
        x_pos = base.coords[0]+i
        y_pos = base.coords[1]+j
        # make sure that the cells in the returned list are passable
        illegal = False
        if x_pos < 0 or x_pos > gridWidth or y_pos < 0 or y_pos > gridHeight:
            illegal = True
        elif 'wall' in grid[x_pos][y_pos].pathType:
            illegal = True
        elif grid[x_pos][y_pos] in closed_list:
            illegal = True
        # the following four elifs are to prevent cutting across corners
        elif i == -1 and 'wall' in grid[x_pos][base.coords[1]].pathType and cutting_illegal:
            illegal = True
        elif i == 1 and 'wall' in grid[x_pos][base.coords[1]].pathType and cutting_illegal:
            illegal = True
        elif j == -1 and 'wall' in grid[base.coords[0]][y_pos].pathType and cutting_illegal:
            illegal = True
        elif j == 1 and 'wall' in grid[base.coords[0]][y_pos].pathType and cutting_illegal:
            illegal = True
        if not illegal:
            if grid[x_pos][y_pos] not in open_list:
                confirmed = grid[x_pos][y_pos]
                confirmed.parent = base
                if i == 0 or j == 0:
                    confirmed.g_score = confirmed.parent.g_score + 10
                elif i != 0 and j != 0:
                    confirmed.g_score = confirmed.parent.g_score + 14
                neighbors.append(confirmed)
            # if it's already on the open list, make sure this parent doesn't offer better g
            else:
                if i == 0 or j == 0:
                    potential_g_score = base.g_score + 10
                elif i != 0 and j != 0:
                    potential_g_score = base.g_score + 14
                if grid[x_pos][y_pos].g_score > potential_g_score:
                    grid[x_pos][y_pos].g_score = potential_g_score
                    
    return neighbors


       




# returns a list of grid cells that is a line between given start and
# end cells, incliding both ends. Bresenham's line algorithm.
def crowLine(x0, y0, x1, y1):
    line = [(x0, y0)]
    dx = abs(x1-x0)
    dy = abs(y1-y0)
    if x0 < x1:
        sx = 1
    else:
        sx = -1
    if y0 < y1:
        sy = 1
    else:
        sy = -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        e2 = 2 * err
        if e2 > -dy:
            err = err - dy
            x0 += sx
        if e2 < dx:
            err = err + dx
            y0 += sy
        line.append((x0, y0))

    return line


class GridCell:
    def __init__(self, GRIDSIZE, gridX, gridY):
        self.coords = (gridX, gridY)
        self.rect = pygame.Rect(gridX * GRIDSIZE, gridY * GRIDSIZE, GRIDSIZE, GRIDSIZE)
        self.outlineSize = 2
        self.outlineColor = None
        self.color = None
        
        self.pathType = []
        self.parent = None
        self.f_score = None
        self.g_score = None
        self.h_score = None
