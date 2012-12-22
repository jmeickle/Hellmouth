# Functions for making hexes easier to use.
import random

from define import *
from dice import *
from math import *

#
# Hexagonal coordinate system definitions.
#

# Direction constants.
#
#   NW    NE
#     /  \
# CW | CC | CE
#     \  /
#   SW    SE

# No location
ANYWHERE = None

# Center
CC = (0,0)

# Northwest
NW = (0, -1)
# Northeast
NE = (1, -1)
# East
CE = (1, 0)
# Southeast
SE = (0, 1)
# Southwest
SW = (-1, 1)
# West
CW = (-1, 0)

# List of directions
dirs = [NW, NE, CE, SE, SW, CW]
# Rotation helper dict
rotation = {NW: 0, NE: 1, CE: 2, SE: 3, SW: 4, CW: 5}

#
# Offset directions for rendering.
#

# North
NN = (0, -1)
# "Half" east
EE = (1, 0)
# South
SS = (0, 1)
#"Half" west
WW = (-1, 0)

# List of offsets.
offsets = [NN, EE, SS, WW]

# Return a direction to face in after a number of turns right.
def rot(dir, turns=1):
    if dir == CC:
        return dir
    start = rotation[dir]
    end = (start+turns) % num_dirs
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


# A generic shape. Can be anything; only requires a center.
class Shape():
    def __init__(center):
        self.center = center

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
def perimeter(origin, rank):
    if rank == 0:
        return [origin]
    corner = add(origin, mult(SE, rank))
    hexes = [corner]
    for dir in dirs:
        hexes.extend(cardinal_line(corner, rank, dir))
        corner = hexes[-1]
    return hexes

# Find all hexes up to a given rank.
def area(origin, rank):
    hexes = []
    for r in range(rank):
        hexes.extend(perimeter(origin, r+1))
    return hexes

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

# TODO: Clean this the fuck up.
# TODO: Make function iteration actually work.
# By default, this takes a map[][] and puts the current range in each cell.
def iterator(map, x, y, rank, list=False, iterate=True, debug=False, curr=0):
    if list is True:
        ret = []
    if debug is True:
        print "Rank %d Hexagon:" % curr,
    for Y in range(-curr, curr+1):
        if debug is True:
            print ""
        for X in range(-curr, curr+1):
            if debug is True:
                if distance(x, y, x+X, y+Y) < curr:
                    print "   -   ",
                elif distance(x, y, x+X, y+Y) > curr:
                    print "   +   ",
            if distance(x, y, x+X, y+Y) == curr:
                if debug is True:
                    print "(%2d,%2d)" % (X, Y),
                    map[x+X][y+Y] = curr
                elif list is False:
                    map.append((x+X, y+Y))
                else:
                    ret.append((x+X, y+Y))
    if debug is True:
        print "\n"

    if iterate is True:
        if curr < rank:
            if list is False:
                iterator(map, x, y, rank, list, iterate, debug, curr+1)
            else:
                ret.extend(iterator(map, x, y, rank, list, iterate, debug, curr+1))

    if list is True: return ret

# Generate a map of "."s and return it.
def hex_map(height, width):
    map = []
    for Y in range(0,height):
        map.append([])
        for X in range(0,width):
            map[Y].append(".")
    return map

# Simple tool to test hex code.
# Takes a center point, hex size, and map size.
def hex_tester(x, y, rank, height, width):

    print "Rank %s Hexagon at %s,%s; Map %sx%s" % (rank,x,y,width,height)

    map = hex_map(height, width)

    print "Array coordinates:"
    iterator(map,x,y,rank,debug=True)

    print "Distance in array representation:"
    for Y in range(0,height):
        for X in range(0,width):
            sys.stdout.write(" %s"%map[Y][X])
        print "\n",

    print ""

    print "Distance in hex representation:"
    for Y in range(0,height):
        for spaces in range(Y):
            sys.stdout.write(" ")
        for X in range(0,width):
            sys.stdout.write(" %s"%map[Y][X])
        print "\n",

if __name__ == "__main__":
    import sys # Slightly cleaner printing for the above test code.
#    x = 10
#    y = 10
#    rank = 8
#    height = 24
#    width = 24
    #hex_tester(x, y, rank, height, width)

    # Rotation test
#    import random
#    for x in range(10):
#        dir = random.choice(dirs)
#        num = random.randint(1,6)
#        print "Was", dir,
#        print ", rotated %s to face" % num, rot(dir, num)

    # Line test.
    map = []
    width = 20
    height = 20
    for y in range(width):
        map.append([])
        for x in range(height):
            map[y].append(".")

    pos1 = (width/2, height/2)
    pos2 = (random.randint(1, width)-1, random.randint(1, height)-1)
    steps = line(pos1, pos2)
    print steps

    for step in range(len(steps)):
        x, y = steps[step]
        map[y][x] = step+1
  
    map[pos2[1]][pos2[0]] = "$"
    map[pos1[1]][pos1[0]] = "^"

    for Y in range(height):
        sys.stdout.write(" " * Y)
        for X in range(height):
            sys.stdout.write(" %s" % map[Y][X])
        print "\n",
