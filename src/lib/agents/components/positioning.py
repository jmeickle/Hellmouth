"""Provides functionality for Agents to be positioned on a map."""

from src.lib.agents.components.component import Component

from src.lib.util.geometry.space import Point
from src.lib.util.trait import Trait

"""Traits."""

# TODO: Multi-position creatures.
class Positionable(Trait):
    """Provides methods to manage coordinate position on a grid."""
    # Default to a blank position.
    position = Point()

    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's position."""
        Trait.super(Positionable, self).__init__(*args, **kwargs)
        self.position = kwargs.pop("cell", self.position)

    @Trait.include
    def __repr__(self):
        return "%s@%s" % (self.appearance(), self.coords)

    @property
    def coords(self):
        """Return self's coordinate position."""
        return self.position

    @coords.setter
    def coords(self, value):
        """Set self's coordinate position."""
        assert isinstance(value, Point), "Tried to set a non-Point as coordinate position: {}".format(value)
        self.position = value

    def distance(self, target):
        """Return the distance from self to a target using their coordinate positions."""
        return self.metric.distance(self.position, target.position)

# TODO: Multi-cell creatures.
class CellPositionable(Positionable):
    """Provides methods to manage cell position on a map."""
    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's position."""
        Trait.super(CellPositionable, self).__init__(*args, **kwargs)
        if not self.cell and "cell" in kwargs:
            self.cell = kwargs.pop("cell")

    @property
    def cell(self):
        """Return the cell at self's position within self's location."""
        return self.location.cell(self.coords) if self.location else None

    @cell.setter
    def cell(self, value):
        """Set self's position to that of a cell within self's location."""
        self.coords = value.coords

class SubcellPositionable(CellPositionable):
    """Provides methods to manage subcell position within a cell."""
    subcell = None

    @Trait.include
    def __init__(self, *args, **kwargs):
        """Set self's subcell position."""
        Trait.super(SubcellPositionable, self).__init__(*args, **kwargs)
        self.subcell = kwargs.pop("subcell", subcell)