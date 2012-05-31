from generators.maps.mapgen import MapGen
from hex import *
from objects.terrain import *

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
        self.connect_exits()
        return self.cells, self.exits

class MeatTunnel(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)

    def attempt(self):
        self.place_exits()
        self.connect_exits()
        return self.cells, self.exits

class MeatTower(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)

    def attempt(self):
        self.place_exits()
        self.connect_exits()
        return self.cells, self.exits

