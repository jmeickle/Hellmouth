import random

from src.lib.agents.terrain.terrain import Wall, EastWestWall, NorthSouthWall, DirtRoad
from src.games.husk.agents.terrain.outdoors import Corn, TrampledCorn
from src.games.husk.generators.maps.outdoors import Cornfield

from src.lib.util.debug import *
from src.lib.util.dice import *
from src.lib.util.hex import *

class Farmhouse(Cornfield):
    def __init__(self, exits=None):
        super(Farmhouse, self).__init__(exits)
        self.size = 50
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

        # Farmhouse
        farmhouse_pos = add(self.center, mult(NE, 25))
        self.place_building(farmhouse_pos, 10, 10)

        # Outlying buildings
        for direction in [CW, SE]:
            distance = r1d6()+15
            position = add(self.center, mult(direction, distance))
            self.place_cluster(position)
            self.place_road(add(direction, self.center), position)

        self.place_road(self.entry, farmhouse_pos)
        # TODO: only works for 5,5
        # x = 0
        # for cell in house:
        #     # North wall
        #     if x < width:
        #         self.cells[cell] = (None, NorthSouthWall())
        #     # East wall
        #     elif x < width + height:
        #         self.cells[cell] = (None, EastWestWall())
        #     # South wall                
        #     elif x < 2*width + height + 1:
        #         self.cells[cell] = (None, NorthSouthWall())
        #     # West wall
        #     elif x < 2*width + 2*height + 1:
        #         self.cells[cell] = (None, EastWestWall())
        #     # Northwest corner
        #     else:
        #         self.cells[cell] = (None, NorthSouthWall())
        #     x += 1

        self.place_passages()

    def random_directions(self, num):
        assert num <= 6

        directions = dirs[:]
        while num > 0:
            num -= 1
            direction = random.choice(directions)
            directions.remove(direction)
            yield direction

    def place_cluster(self, origin):
        for direction in self.random_directions(random.choice([1,2,2,3])):
            building_position = add(origin, mult(direction, 3))#+4))
            self.place_building(building_position, r1d6()/2+2, r1d6()/2+2)
            # self.place_road(origin, building_position)

    def place_road(self, start, end):
        road = []
        cells = line(start, end)

        x = 0
        loops = 0
        while x < len(cells) and loops < 1000:
            loops += 1
            pos = cells[x]
            data, terrain = self.cells[pos]
            if not terrain:
                x += 1
                road.append(pos)
            else:
                x += 1                
                continue
                # Retry:
                # x = max(0, x-5)
                # road = road[0:-5]

        for pos in road:
            self.cells[pos] = (None, DirtRoad())

    def place_building(self, origin, height, width):
        for cell in rectangle_perimeter(origin, height, width):
            self.cells[cell] = (None, Wall())