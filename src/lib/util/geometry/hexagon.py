"""Define the geometry of hexagons.

This module expands the terminology guides in `src.lib.util.geometry.space` 
and `src.lib.util.geometry.shape` with some definitions specific to hexagons:

_heading_: One of the six cardinal hexagonal directions. These are represented
as the points at a distance of 1 from the coordinate system's origin (0, 0):

       NW    NE
         /  \
     CW | CC | CE
         \  /
       SW    SE


_rank_: The 'radius' of a set of hexagons. Given a set of hexagons and an origin 
within it, the rank is the greatest distance observed.

_pole_: Given an origin, rank, and heading, the hexagon that would be reached by 
traveling along a heading until reaching that rank.

_index_: Given an origin, rank, heading, and rotation, an enumeration of the 
order in which hexagons at that rank are visited.
"""

from src.lib.util.geometry.shape import Shape
from src.lib.util.geometry.space import *

class Hexagon(Shape):
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
    heading_names = {
        NW: "Northwest",
        NE: "Northeast",
        CE: "East",
        SE: "Southeast",
        SW: "Southwest",
        CW: "West"
    }

    def __init__(self, pos):
        assert False, "Tried to instantiate an abstract Hexagon."

    def __repr__(self):
        return "<%s[%s]>" % (self.__class__.__name__, self.pos)
