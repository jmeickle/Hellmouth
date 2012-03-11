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

#def hex_iterator(x, y, rank):
