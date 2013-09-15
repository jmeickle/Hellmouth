"""Geometry for hexagons."""

from src.lib.util.geometry import *

class Hexagon(object):
    """Class for hexagonal shape."""

    # Number of edges
    edges = 6

    # No location
    ANYWHERE = None

    # Center
    CC = Point(0, 0)

    # Northwest
    NW = Point(0, -1)
    # Northeast
    NE = Point(1, -1)
    # East
    CE = Point(1, 0)
    # Southeast
    SE = Point(0, 1)
    # Southwest
    SW = Point(-1, 1)
    # West
    CW = Point(-1, 0)

    # List of headings
    headings = [NW, NE, CE, SE, SW, CW]
    heading_names = {}

    def __init__(self, pos):
        assert False, "Tried to instantiate an abstract Hexagon."

    def __repr__(self):
        return "<%s[%s]>" % (self.__class__.__name__, self.pos)
