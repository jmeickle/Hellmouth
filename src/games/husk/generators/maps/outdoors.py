from src.games.husk.agents.terrain.outdoors import Corn, TrampledCorn

from src.lib.agents.terrain.passage import Path
from src.lib.generators.maps.layout import LayoutGenerator

from src.lib.util.geometry.hexagon import Hexagon

class Cornfield(LayoutGenerator):
    def __init__(self, map_obj):
        super(Cornfield, self).__init__(map_obj)

        self.wall_width = 3

        self.size += 10
        self.wall_width += 10

        self.entry = mult(SW, self.size-self.wall_width-1)

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

        self.place_passages()
        return self.cells, self.passages

    def place_corn(self):
        import random
        if random.choice(range(50)) > 40:
            return TrampledCorn()
        else:
            return Corn()

    def place_passages(self):
        """Place random stairs, then set their positions in a dict."""
        if not self.passages:
            return False
        passages = {}
        perimeter = random_perimeter(self.center, self.size - self.wall_width, len(self.passages))
        for which, passage in self.passages.items():
            where, pos = passage
            if not pos:
                pos = perimeter.pop()
            # Block off the immediate surroundings (rank=1)
            for cell in area(pos):
                self.cells[cell] = (None, None)
            passages[which] = Path(which, where)
            self.cells[pos] = (None, passages[which])
        self.passages = passages