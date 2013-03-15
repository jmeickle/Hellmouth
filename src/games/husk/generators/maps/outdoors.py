from src.games.husk.agents.terrain.outdoors import Corn, TrampledCorn

from src.lib.generators.maps.mapgen import MapGen
from src.lib.objects.terrain import Stairs

from src.lib.util.hex import *

class Cornfield(MapGen):
    def __init__(self, exits=None):
        super(Cornfield, self).__init__(exits)
        self.wall_width = 3
        self.entry = mult(SW, self.size-self.wall_width)

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

    # Place random stairs, then set their positions in a list.
    def place_exits(self):
        if self.exits is None:
            return False
        exits = []
        for which, exit in self.exits.items():
            where, pos = exit
            if not pos:
                pos = mult(NE, self.size - self.wall_width)
            self.cells[pos] = (None, Stairs(which, where))
            exits.append((which, pos))
        self.exits = exits