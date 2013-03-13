from src.lib.generators.maps.mapgen import MapGen
from src.lib.util.hex import *
from src.games.husk.agents.terrain.outdoors import Corn, TrampledCorn

class Cornfield(MapGen):
    def __init__(self, exits=None):
        MapGen.__init__(self, exits)
        self.wall_width = 3

    def attempt(self):
        hexes = area(self.center, self.size, True)

        # Cornfield edge.
        for pos, dist in hexes:
            if dist >= self.size - self.wall_width:
                self.cells[pos] = (dist, self.place_corn())
            else:
                self.cells[pos] = (dist, None)

        hexes = [pos for pos, dist in hexes]

        # Corn rows.
        spacing = 2 # Every other row
        pos = self.center
        for d in [NE, SW]:
            row_start = add(self.center, d)
            while row_start in hexes:
                self.cells[row_start] = (dist, self.place_corn())
                for row in [NW, SE]:
                    row_pos = row_start
                    while row_pos in hexes:
                        row_pos = add(row, row_pos)
                        self.cells[row_pos] = (dist, self.place_corn())
                row_start = add(row_start, mult(d, spacing))

        self.place_exits()
        self.connect_exits()
        self.place_levers()
        return self.cells, self.exits

    def place_corn(self):
        import random
        if random.choice(range(50)) > 40:
            return TrampledCorn()
        else:
            return Corn()