import random

from src.lib.agents.terrain.passage import Path
from src.lib.generators.maps.layout import LayoutGenerator

from src.lib.util import debug
from src.lib.util.geometry.hexagon import Hexagon

from src.games.husk.agents.terrain.outdoors import Corn, TrampledCorn

class Cornfield(LayoutGenerator):
    def __init__(self, map_obj):
        super(Cornfield, self).__init__(map_obj)

        self.wall_width = 3

        self.size += 10
        self.wall_width += 10

        self.entry = Hexagon.SW * (self.size-self.wall_width-1)

    def attempt(self):
        # Cornfield edge.
        for rank, index, coords in Hexagon.area(self.center, self.size):
            if rank >= self.size - self.wall_width:
                self.cells[coords] = (rank, self.place_corn())
            else:
                self.cells[coords] = (rank, None)


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

        self.place_passages()
        return self.cells, self.passages

    def place_corn(self):
        if random.choice(range(50)) > 40:
            return TrampledCorn()
        else:
            return Corn()

    def place_passages(self):
        """Place random stairs, then set their positions in a dict."""
        if not self.passages:
            return False
        passages = {}
        perimeter = random.sample([h for h in Hexagon.perimeter(self.center, self.size - self.wall_width)], len(self.passages))

        for which, passage in self.passages.items():
            where, pos = passage
            if not pos:
                index, coords = perimeter.pop()
            # Block off the immediate surroundings.
            for rank, index, coords in Hexagon.area(coords):
                self.cells[coords] = (None, None)
            passages[which] = Path(which, where)
            self.cells[coords] = (None, passages[which])
        self.passages = passages