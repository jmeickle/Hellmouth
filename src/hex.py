import random

from define import *
from dice import *

# Functions for making hexes easier to use.
# Directional stuff
# Center!
CC = (0,0)

NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)
dirs = [NW, NE, CE, SE, SW, CW]
rotation = {NW: 0, NE: 1, CE: 2, SE: 3, SW: 4, CW: 5}
num_dirs = len(dirs)

# Offset directions. These only make sense in the context of rendering!
NN = (0, -1)
EE = (1, 0)
SS = (0, 1)
WW = (-1, 0)
offsets = [NN, EE, SS, WW]
num_offsets = len(offsets)

# Other directional information.
ANYWHERE = None

# Return the sign of a number.
def signum(int, zero=False):
    if int < 0:
        return -1
    elif int == 0 and zero is True:
        return 0
    else:
        return 1

# Return a direction to face in after a number of turns right.
def rot(dir, turns=1):
    if dir == CC:
        return dir
    start = rotation[dir]
    end = (start+turns) % num_dirs
    return dirs[end]

# Alias for 3 rotations.
def flip(dir):
    return rot(dir, 3)

# Add a hex dir to a hex pos.
def add(pos, dir):
    return pos[0] + dir[0], pos[1] + dir[1]

# Subtract two tuples.
def sub(pos1, pos2):
    return pos1[0] - pos2[0], pos1[1] - pos2[1]

# Multiply a tuple by an int.
def mult(pos, int):
    return pos[0] * int, pos[1] * int

# Calculate hex distance with two hex positions.
def dist(pos1, pos2):
    return distance(pos1[0], pos1[1], pos2[0], pos2[1])

def distance(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if signum(dx) != signum(dy):
        distance = max(abs(dx), abs(dy))
    else:
        distance = abs(dx) + abs(dy)
    return distance

# Generate a perimeter around an origin and return random points on it.
def random_perimeter(dist, origin=CC, choices=1):
    cells = perimeter(dist, origin)
    points = []
    for x in range(choices):
        choice = random.choice(cells)
        cells.remove(choice)
        points.append(choice)
    return points

# Generate a perimeter around an origin and return random points on it.
def random_area(dist, origin=CC, choices=1):
    cells = area(dist, origin)
    points = []
    for x in range(choices):
        choice = random.choice(cells.keys())
        del cells[choice]
        points.append(choice)
    return points

# Turns out this is slower. Xom laughs.
def _area(rank, pos, dir, left=False, right=True, curr=0):
    hexes = [pos]
    if curr < rank:
        hexes.extend(_area(rank, add(pos, dir), dir, False, False, curr+1))
        if right is True:
            hexes.extend(_area(rank, add(pos, rot(dir)), dir, left, right, curr+1))
        if left is True:
            hexes.extend(_area(rank, add(pos, rot(dir, 5)), dir, left, right, curr+1))
    return hexes

# Generate a dict of hex position : distance, including the start position.
def area(rank, origin=CC, info=True):
    hexes = {}
    # +1 to account for needing both == 0 and == rank.
    for x in range(rank+1):
        for hex in perimeter(x, origin, info):
            if info is True:
                hex, data = hex
                hexes[hex] = data
            else:
                hexes[hex] = True
    return hexes

    # Older method, could be good but needs work:
    #for dir in dirs:
    #    hexes.extend(_area(rank, add(origin, dir), dir, True))
    #return hexes

# Oldest method. Crude!
#    for Y in range(-rank, rank+1):
#        for X in range(-rank, rank+1):
#            offset = (X,Y)
#            hex = add(origin, offset)
#            distance = dist(origin, hex)
#            if distance <= rank:
#                hexes[hex] = distance
#    return hexes

# Hexes on the edge of an area.
def perimeter(rank, origin=CC, info=False):
    hexes = []
    if rank == 0:
        data = origin
        if info is True:
            data = (data, 0)
        hexes.append(data)
    else:
        pos = add(origin, mult(SW, rank))
        for dir in dirs:
            next = add(pos, mult(dir, rank))
            for hex in line(pos, next):
                data = hex
                if info is True:
                    data = (data, rank)
                hexes.append(data)
            pos = next
    return hexes

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
