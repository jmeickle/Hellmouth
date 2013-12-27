"""A Cell is a partition of a Map. Like Maps, there can be Cells of different
scales, such as an overworld Cell containing an encounter Map."""

import random

from src.lib.util.geometry.hexagon import Hexagon
from src.lib.util.text import *

class BaseCell(object):
    """An abstract partition of a Map."""
    
    def __init__(self, coords, parent):
        self.coords = coords
        self.map = parent
        self.terrain = None

    # TODO: Multiple terrain
    # TODO: WHAT.
    def get_terrain(self):
        """Return terrain inside of a cell."""
        if self.terrain:
            return [self.terrain]
        else:
            return []

    def can_position(self, agent):
        """Return whether this cell is a valid position for an `Agent`."""
        return True