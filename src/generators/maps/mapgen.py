import random
from define import *
from dice import *
from hex import *
from objects.terrain import *

# Map generator class. If called, builds a hexagonal shape of plain tiles.
class MapGen():
    def __init__(self, exits=None):
        self.center = (0,0)
        self.size = 25
        self.cells = {}
        self.exits = exits

    def attempt(self):
        hexes = area(self.size, self.center)
        for pos, dist in hexes.items():
            self.cells[pos] = (dist, None)
        self.place_exits()
        return self.cells

    # Place random stairs.
    def place_exits(self):
        for which, exit in self.exits.items():
            where, pos = exit
            if pos is None:
                dist = r1d(self.size)
                pos = random_pos(dist, self.center)
            self.cells[pos] = (dist, Stairs(which, where))

class MeatArena(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)
        self.walls = 3

    def attempt(self):
        hexes = area(self.size, self.center)

        # Arena floor / walls
        for pos, dist in hexes.items():
            if dist > self.size - self.walls:
                self.cells[pos] = (dist, MeatWall('inner'))
            elif dist == self.size - self.walls:
                self.cells[pos] = (dist, MeatWall('outer'))
            else:
                self.cells[pos] = (dist, None)

        # Randomly placed columns
        colnum = self.size / 2 + r1d6()
        for x in range(colnum):
            colsize = random.randint(1, 3)
            pos = (self.center[0] + flip()*random.randint(4, self.size)-colsize, self.center[1] + flip() * random.randint(4,self.size)-colsize)
            col = area(colsize, pos)
            for pos, dist in col.items():
                if dist == colsize:
                    self.cells[pos] = (dist, MeatWall('outer'))
                else:
                    self.cells[pos] = (dist, MeatWall('inner'))

        self.place_exits()
        return self.cells

class Cave(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)
        self.max_connections = 30
        self.max_nodes = 40
        self.scale = 1

        self.nodes = []
        self.connections = {}

    def store(self, cells, size):
        for pos, dist in cells.items():
            if dist == size and self.cells.get(pos) is None:
                self.cells[pos] = (dist, CaveWall())
            else:
                self.cells[pos] = (dist, None)

    def attempt(self):
        self.build_nodes()

        # Entry point.
        node = self.nodes.pop(0)
        pos = self.center
        size = 5
        hexes = area(size, pos)
        self.store(hexes, size)

        for connection in self.connections.pop(node, []):
            self.place_nodes(connection, pos)

#        for pos, dist in self.cells.items():
#            cells[pos] = (dist, None)

        self.place_exits()
        return self.cells

    # Connect nodes with a line.
    def connect_nodes(self, pos1, pos2):
        width = min(r1d6(), 3)
        steps = line(pos1, pos2)
        for step in steps:
            cells = area(width, step)  # TODO: Efficiency!
            for pos, dist in cells.items():
#                if dist == width:
#                    self.cells[pos] = (None, CaveWall())
#                else:
                    self.cells[pos] = (None, None)

    # Place a node, then try to do the same for its children.
    def place_nodes(self, node, origin):
        dir = random.choice(dirs)
        distance = self.scale * r3d6() + r3d6()
        pos = add(origin, (dir[0]*distance, dir[1]*distance))

        self.connect_nodes(origin, pos)

        size = r1d6() + 2
        cells = area(size, pos)
        self.store(cells, size)
#        for pos, dist in cells.items():
#            self.cells[pos] = (dist, None)

        for connection in self.connections.pop(node, []):
            self.place_nodes(connection, pos)

    def build_nodes(self):
        # Starting node.
        node = len(self.nodes)
        self.nodes.append(node)

        while len(self.connections) < self.max_connections:
            node = random.choice(self.nodes)
            for child in range(max(1, r1d6()-3)):
                # Make a new node and connect to it.
                if len(self.nodes) < self.max_nodes:#random.randint(1, len(self.nodes)) <= self.max_nodes) >= len(self.nodes):
                    child_node = len(self.nodes)
                    self.nodes.append(child_node)
                # Connect to an existing node that isn't us.
                else:
                    child_node = random.choice(self.nodes)
                    if node == child_node:
                        continue;
                # Create the connection.
                list = self.connections.get(node, [])
                list.append(child_node)
                self.connections[node] = list
#                list = self.connections.get(child_node, [])
 #               list.append(node)
#                self.connections[child_node] = list
