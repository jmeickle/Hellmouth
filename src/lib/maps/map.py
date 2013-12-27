"""A Map defines an area of game space in which the primary interactions are
quantized actions (most commonly, movement). It is the canonical representation
of a portion of the game's 'reality', and it is responsible for managing all
gameplay occurring within its scope.

Maps typically quantize time into a turn or energy system and quantize space
into Cells.

Maps can be of different scales. The most typical scales are:

    * Encounter: a 'combat map' with one Actor per Cell
    * Location: a 'site map' with one 'band' or 'patrol' of Actors per Cell
    * Region: a 'country map' with one Location per Cell
    * World: a 'zoomed out' world map with one Region per Cell
"""
from collections import deque

from src.lib.maps.cell import BaseCell

from src.lib.util import debug
from src.lib.util.geometry.space import Point
from src.lib.util.log import Log
from src.lib.util.queue import Queue
from src.lib.util.text import *

from src.lib.data import screens

class MapException(Exception):
    pass

class InvalidCellException(MapException):
    pass

class BaseMap(object):
    """An area of game space partitioned into Cells."""

    cell_class = BaseCell

    def __init__(self, level, map_id):
        # Maps don't make sense without an associated Level.
        # TODO: (not actually true, what about generating a ton of levels to compare?)
        self.level = level

        # Use the provided map ID (~depth).
        self.map_id = map_id

        # Display information.
        self.name = None

        # # Map generation parameters.
        # self.layout = None
        # self.size = None
        # self.center = None
        # self.passages = None
        # self.depth = None
        # self.entry = None # Player start point. TODO: Replace by bidirectional stairs!

        # Dict of (hex) cell objects, indexed by pos.
        self.cells = {}

        # # Default information if a cell doesn't exist.
        # # TODO: Expand!
        # self.floor = None

    def get_controller(self):
        """Return the Actor serving as primary controller in this Map."""
        return self.level.get_controller()

    """Map arrival methods."""

    # By default, before_arrive tries to load the matching screen and plugs in a
    # callback to self.arrive. Otherwise, it calls it itself.
    def before_arrive(self, entrance_id, exit_id):
        entryscreen = self.level.name
        if self.name is not None:
            entryscreen  += ", " + self.name # HACK: Later it should choose different dict for different levels.
        Log.add("You enter %s's %s." % (self.level.name, self.name))

    def arrive(self, entrance_id, exit_id):
        for passage_id, passage_obj in self.get_passages():
            self.get_controller().highlights[passage_id] = passage_obj

    def arriving_actor(self, actor, entrance_id, exit_id):
        passage = self.get_passage(entrance_id)

        try:
            self.relocate(actor)
        except Exception, e:
            raise MapException("Couldn't relocate:" + "\n".join([str(_) for _ in (self, actor, entrance_id, exit_id, passage.coords)]))

        if not self.reposition(actor, passage.coords):
            raise MapException("Couldn't place:\n" + "\n".join([str(_) for _ in (self, actor, entrance_id, exit_id, passage.coords)]))

    """Map departure methods."""

    def before_depart(self, map_id, entrance_id, exit_id):
        """Do anything that needs to happen before leaving this Map."""
        pass

    def depart(self, map_id, entrance_id, exit_id):
        """Do anything that needs to happen as we actually leave this Map."""
        self.get_controller().highlights = {}

    def departing_actor(self, actor, map_id, entrance_id, exit_id):
        pass

    """Map passage methods."""

    def get_passage(self, passage_id):
        """Return a passage from a passage ID."""
        return self.layout.passages.get(passage_id)

    def get_passages(self):
        """Return an iterator over all passages."""
        return self.layout.passages.items()

    def add_cell(self, coords):
        """Create a Cell, store it within this map, and return it."""
        assert isinstance(coords, Point), "Tried to non-Point here"
        cell = self.cell_class(coords, self)
        self.cells[coords] = cell
        return cell

    # Return a cell at a pos tuple.
    def cell(self, pos):
        return self.cells.get(pos)

    def can_locate(self, agent):
        """Return whether this map is a valid location for an `Agent`."""
        return True

    def relocate(self, agent):
        """Attempt to relocate an `Agent` to this map."""
        if not self.can_locate(agent):
            raise Exception

        # Set the Agent's location.
        agent.location = self

    def reposition(self, agent, coords):
        """Attempt to reposition an `Agent` to a set of coordinates on this map."""
        # TODO: Change to raise exceptions for various types of placement failures.
        assert hasattr(agent, "coords"), "Tried to reposition a non-positionable Agent {}.".format(agent)
        assert isinstance(coords, Point), "Tried to reposition an Agent {} into a non-Point position {}.".format(agent, coords)
        cell = self.cells.get(coords)

        if not cell:
            raise InvalidCellException, "Tried to reposition an Agent {} into an invalid cell at coordinates {}.".format(agent, coords)

        if not cell.can_position(agent):
            raise MapException

        # Store the Agent in the cell and set its position.
        agent.cell = cell
        return True

    def place_actor(self, actor, coords):
        """Place an `Actor` on this `Map`."""
        try:
            if not self.cell(coords).can_contain(actor):
                return False
        except AttributeError as e:
            debug.die((e, dir(self.cell(coords))))

        self.relocate(actor)
        self.reposition(actor, coords)

        Queue.add(actor)

    def place_terrain(self, terrain, coords):
        if self.cell(coords).get_terrain():
            return False

        self.relocate(terrain)
        self.reposition(terrain, coords)

    def remove_actor(self, actor):
        """Remove an Actor from this Map."""
        actor.cell().remove(actor)
        # TODO: more of a callback approach
        self.level.remove_actor(actor)

    # Decides whether a position is a valid one.
    # TODO: Handle moving into nonexistent but cell-prototyped positions.
    def valid(self, pos):
        if self.cells.get(pos) is None:
            return False
        return True

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