"""Encounter scale map."""

from src.lib.maps.map import BaseMap
from src.lib.maps.encounter.cell import EncounterCell

class EncounterMap(BaseMap):
    cell_class = EncounterCell