import random
from define import *
from dice import *
from hex import *

# Map generator class. If called, builds a hexagonal shape of plain tiles.
class MapGen():
    def __init__(self):
        self.center = (0,0)
        self.size = 25
        self.cells = {}

    def attempt(self):
        hexes = area(self.size, self.center)
        for pos, dist in hexes.items():
            self.cells[pos] = (dist, None)
        return self.cells

class MeatArena(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self.walls = 3

    def attempt(self):
        hexes = area(self.size, self.center)

        # Arena floor / walls
        for pos, dist in hexes.items():
            if dist > self.size - self.walls:
                self.cells[pos] = (dist, 'wall-outer')
            elif dist == self.size - self.walls:
                self.cells[pos] = (dist, 'wall-inner')
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
                    self.cells[pos] = (dist, 'wall-outer')
                else:
                    self.cells[pos] = (dist, 'wall-inner')

        return self.cells

class Cave(MapGen):
    def __init__(self):
        MapGen.__init__(self)
        self.max_connections = 30
        self.max_nodes = 40
        self.scale = 1

        self.nodes = []
        self.connections = {}

    def attempt(self):
        self.build_nodes()
        node = self.nodes.pop(0)

        # Entry point, at (0, 0).
        pos = self.center
        cells = area(3, pos)
        self.cells.update(cells)

        for connection in self.connections.pop(node, []):
            self.place_nodes(connection, pos)

        cells = {}

        for pos, dist in self.cells.items():
            cells[pos] = (dist, None)

        return cells

    # Connect nodes with a line.
    def connect_nodes(self, pos1, pos2):
        width = min(r1d6(), 3)
        steps = line(pos1, pos2)
        for step in steps:
            if width > 1:
                cells = area(width-1, step)  # TODO: Efficiency!
                for cell in cells.keys():
                    self.cells[cell] = (None, None)
            else:
                self.cells[step] = (None, None)

    # Place a node, then try to do the same for its children.
    def place_nodes(self, node, origin):
        dir = random.choice(dirs)
        distance = self.scale * r3d6() + r3d6()
        pos = add(origin, (dir[0]*distance, dir[1]*distance))

        self.connect_nodes(origin, pos)

        size = r1d6() + 2
        cells = area(size, pos)
#        for pos, dist in cells.items():
#            self.cells[pos] = (dist, None)
        self.cells.update(cells)

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
