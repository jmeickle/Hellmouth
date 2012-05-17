# Functions for making hexes easier to use.

def signum(int):
    if int < 0:
        return -1
    else:
        return 1

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
    x = 10
    y = 10
    rank = 8
    height = 24
    width = 24
    hex_tester(x, y, rank, height, width)
