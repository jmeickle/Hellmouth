# Code based on:
#     http://www.vanreijmersdal.nl/54/hexagon-pathfinding/
# which itself was based on:
#     http://www.policyalmanac.org/games/aStarTutorial.htm
# and found through:
#     http://www.amagam.com/hexpath/

from src.lib.util.define import *

class AStar(object):
    def __init__(self, agent, map, metric=None, heuristic=None):
        self.open_list = {}
        self.closed_list = {}
        self.agent = agent
        self.map = map
        self.metric = self.map.level.metric if not metric else metric
        self.heuristic = self.metric.distance if not heuristic else heuristic

    def add_open(self, pos, parent=None, first_node=False):
        cell = self.map.cell(pos)
        if not cell:
            """No need to even create a node if it's not even a cell."""
            self.closed_list[pos] = None
            return False
        else:
            if first_node or not cell.can_block(self.agent):
                """Can pass through this cell. Add it to the open list."""
                node = AStarNode(self, pos, parent)
                self.open_list[pos] = node
                return node
            # TODO: Figure these conditions out?
            # elif blocked is False and cell.can_block(self.agent) is False:
            #     node = AStarNode(self, pos, parent)
            #     self.open_list[pos] = node
            #     return node
            # Can't pass through, but keep it around.
            else:
                """Cannot pass through this cell."""
                self.add_closed(pos, parent)
                return False

    def add_closed(self, pos, parent=None):
        """Create an AStarNode, but move it directly to the closed list."""
        node = AStarNode(self, pos, parent)
        self.closed_list[pos] = node
        return node

    def move_open(self, pos):
        """Move an AStarNode from the open list to the closed list."""
        self.open_list[pos] = self.closed_list[pos]
        del self.closed_list[pos]

    def move_closed(self, pos):
        """Move an AStarNode from the closed list to the open list."""
        self.closed_list[pos] = self.open_list[pos]
        del self.open_list[pos]

    def lower(self, node1, node2):
        """Return the AStarNode with the lower cost."""
        if node1.cost < node2.cost:
            return node1
        else:
            return node2

    def lowest(self):
        """Return the AStarNode with the lowest cost from the open list."""
        return reduce(lambda x, y: self.lower(x, y), self.open_list.values())

    def path(self, pos, dest):
        """Request a path from a position to a destination."""
        curr = self.add_open(pos, None, True)
        for heading in self.metric.headings:
            pos = self.add_open(curr.pos + heading, curr)
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
        """Internal method to request a path from a position to a destination."""
        self.move_closed(curr.pos)
        if curr.pos == dest:
            return curr

        for heading in self.metric.headings:
            pos = curr.pos + heading
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

class AStarNode(object):
    """A node within an AStar object."""
    def __init__(self, astar, pos, parent):
        self.astar = astar
        self.pos = pos
        self.parent = parent
        self.g = 0
        self.h = 0
        self.cost = 0

    def set_cost(self, start, dest, calculate=True):
        """Set the cost of moving into this AStarNode."""
        self.g = 1 # Later: base move cost on involved terrain.
        if calculate is True:
            self.h = self.astar.heuristic(self.pos, dest)
        self.cost = self.g + self.h

    def get_path(self):
        """Return the path to this AStarNode's parent."""
        if self.parent is None:
            return []
        else:
            return [self.pos] + self.parent.get_path()

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
