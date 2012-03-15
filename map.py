from collections import deque
#from random import randint

class Map:
    def __init__(self):
        # X / Y height (remember off by ones!)
        self.height = None
        self.width = None

        # List of cell objects
        self.cells = None

        # Action queue and current actor
        self.queue = deque()
        self.acting = None

    def loadmap(self, x, y):
#        content = ("~", ".", ",", "!", "?")

        self.cells = []
        for X in range(x):
            self.cells.append([])
            for Y in range(y):
                self.cells[X].append(Cell())
#content[randint(0, 4)]))
        self.width = X+1
        self.height = Y+1

    # Place an object on the map.
    def put(self, obj, pos):
        # Update the map
        self.cells[pos[0]][pos[1]].add(obj)
        self.queue.append(obj)

        # Update the object
        obj.pos = pos
        obj.map = self
        return obj

class Cell:
    def __init__(self, glyph='.'):
        self.glyph = glyph
        self.monster = None

    # Add a monster to a cell.
    def add(self, obj):
        if self.monster is None:
            self.monster = obj
        else:
            return False

    # Stub, for eventually handling multiple things
    def remove(self, obj):
        self.monster = None

    # Return a glyph to display for this cell.
    # Later, this will be a better function.
    def draw(self):
        if self.monster is not None:
            return self.monster.glyph
        else:
            return self.glyph

    # Return whether the cell is passable
    def blocked(self):
        if self.monster is not None:
            return True

if __name__ == '__main__':
    # Basic test: make a map and print it
    map = Map()
    map.loadmap(2, 2)
    print map

    # More advanced: add an actor   
    from actor import Actor
    map.put(Actor(), (0, 0))
    print map.cells[0][0].monster.name
