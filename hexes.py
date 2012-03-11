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

def hex_iterator(map, x, y, rank, debug=False, curr=0):
    if debug is True:
        print "Rank %d Hexagon:" % curr,
    for Y in range(-curr, curr+1):
        if debug is True:
            print ""
        for X in range(-curr, curr+1):
            if debug is True:
                if dist(x, y, x+X, y+Y) < curr:
                    print "   -   ",
                elif dist(x, y, x+X, y+Y) > curr:
                    print "   +   ",
            if dist(x, y, x+X, y+Y) == curr:
                if debug is True:
                    print "(%2d,%2d)" % (X, Y),
                map[x+X][y+Y] = curr
    if debug is True:
        print "\n"
    if curr < rank:
        hex_iterator(map, x, y, rank, debug, curr+1)

# Simple tool to test hex code.
# Takes a center point, hex size, and map size.
def hex_tester(x, y, rank, height, width):

    print "Rank %s Hexagon at %s,%s; Map %sx%s" % (rank,x,y,width,height)

    # Generate empty map.
    map = []
    for Y in range(0,height):
        map.append([])
        for X in range(0,width):
            map[Y].append(".")

    print "Array coordinates:"
    hex_iterator(map,x,y,rank,debug=True)

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
    import sys
#    import getopt
#    options = getopt.getopt(sys.argv[1:], 'xyrhw')
    x = 10
    y = 10
    rank = 8
    height = 24
    width = 24
#    hex_tester(0,0,4,20,20)
    hex_tester(x, y, rank, height, width)
