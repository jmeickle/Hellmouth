import define
from dice import *
import hex
import random
import ai/astar

class Location:
    def __init__(self, pos):
        self.name = ""
        self.pos = pos
        self.neighbors = {}
        self.paths = {}
        self.visibility = 1

    def connect(self, loc2, path=True):
        print self, loc2, path
        conn = (self, loc2)
        back = (loc2, self)
        connected = self.neighbors.get(conn, [])
        if not connected:
            self.neighbors[conn] = [path]
            loc2.neighbors[back] = [path]
        else:
            connected.extend([path])
            self.neighbors[conn] = connected
            loc2.neighbors[back] = connected

    def landmark(self):
        return self.visibility

    # Test code.
    def test_put_in(self, map):
        y, x = self.pos
        map[y-1][x-1] = self.landmark()

# Test code.
if __name__ == "__main__":
    # Generate map.
    x = 20
    y = 20
    map = hex.hex_map(x, y)
    # Generate a list of random locations.
    locations = {}
    num_locs = 20
    for i in range(num_locs):
        pos = (random.randint(1, x), random.randint(1, y))
        loc = Location(pos)
        # Init each location with random values.
        if r1d6() > 5:
            loc.visibility += r1d6()
        loc.name = "N%s" % i
        locations[loc.name] = loc
        loc.test_put_in(map)

    # Connect each location to a few random locations.
    for i in range(num_locs):
        for j in range(r1d6()):
            loc1 = locations["N%s" % (random.randint(1, num_locs)-1)]
            loc2 = locations["N%s" % (random.randint(1, num_locs)-1)]
            if r1d6() > 5:
                loc1.connect(loc2, "P%d" % i)
            else:
                loc1.connect(loc2)

    # Print what connects to where
    for i in locations.values():
        print "%s: " % i.name
        for k, v in i.neighbors.items():
            print "%s->%s: " % (i.name, k[1].name),
            for conn in v:
                print "%s," % conn,
            print ""

    # Print map
    for y in range(len(map)):
        print "" 
        if y % 2:
            print "",
        for x in range(len(map[y])):
            print map[y][x],
