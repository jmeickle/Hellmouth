# The map and cells in the map.
# TODO: Not cells in the map.
from collections import deque
from text import *
from generators.items import generate_item
import random
import hex
from data import screens
import log

class Encounter:
    def __init__(self, level):
        # Maps don't make sense without an associated Level.
        self.level = level
        # We'll use the level's player by default.
        self.player = self.level.player

        # Display information.
        self.name = None
        self.screens = []

        # Map generation parameters.
        self.layout = None
        self.size = None
        self.center = None
        self.exits = None
        self.depth = None
        self.entry = None # Player start point. TODO: Replace by bidirectional stairs!

        # Dict of (hex) cell objects, indexed by pos.
        self.cells = {}

        # Default information if a cell doesn't exist.
        # TODO: Expand!
        self.floor = None

        # Action queue and current actor
        self.queue = deque()
        self.acting = None

        # Where we're traveling to.
        self.destination = None

    # The map portion of the game loop.
    def loop(self):
        # Don't continue looping if we have a destination.
        if self.destination is not None:
            return False

        # If nobody is acting, let the first in the queue act.
        if self.acting is None:
            self.acting = self.queue.popleft()
            self.acting.before_turn()

        # NPCs use act() until the player's turn comes up.
        if self.acting.controlled is False:
            self.acting.act()

    # Go to another map, or if destination is False, let the level figure it out.
    def go(self, destination):
        self.before_leave(destination)

    # By default, before_arrive tries to load the matching screen and plugs in a
    # callback to self.arrive. Otherwise, it calls it itself.
    def before_arrive(self):
        entryscreen = self.level.name + ", " + self.name # HACK: Later it should choose different dict for different levels.
        log.add("You enter %s." % entryscreen)
        if screens.text.get(striptags(entryscreen)) is not None:
            arguments = {"header_right" : entryscreen, "footer_text" : screens.footer, "callback" : self.arrive}
            self.screen(striptags(entryscreen), arguments)
        else:
            return self.arrive()

    # Handle arriving at the map.
    def arrive(self):
        self.player.map = self
        self.put(self.player, self.entry)
        # HACK: Highlights should be handled a bit more nicely than this.
        if self.exits is not None:
            for exit in self.exits:
                which, pos = exit
                self.player.highlights[which] = pos

    # Do anything that needs to happen before confirming that we've left this map.
    def before_leave(self, destination):
        self.leave(destination)

    # Do anything that needs to happen as we actually leave this map.
    def leave(self, destination):
        self.player.highlights = {}
        self.destination = destination

    # Call on the dark powers of the terrain generator.
    def generate_terrain(self):
        generator = self.layout(self.exits)
        cells, self.exits = generator.attempt()
        # TODO: Possibly checks for validity first
        # TODO: This is kind of backwards! We should be feeding this into the generator. C'est la vie.
        self.center = generator.center
        self.entry = self.center
        self.size = generator.size
        # Final step.
        self.populate(cells)

    # Take a provided dict of {pos : (other data)} and turn it into cell objects.
    def populate(self, cells):
        for pos, contents in cells.items():
            distance, terrain = contents # HACK: This won't always be a tuple like this.
            cell = Cell(pos, self)
            if terrain is not None:
                cell.put_terrain(terrain)

            # TODO: Replace this test code with something better.
            if random.randint(1, 10) == 1:
                for x in range(random.randint(1, 3)):
                    cell.put(generate_item(random.choice(("shortsword", "spear", "thrusting broadsword", "armor", "gloves", "boots", "leggings"))))

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
    # TODO: It's still awful. I'm scared to touch it because so much relies on it.
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
            obj.cell = cell
            cell.add(obj, terrain)

        return obj

    # Decides whether a position is a valid one.
    # TODO: Handle moving into nonexistent but cell-prototyped positions.
    def valid(self, pos):
        if self.cells.get(pos) is None:
            return False
        return True

    # Add a screen to self.screens, which will eventually result in it being displayed.
    def screen(self, screenname, arguments=None, screenclass=None):
        self.screens.append((screenname, arguments, screenclass))

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

# TODO: Move this into its own file.
class Cell:
    def __init__(self, pos, parent):
        self.map = parent
        self.pos = pos

        # Stuff inside the cell
        self.actor = None
        self.terrain = None
        self.items = {}

    # STUB
    def put_terrain(self, terrain):
        self.terrain = terrain
        terrain.cell = self

    # Return a glyph to display for this cell.
    # TODO: improve this function greatly
    def draw(self):
        if self.actor is not None:
            return self.actor.glyph, self.actor.color
        elif self.terrain is not None:
            return self.terrain.glyph, self.terrain.color
        elif len(self.items) == 1:
            return '?', 'magenta-black'
        elif len(self.items) > 1:
            return '!', 'magenta-black'
        else:
            return self.map.floor

    # TODO: Options for what to list.
    # TODO: This should go through the 'describe' functions; it should only be returning information, not strings!
    def contents(self):
        list = []
        if self.actor is not None:
            list.append("a %s" % self.actor.name)
        if self.terrain is not None:
            list.append("a %s" % self.terrain.name)
        if len(self.items) > 0:
            for appearance, itemlist in self.items.items():
                list.append(appearance)
        if not list:
            list.append("nothing of interest")
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
        return False

    # Return whether the cell has blocking terrain in it.
    def impassable(self):
        if self.terrain is not None:
            if self.terrain.blocking is True:
                return True
        return False

    # Return whether the cell is passable
    def blocked(self):
        if self.occupied() is True or self.impassable() is True:
            return True
        return False

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
