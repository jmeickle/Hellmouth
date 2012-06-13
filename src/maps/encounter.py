# The map and cells in the map.
# TODO: Not cells in the map.
from collections import deque
import hex
from text import *
from data import screens
import log
from maps.cell import Cell

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
        if self.acting is not None:
            if self.acting.controlled is False:
                self.acting.act()

    # Go to another map, or if destination is False, let the level figure it out.
    def go(self, destination):
        self.before_leave(destination)

    # By default, before_arrive tries to load the matching screen and plugs in a
    # callback to self.arrive. Otherwise, it calls it itself.
    def before_arrive(self):
        entryscreen = self.level.name
        if self.name is not None:
            entryscreen  += ", " + self.name # HACK: Later it should choose different dict for different levels.
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
            obj.ready()

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
