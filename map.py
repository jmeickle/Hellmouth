import random
from random import randint

class Map:
    def __init__(self):
        self.cells = None
        self.height = None
        self.width = None

    def loadmap(self, x, y):
        random.seed("TEST")
        content = ("~", ".", ",", "!", "?")

        self.cells = []
        for Y in range(y):
            self.cells.append([])
            for X in range(x):
                self.cells[Y].append(Cell(content[randint(0, 4)]))
        self.height = Y+1
        self.width = X+1

    # Place an object on the map.
    def put(self, obj, pos):
        # Update the map
        self.cells[pos[0]][pos[1]].add(obj)

        # Update the object
        obj.pos = pos
        obj.map = self
        return obj

class Cell:
    def __init__(self, glyph):
        if glyph is None:
            self.glyph = 'X'
        else:
            self.glyph = glyph
        self.monster = None

    # Add a monster to a cell.
    def add(self, obj):
        if self.monster is None:
            self.monster = obj
        else:
            return False

    # Stub, for eventually handling multiple things
    def rem(self, obj):
        self.monster = None

    # Return a glyph to display for this cell.
    # Later, this will be a better function.
    def draw(self):
        if self.monster is not None:
            return self.monster.glyph
        else:
            return self.glyph

if __name__ == '__main__':
    # Basic test: make a map and print it
    map = Map()
    map.loadmap(2, 2)
    print map

    # More advanced: add an actor   
    from actor import Actor
    map.put(Actor(), (0, 0))
    print map.cells[0][0].monster.name
