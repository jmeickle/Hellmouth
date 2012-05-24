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

