# Code based on:
#     http://www.vanreijmersdal.nl/54/hexagon-pathfinding/
# which itself was based on:
#     http://www.policyalmanac.org/games/aStarTutorial.htm
# and found through:
#     http://www.amagam.com/hexpath/

if __name__ != '__main__':
    from define import *
    from hex import *

def heuristic(pos1, pos2):
# Manhattan (probably totally broken for hexes!):
#    return abs(pos1[0]-pos2[0]) + abs(pos1[1]-pos2[1])
# Pure hexagonal distance:
    return dist(pos1, pos2)

class AStar:
    def __init__(self, map):
        self.open_list = {}
        self.closed_list = {}
        self.map = map

    def add_open(self, pos, parent=None, blocked=False):
        cell = self.map.cell(pos)
        if cell is not None:
            # Can pass through. Use it.
            if blocked is True and cell.blocked() is False:
                node = Node(pos, parent)
                self.open_list[pos] = node
                return node
            elif blocked is False and cell.impassable() is False:
                node = Node(pos, parent)
                self.open_list[pos] = node
                return node
            # Can't pass through, but keep it around.
            else:
                self.add_closed(pos, parent)
                return False
        # No need to even create a node if it's not even a cell.
        else:
            self.closed_list[pos] = None
            return False

    # Create a node, but move it directly to the closed list.
    def add_closed(self, pos, parent=None):
        node = Node(pos, parent)
        self.closed_list[pos] = node
        return node

    def move_open(self, pos):
        self.open_list[pos] = self.closed_list[pos]
        del self.closed_list[pos]

    def move_closed(self, pos):
        self.closed_list[pos] = self.open_list[pos]
        del self.open_list[pos]

    def lower(self, node1, node2):
        if node1.cost < node2.cost:
            return node1
        else:
            return node2

    # Return the lowest value from the open list.
    def lowest(self):
        #return min(self.open_list.values(), key=lambda x:x.cost)
        return reduce(lambda x, y: self.lower(x, y), self.open_list.values())

    # Request a path from a destination to one.
    def path(self, pos, dest):
        curr = self.add_open(pos)

        for dir in dirs:
            pos = self.add_open(add(curr.pos, dir), curr, True)
            if pos is not False:
                pos.set_cost(curr.pos, dest)

        self.move_closed(curr.pos)

        loops = 0
        while len(self.open_list) > 0:
            loops += 1
            next = self.lowest()
            path = self._path(next, dest)
            if path is not False:
                return path.get_path()
            if loops > 10000:
                exit("Too many loops! Length:%s\n%s" % (len(self.open_list), self.open_list))
        return False

    def _path(self, curr, dest):
        self.move_closed(curr.pos)
        if curr.pos == dest:
            return curr

        for dir in dirs:
            pos = add(curr.pos, dir)
            if self.closed_list.get(pos) is None:
                existing = self.open_list.get(pos)
                if existing is None:
                    node = self.add_open(pos, curr)
                    if node is not False:
                        node.set_cost(curr.pos, dest)
                elif existing.g > curr.g:
                    existing.parent = curr
                    existing.set_cost(curr.pos, dest, False)
        return False

class Node:
    def __init__(self, pos, parent):
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.cost = 0

    def set_cost(self, start, dest, calculate=True):
        self.g = 1 # Static move cost for now. Later, based on terrain of square moving into / out of.
        if calculate is True:
            self.h = heuristic(self.pos, dest)
        self.cost = self.g + self.h

    def get_path(self):
        if self.parent is None:
            return []
        else:
            list = [self.pos]
            list.extend(self.parent.get_path())
            return list

# Test code.
if __name__ == "__main__":
    print "Hexagonal A* Test Function"

    # Appends where it's running it from, so that should be the Hellmouth main folder.
    import os, sys
    path = os.path.abspath('.')
    sys.path.append(path)
    import random

    # Hellmouth imports, which depend on lower folders.
    from define import *
    import hex

    # Map parameters.
    x = 50
    y = 50
    start = (13, 13)
    finish = (random.randint(0, x-1), random.randint(0, y-1))

    print "Start: (%s, %s)" % start,
    print "Finish: (%s, %s)" % finish

    # Run A*
    ai = AStar()
    result = ai.path(start, finish)
    if result is False:
        print "Could not find a path. Aborting."
        exit(ai.__dict__)
    else:
        path = result.get_path()
    print "True distance: %s" % dist(start, finish)
    print "Steps taken: %s" % (len(path))# Because it includes (0, 0)
    print "Path taken: %s" % path

    # Generate map
    map = hex_map(x, y)

    # Draw the path
    for pos in path:
        map[pos[1]][pos[0]] = "X"

    # Draw the start and finish
    map[start[1]][start[0]] = "^"
    map[finish[1]][finish[0]] = "$"

    print "Visual representation:"
    for Y in range(0,y):
        for spaces in range(Y):
            sys.stdout.write(" ")
        for X in range(0,x):
            sys.stdout.write(" %s"%map[Y][X])
        print "\n",
