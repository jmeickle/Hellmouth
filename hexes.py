# Functions for making hexes easier to use.

def signum(int):
    if int < 0:
        return -1
    else:
        return 1

def dist(x1, y1, x2, y2):
    dx = x1 - x2
    dy = y1 - y2
    if signum(dx) != signum(dy):
        dist = max(abs(dx), abs(dy))
    else:
        dist = abs(dx) + abs(dy)

    return dist

def hex_iterator(map, x, y, rank, curr=0):
    mid = 10
    print "Rank %d Hexagon:" % curr,
    for Y in range(-curr, curr+1):
        print ""
        for X in range(-curr, curr+1):
            if X+curr < x and y-curr > Y:
                continue 
            elif X-curr > x and y+curr < Y:
                continue
            elif dist(x, y, X, Y) != curr:
                print "   -   ",
                continue
            else:
                print "(%2d,%2d)" % (X, Y),
                map[X+mid][Y+mid] = curr
    print "\n"
    if curr < rank:
        hex_iterator(map, x, y, rank, curr+1)

# Simple hex debugger
map = []
for y in range(0,20):
    map.append([])
    for x in range(0,20):
        map[y].append(".")

print "Array coordinates:"
hex_iterator(map,0,0,4)

import sys

print "Distance in array representation:"
for y in range(0,20):
    for x in range(0,20):
        sys.stdout.write(" %s"%map[y][x])
    print "\n",
print ""

print "Distance in hex representation:"
for y in range(0,20):
    for spc in range(y):
        sys.stdout.write(" ")
    for x in range(0,20):
        sys.stdout.write(" %s"%map[y][x])
    print "\n",
