"""Distance, geometry, rotation, etc. methods for a hexagonal topology."""

import random

from define import *
from dice import *
from math import *

"""Hexagonal coordinate system definitions."""

"""Direction constants.

   NW    NE
     /  \
 CW | CC | CE
     \  /
   SW    SE
"""

import itertools

def directions(start=NW):
    """Return an iterator over hexagonal directions, starting from a provided direction."""
    index = dirs.index(start)
    return itertools.cycle(dirs[index:] + dirs[:index])

# Return a direction to face in after a number of turns right.
def rot(dir, turns=1):
    if dir == CC:
        return dir
    start = rotation[dir]
    end = (start+turns) % 6
    return dirs[end]

# Alias for rotating 180 degrees (3 rotations).
def flip(dir):
    return rot(dir, 3)

# Return a list of hexes along an arc.
def arc(dir, wide=False):
    if wide is True:
        arc_directions = dirs[:]
        arc_directions.remove(dir)
    else:
        arc_directions = [dir, rot(dir, 1), rot(dir, -1)]
    return arc_directions

# Add two tuples (typically, add a hex dir to a hex pos).
def add(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]

# Subtract two coordinates.
def sub(pos1, pos2):
    return pos1[0] - pos2[0], pos1[1] - pos2[1]

# Multiply a coordinate (typically a direction) by an integer.
def mult(pos, int):
    return pos[0] * int, pos[1] * int

# Divide a tuple by an int.
def div(pos, int):
    return pos[0] / int, pos[1] / int

# Calculate hexagonal distance between two coordinates.
def dist(pos1, pos2):
    return distance(pos1[0], pos1[1], pos2[0], pos2[1])

# Calculate hexagonal distance between two pairs of X, Y coordinates.
def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if signum(dx) != signum(dy):
        distance = max(abs(dx), abs(dy))
    else:
        distance = abs(dx) + abs(dy)
    return distance

# Get the hexes along a cardinal direction.
def cardinal_line(origin, dist, dir):
    pos = origin
    cells = []
    for index in range(dist):
        pos = add(pos, dir)
        cells.append(pos)
    return cells

# Get the hexes along a Bresenham line.
def line(pos1, pos2, max=None):
    line = []

    dx, dy = sub(pos2, pos1)
    sig = (signum(dx) != signum(dy))

    if dx < 0:
        xone = -1
    else:
        xone = 1

    if dy < 0:
        yone = -1
    else:
        yone = 1

    if dx % 2 != 0:
        dx *= 2
        dy *= 2

    dx = abs(dx)
    dy = abs(dy)
    factor = dx/2

    x, y = pos1
    line.append((x, y))

    if dx >= dy:
        while x != pos2[0] or y != pos2[1]:
            factor += dy
            if factor >= dx:
                factor -= dx
                if sig is True:
                    x += xone
                    y += yone
                else:
                    x += xone
                    line.append((x,y))
                    y += yone
            else:
                x += xone
            if max and len(line) >= max:
                break
            line.append((x,y))
    else:
        while x != pos2[0] or y != pos2[1]:
            factor += dx
            if factor >= dy:
                factor -= dy
                if sig is True:
                    y += yone
                    x += xone
                else:
                    y += yone
                    line.append((x,y))
                    x += xone
            else:
                y += yone
            if max and len(line) >= max:
                break
            line.append((x,y))
    return line


# TODO: A generic shape. Can be anything; only requires a center.
# class Shape():
#     def __init__(center):
#         self.center = center

# A hexagon, which is the hexgrid equivalent of a square.
#
# The rank is the number of full hexes from the center to the edge, like so:
#
#  2 2 2
# 2 1 1 2
#2 1 0 1 2
# 2 1 1 2
#  2 2 2

# class Hexagon(Shape):
#     def __init__(center, rank=1):
#         Shape.__init__(self, center)
#         self.rank = rank
#         self.cells = self.area(center, rank)

# Find all hexes at a given distance.
def perimeter(origin, rank, data=False):
    if rank == 0:
        if data is False:
            return [origin]
        else:
            return [(origin, 0)]
    corner = add(origin, mult(SW, rank))
    cells = [corner]
    for dir in dirs:
        cells.extend(cardinal_line(corner, rank, dir))
        corner = cells[-1]
    if data is False:
        return cells
    else:
        return [(cell, rank) for cell in cells]

# Find all hexes up to a given rank.
def area(origin, rank=1, data=False):
    cells = []
    for r in range(rank+1):
        cells.extend(perimeter(origin, r, data))
    return cells

# Return a number of random points on a perimeter.
def random_perimeter(origin, rank, choices=1):
    cells = perimeter(origin, rank)
    points = []
    for x in range(choices):
        choice = random.choice(cells)
        cells.remove(choice)
        points.append(choice)
    return points

# Return a number of random points on an area.
def random_area(origin, rank, choices=1):
    cells = area(origin, rank)
    points = []
    for x in range(choices):
        choice = random.choice(cells)
        cells.remove(choice)
        points.append(choice)
    return points

# TODO: fix
def rectangle_perimeter(origin, height, width, data=False):

    nw_corner = add(origin, mult(NW, height/2))
    pos = nw_corner

    for w in range(width):
        pos = add(pos, CE)
        yield pos

    for h in range(height/2 + 1):
        pos = add(pos, SE)
        yield pos
        pos = add(pos, SW)
        yield pos

    for w in range(width):
        pos = add(pos, CW)
        yield pos

    for h in range(height/2 + 1):
        pos = add(pos, NW)
        yield pos
        pos = add(pos, NE)
        yield pos