"""Encounter scale map cells."""

from src.lib.agents.components.container import SectionedContainer
from src.lib.maps.cell import BaseCell

from src.lib.util import debug
from src.lib.util.trait import Trait, Traitable

@Trait.use(SectionedContainer)
class EncounterCell(BaseCell):
    """A partition of an EncounterMap."""
    __metaclass__ = Traitable

    def __init__(self, coords, parent):
        SectionedContainer.super(EncounterCell, self).__init__(sections=("actors", "items"))
        super(EncounterCell, self).__init__(coords, parent)

    @property
    def actors(self):
        return self.contents["actors"]

    @actors.setter
    def actors(self, value):
        self.contents["actors"] = value

    @property
    def items(self):
        return self.contents["items"]

    @items.setter
    def items(self, value):
        self.contents["items"] = value