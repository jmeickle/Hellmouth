# The map and cells in the map.
# TODO: Not cells in the map.
from collections import deque

from src.lib.data import screens
from cell import Cell

from src.lib.util.debug import debug
from src.lib.util.text import *
from src.lib.util.log import Log
from src.lib.util.queue import Queue

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

        # Where we're traveling to.
        self.destination = None

    # The map portion of the game loop.
    def loop(self):
        # Don't continue looping if we have a destination.
        if self.destination is not None:
            return False

        actor = Queue.get_acting()

        if actor and not actor.controlled and actor.before_turn():
            actor.act()

    # Go to another map, or if destination is False, let the level figure it out.
    def go(self, destination):
        self.before_leave(destination)

    # By default, before_arrive tries to load the matching screen and plugs in a
    # callback to self.arrive. Otherwise, it calls it itself.
    def before_arrive(self):
        entryscreen = self.level.name
        if self.name is not None:
            entryscreen  += ", " + self.name # HACK: Later it should choose different dict for different levels.
        Log.add("You enter %s's %s." % (self.level.name, self.name))
        if screens.text.get(striptags(entryscreen)) is not None:
            arguments = {"header_right" : entryscreen, "footer_text" : screens.footer, "callback" : self.arrive}
            self.screen(striptags(entryscreen), arguments)
        else:
            return self.arrive()

    # Handle arriving at the map.
    def arrive(self):
        self.player.map = self
        self.put(self.player, self.entry)
        self.player.trigger("spawned")
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

    # Return a list of actors at a pos tuple.
    def actors(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return []
        else:
            return cell.actors

    # Return terrain at a pos tuple.
    def terrain(self, pos):
        cell = self.cell(pos)
        if cell is None:
            return None
        else:
            return cell.terrain

    # TODO: FIGURE OUT THIS SECTION, WHAT THE FUCK
    # TODO: It's still awful. I'm scared to touch it because so much relies on it.
    # Place an object (either agent or terrain) on the map.
    def put(self, obj, pos, terrain=False):

        cell = self.cells.get(pos)

        if not cell:
            return False

        if terrain is False:
            if cell.occupied():
                return False
            # Update the map
            cell.add(obj, terrain)
            Queue.add(obj)

            # Update the actor
            obj.pos = pos
            obj.map = self
            obj.ready()

        else:
            if cell.get_terrain():
                return False
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

    # TODO: Move to a file output util file.
    # # Print a large text version of the map.
    # def dump(self, size=100, origin=(0,0)):
    #     import sys
    #     print "Map of %s:\n" % self.name
    #     for y in range(-size, size):
    #         line = ""
    #         blank = True
    #         for x in range(-size, size):
    #             if x % 2 == 0:
    #                 line += " "
    #                 continue
    #             cell = self.cell(((x-y)/2,y))
    #             if cell is None:
    #                 glyph = " "
    #             else:
    #                 glyph = cell.glyph
    #                 blank = False
    #             line += glyph
    #         if blank is False:
    #             sys.stdout.write(line)
    #             sys.stdout.write("\n")
    #     exit()