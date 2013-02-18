from src.lib.generators.maps.mapgen import MapGen
from src.lib.util.hex import *
from src.lib.objects.terrain import *

class MeatArena(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)
        self.wall_width = 3

    def attempt(self):
        hexes = area(self.center, self.size, True)

        # Arena floor / walls
        for pos, dist in hexes:
            if dist > self.size - self.wall_width:
                self.cells[pos] = (dist, MeatWall('inner'))
            elif dist == self.size - self.wall_width:
                self.cells[pos] = (dist, MeatWall('outer'))
            else:
                self.cells[pos] = (dist, None)

        # Randomly placed columns
        num_columns = self.size + r3d6()
        column_positions = random_area(self.center, self.size, num_columns)
        for x in range(num_columns):
            column_size = random.choice((1, 1, 1, 2, 2, 3, 4))
            pos = column_positions.pop()
            column = area(pos, column_size, True)
            for pos, dist in column:
                if dist == column_size:
                    self.cells[pos] = (dist, MeatWall('outer'))
                else:
                    self.cells[pos] = (dist, MeatWall('inner'))

        self.place_exits()
        self.connect_exits()
        self.place_levers()
        return self.cells, self.exits

class MeatTunnel(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)

    def attempt(self):
        cells = line(self.center, self.exits["down"][1])

        # Draw the "sides" of the hall.
        for x in range(1, 10):
            start = add(self.center, mult(NW, x))
            finish = add(self.exits["down"][1], mult(NE, x))
            side_line = line(start, finish)
            for pos in side_line:
                if x < 7:
                    self.cells[pos] = (None, None)
                elif x == 7:
                    self.cells[pos] = (None, MeatWall("outer"))
                else:
                    self.cells[pos] = (None, MeatWall("inner"))

        for x in range(1, 10):
            start = add(self.center, mult(SW, x))
            finish = add(self.exits["down"][1], mult(SE, x))
            side_line = line(start, finish)
            for pos in side_line:
                if x < 7:
                    self.cells[pos] = (None, None)
                elif x == 7:
                    self.cells[pos] = (None, MeatWall("outer"))
                else:
                    self.cells[pos] = (None, MeatWall("inner"))

        for x in range(len(cells)):
            cell = cells[x]
            self.cells[cell] = (None, None)
            # Columns.
            if x % 4 == 0:
                for dir in (NW, SW):
                    pos = add(cell, mult(dir, 3))
                    col = area(pos, 1)
                    for pos, dist in col.items():
                        if dist == 1:
                            self.cells[pos] = (dist, MeatWall('outer'))
                        else:
                            self.cells[pos] = (dist, MeatWall('inner'))


        self.place_exits()
        self.connect_exits()
        return self.cells, self.exits

class MeatTower(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)
        self.size = 12
        self.walls = 3

    def attempt(self):
        hexes = area(self.center, self.size)

        # Arena floor / walls
        for pos, dist in hexes.items():
            if dist > self.size - self.wall_width:
                self.cells[pos] = (dist, MeatWall('inner'))
            elif dist == self.size - self.wall_width:
                self.cells[pos] = (dist, MeatWall('outer'))
            else:
                self.cells[pos] = (dist, None)

        # Randomly placed columns
        colnum = self.size / 2 + r1d6()
        for x in range(colnum):
            colsize = random.randint(1, 3)
            pos = (self.center[0] + coin()*random.randint(4, self.size)-colsize, self.center[1] + coin() * random.randint(4,self.size)-colsize)
            col = area(pos, colsize)
            for pos, dist in col.items():
                if dist == colsize:
                    self.cells[pos] = (dist, MeatWall('outer'))
                else:
                    self.cells[pos] = (dist, MeatWall('inner'))

        # Build the Sauceror's tower.
        tower_center = add(self.center, mult(CE, 15))
        tower = area(tower_center, 10)
        for pos, dist in tower.items():
            if dist == 10:
                self.cells[pos] = (dist, MeatWall('outer'))
            elif dist > 10 - self.wall_width:
                self.cells[pos] = (dist, MeatWall('inner'))
            elif dist == 10 - self.wall_width:
                self.cells[pos] = (dist, MeatWall('outer'))
            else:
                self.cells[pos] = (dist, None)

        # Entrance to the tower.
        for pos in area(add(self.center, mult(CE, 7)), 2):
            self.cells[pos] = (dist, None)

        self.place_exits()
        self.connect_exits()
        return self.cells, self.exits

