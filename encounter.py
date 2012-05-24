# The map, cells in the map, and terrain.
from collections import deque
from describe import commas
from item import Item
import random
import hex
class Encounter:
    def __init__(self):
        self.size = None
        self.center = None

        self.name = "MEAT ARENA"

        # Dict of (hex) cell objects, indexed by pos.
        self.cells = {}

        # Action queue and current actor
        self.queue = deque()
        self.acting = None

        # Event log
        self.log = None

        # Player
        self.player = None
        # Where the player starts
        self.entry = None

    # Handle things that happen when the player enters the map.
    def enter(self, player):
        self.player = player
        self.player.location = self.name
        self.put(self.player, self.entry)

    # Handle things that happen when the player leaves the map.
    def leave(self, player):
        self.player.location = None
        self.player = None

    def generate(self, generate):
        generator = generate()
        cells = generator.attempt()
        # TODO: Possibly checks for validity first
        # TODO: Generator has a field for this.
        self.center = generator.center
        self.entry = self.center
        self.size = generator.size
        # Final step.
        self.populate(cells)

    # Take a provided dict of {pos : data} and turn it into objects.
    def populate(self, cells):
        for pos, contents in cells.items():
            distance, terrain = contents
            cell = Cell(pos)
            if terrain is not None:
                cell.put_terrain(terrain)

            # TODO: Replace this test code with something better.
            if random.randint(1, 10) == 1:
                cell.put(Item())

            self.cells[pos] = cell

    # Return a cell at a pos tuple.
    def cell(self, pos):
        return self.cells.get(pos)

    # Return an actor at a pos tuple.
    def actor(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return None
        else:
            return cell.actor

    # Return terrain at a pos tuple.
    def terrain(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return None
        else:
            return cell.terrain

    # TODO: FIGURE OUT THIS SECTION, WHAT THE FUCK
    # Place an object on the map.
    def put(self, obj, pos, terrain=False):

        cell = self.cells.get(pos)

        if cell is None:
            return False

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

    # Decides whether a position exists.
    def valid(self, pos):
        if self.cells.get(pos) is None:
            return False
        return True

    # Print a large text version of the map.
    def dump(self, size=100, origin=(0,0)):
        import sys
        print "Map of %s:\n" % self.name
        for y in range(-size, size):
            line = ""
            blank = True
            for x in range(-size, size):
                if x % 2 == 0:
                    line += " "
                    continue
                cell = self.cell(((x-y)/2,y))
                if cell is None:
                    glyph = " "
                else:
                    glyph = cell.glyph
                    blank = False
                line += glyph
            if blank is False:
                sys.stdout.write(line)
                sys.stdout.write("\n")
        exit()

class Cell:
    def __init__(self, pos, glyph='.', color=None):
        # Don't really need it but it might come in handy.
        self.pos = pos

        # Basic cell details
        self.glyph = glyph
        self.color = "meat-black"

        # Stuff inside the cell
        self.actor = None
        self.terrain = None
        self.items = {}

    # STUB
    def put_terrain(self, terrain):
        self.terrain = terrain

    # Return a glyph to display for this cell.
    # TODO: improve this function greatly
    def draw(self):
        if self.actor is not None:
            return self.actor.glyph, self.actor.color
        elif self.terrain is not None:
            return self.terrain.glyph, self.terrain.color
        elif len(self.items) > 0:
            return '!', 'magenta-black'
        else:
            return self.glyph, self.color

    # TODO: Options for what to list.
    # TODO: This should go through the 'describe' functions; it should only be returning information, not strings!
    def contents(self):
        list = []
        if self.actor is not None:
            list.append("a %s" % self.actor.name)
        if self.terrain is not None:
            list.append("a %s" % self.terrain.name)
        if len(self.items) > 0:
            list.append("some items")
        return commas(list, True) # Capitalized.

    # ITEMS

    # 'Forcibly' put an item into a cell.
    def _put(self, item):
        list = self.items.get(item.appearance(), None)
        if list is None:
            self.items[item.appearance()] = [item]
        else:
            list.append(item)

    # Put an item into a cell.
    # TODO: Sanity checks that _put doesn't have.
    def put(self, item):
        self._put(item)

    # 'Forcibly' remove a specific item from a cell.
    # Returns the item if it's successfully removed.
    # Returns false if there are no items matching that appearance.
    # Errors if the item is not in the list.
    def _get(self, item):
        list = self.items.get(item.appearance, None)
        if list is not None:
            return list.remove(item)
        else:
            return False

    # Remove a random item of a given appearance from a cell.
    # Returns the item if it's successfully removed.
    # Returns false if there are no items matching the appearance.
    def get(self, appearance):
        list = self.items.get(appearance, None)
        if list is not None:
            return list.remove(random.choice(list))
        else:
            return False

    # Take an appearance and a list, and tack it onto the cell contents.
    def _merge(self, appearance, list):
        current = self.items.get(appearance, None)
        if current is not None:
            return current.extend(list)
        else:
            self.items[appearance] = list

    # Boolean: whether you can get items from a cell
    # STUB: Add real checks here.
    def can_get(self):
        return True

    # Boolean: whether you can put items into a cell
    # STUB: Add real checks here.
    def can_put(self):
        return True

    # Returns how many items of a given appearance are in the cell.
    def count(self, appearance):
        list = self.items.get(item.appearance, None)
        if list is None:
            return 0
        else:
            return len(list)

    # ACTORS

    # Add a actor to a cell.
    def add(self, obj, terrain=False):
        if obj is None:
            exit("Tried to place a non-object")

        if terrain is False:
            if self.actor is None:
                self.actor = obj
            else:
                return False
        else:
            if self.terrain is None:
                self.terrain = obj
                if self.terrain is None:
                   exit("No terrain after placement")
            else:
                return False

    # Stub, for eventually handling multiple things
    def remove(self, obj):
        self.actor = None

    # MOVEMENT

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

if __name__ == '__main__':
    # Basic test: make a map and print it
    size = 50
    map = Encounter(size)
    #hexes = hex.area(map.rank)
    #for hex in hexes:
    #    map.cells[hex] = None

    # Prepare the map.
    map.loadmap()

    #print map.cells
    print len(map.cells)
    #print map.cells
    # More advanced: add an actor   
    #from actor import Actor
    #map.put(Actor(), (0, 0))
    #print map.cells[0][0].actor.name

    #for y in range(-15, 15):
    #    str = ""
    #    for x in range(-15, 15):
    #        str += map.cells.get((x,y), "x")
    #    print "%s%s" % (" " * (y%2), str)
