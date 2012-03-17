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

        # Event log
        self.log = None

        # Player
        self.player = None

        # View range for the map
        self.viewrange = 11

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

    # TODO: FIGURE OUT THIS SECTION, WHAT THE FUCK
    # Place an object on the map.
    def put(self, obj, pos, terrain=False):
        #if self.valid(pos) is False:
        #    return False

        cell = self.cell(pos)

        # TODO: Prevent this from ever happening...
        #if cell is None:
        #    return False

        if cell.blocked() is True:
            return False

        if terrain is False:
            # Update the map
            cell.add(obj, terrain)
            self.queue.append(obj)

            # Update the actor
            obj.pos = pos
            obj.map = self

        else:
            # Update the map
            cell.add(obj, terrain)

        return obj

    # Return a cell at a pos tuple.
    def cell(self, pos):
        return self.cells[pos[0]][pos[1]]

    # Return an actor at a pos tuple.
    def actor(self, pos):
        return self.cell(pos).actor

    # Return terrain at a pos tuple.
    def terrain(self, pos):
        return self.cell(pos).terrain

    # Decides whether a position exists.
    def valid(self, pos):
        if pos[0] < 0 or pos[0] >= self.width \
        or pos[1] < 0 or pos[1] >= self.height:
            return False
        else:
            return True

class Cell:
    def __init__(self, glyph='.', color=None):
        # Basic cell details
        self.glyph = glyph
        self.color = color

        # Stuff inside the cell
        self.actor = None
        self.terrain = None

    # Add a actor to a cell.
    def add(self, obj, terrain=False):
        if obj is None:
            exit("Tried to place a non-object")

        if terrain is False:
            if self.actor is None:
                self.actor = obj
            else:
                return false
        else:
            if self.terrain is None:
                self.terrain = obj
                if self.terrain is None:
                   exit("No terrain after placement")
            else:
                return false

    # Stub, for eventually handling multiple things
    def remove(self, obj):
        self.actor = None

    # Return a glyph to display for this cell.
    # Later, this will be a better function.
    def draw(self):
        if self.terrain is not None:
            return self.terrain.glyph, self.terrain.color
        elif self.actor is not None:
            return self.actor.glyph, self.actor.color
        else:
            return self.glyph, self.color

    # Return whether the cell has a creature in it.
    def occupied(self):
        if self.actor is not None:
            return True

    # Return whether the cell has blocking terrain in it.
    def impassable(self):
        if self.terrain is not None:
            if self.terrain.blocking is True:
                return True

    # Return whether the cell is passable
    def blocked(self):
        if self.occupied() is True or self.impassable() is True:
            return True

class Terrain():
    def __init__(self, glyph="X", color="red-black", blocking=True):
        self.glyph = glyph
        self.color = color
        self.blocking = blocking

if __name__ == '__main__':
    # Basic test: make a map and print it
    map = Map()
    map.loadmap(2, 2)
    print map

    # More advanced: add an actor   
    from actor import Actor
    map.put(Actor(), (0, 0))
    print map.cells[0][0].actor.name
