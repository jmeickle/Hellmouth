import random
from dice import *
from hex import *
from encounter import Terrain, Cell
import itertools

class MeatArena():
    #def __init__(self):


    def attempt(self, map):
        rank = 25
        center_x, center_y = (0,0)

        # Hexagonal walls around the arena.
        wall_rank = rank + 3

        # Arena floor hexes
        arena = area(rank)
        # Wall hexes
        walls = area(wall_rank, (center_x, center_y))

        for pos in walls:
            map.cells[pos] = Cell(pos)
            map.put(Terrain(), pos, True)

        for pos in arena:
            map.cells[pos].terrain = None

        # Randomly placed columns
        colnum = rank / 2 + r1d6()
        for x in range(colnum):
            colsize = random.randint(1, 3)
            pos = (center_x + flip()*random.randint(4, rank)-colsize, center_y + flip() * random.randint(4,rank)-colsize)
            col = area(colsize, pos)#hex.iterator(map, pos[0], pos[1], colsize, True, True, False, 0)
            for loc in col:
                map.put(Terrain(), loc, True)
