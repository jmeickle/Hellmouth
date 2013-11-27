"""Immobile (usually!) Agents with a wide variety of roles."""

from src.lib.agents.agent import Agent
from src.lib.agents.components.location import Locatable
from src.lib.agents.components.positioning import CellPositionable

from src.lib.util.log import Log
from src.lib.util.trait import Trait

@Trait.use(Locatable, CellPositionable)
class Terrain(Agent):
    def __init__(self, terrain_type=None):
        Locatable.super(Agent, self).__init__()
        CellPositionable.super(Agent, self).__init__()
        super(Terrain, self).__init__()

        self.name = None
        self.color = None
        self.glyph = None
        self.terrain_type = terrain_type

    # Do additional setup based on the provided terrain type.
    def setup(self):
        return False

    def can_block(self, agent, direction):
        """Return whether this cell can block an Agent coming from a direction."""
        return False

class Wall(Terrain):
    """Base class for artificial constructions."""
    def __init__(self, terrain_type=None):
        super(Wall, self).__init__()
        self.name = "wall"
        self.glyph = "#"
        self.color = "yellow-black"

    def can_block(self, agent, direction):
        return True

class EastWestWall(Wall):
    def __init__(self, terrain_type=None):
        super(EastWestWall, self).__init__()
        self.name = "wall"
        self.glyph = "|"
        self.color = "yellow-black"

    def can_block(self, agent, direction):
        return True

class NorthSouthWall(Wall):
    def __init__(self, terrain_type=None):
        super(NorthSouthWall, self).__init__()
        self.name = "wall"
        self.glyph = "-"
        self.color = "yellow-black"

    def can_block(self, agent, direction):
        return True

# Meat Arena
class MeatWall(Wall):
    def __init__(self, terrain_type=None):
        super(MeatWall, self).__init__()
        self.name = "meat wall"
        self.glyph = "X"
        self.color = "red-black"
        self.setup(terrain_type)

    def setup(self, terrain_type):
        if terrain_type == 'inner':
            self.color = "yellow-black"
            self.name = "inner " + self.name

# Caves
class CaveWall(Wall):
    def __init__(self, terrain_type=None):
        super(CaveWall, self).__init__()
        self.name = "rough-hewn cave wall"
        self.glyph = "#"
        self.color = "yellow-black"

class Window(Terrain):
    def __init__(self, terrain_type=None):
        super(Window, self).__init__()
        self.name = "window"
        self.glyph = "|"
        self.color = "cyan-black"

    def can_block(self, agent, direction):
        return True

class DirtRoad(Terrain):
    def __init__(self, terrain_type=None):
        super(DirtRoad, self).__init__()
        self.name = "dirt road"
        self.glyph = "~"
        self.color = "yellow-black"