import random
from src.lib.util.define import *
from src.lib.util.dice import *
from src.lib.util.hex import *
from src.lib.objects.terrain import *

class LayoutGenerator(object):
    """Base layout generator class. If called, builds a simple hexagonal
    layout."""
    def __init__(self, map_obj):
        self.center = map_obj.center
        self.size = map_obj.size
        self.passages = map_obj.passages

        self.cells = {}

    def attempt(self):
        hexes = area(self.center, self.size, True)
        for pos, dist in hexes:
            self.cells[pos] = (dist, None)
        self.place_passages()

    # Place random stairs, then set their positions in a list.
    def place_passages(self):
        if not self.passages:
            return False
        passages = {}
        for which, passage in self.passages.items():
            where, pos = passage
            if not pos:
                dist = r1d(self.size/2) + self.size/2 - 4
                pos = random_perimeter(self.center, dist).pop()
                self.cells[pos] = (dist, Stairs(which, where))
            else:
                self.cells[pos] = (None, Stairs(which, where))
            passages[which] = self.cells[pos][1] # The terrain above
        self.passages = passages

    def connect_passages(self):
        if self.passages is None:
            return False
        # HACK: Dig line from exit to center.
        for which, pos in self.passages:
            cells = line(self.center, pos)
            cells.pop()
            for cell in cells:
                self.cells[cell] = (None, None)

    def place_levers(self):
        dist = 4
        pos = random_perimeter(self.center, dist).pop()
        self.cells[pos] = (None, Lever(None))

class Cave(LayoutGenerator):
    def __init__(self, **kwargs):
        super(Cave, self).__init__(**kwargs)
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
        hexes = area(pos, size)
        self.store(hexes, size)

        for connection in self.connections.pop(node, []):
            self.place_nodes(connection, pos)

#        for pos, dist in self.cells.items():
#            cells[pos] = (dist, None)

        self.place_passages()

    # Connect nodes with a line.
    def connect_nodes(self, pos1, pos2):
        width = min(r1d6(), 3)
        steps = line(pos1, pos2)
        for step in steps:
            # TODO: Efficiency!
            cells = area(step, width, True)
            for pos, dist in cells.items():
                if dist == width:
                    self.cells[pos] = (None, CaveWall())
                else:
                    self.cells[pos] = (None, None)

    # Place a node, then try to do the same for its children.
    def place_nodes(self, node, origin):
        dir = random.choice(dirs)
        distance = self.scale * r3d6() + r3d6()
        pos = add(origin, (dir[0]*distance, dir[1]*distance))

        self.connect_nodes(origin, pos)

        size = r1d6() + 2
        cells = area(pos, size, True)
        self.store(cells, size)
        for pos, dist in cells:
            self.cells[pos] = (dist, None)

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
