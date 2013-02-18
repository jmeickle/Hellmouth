# Terrain objects.

from src.lib.agents.agent import Agent

class Terrain(Agent):
    def __init__(self, terrain_type=None):
        self.cell = None
        self.name = None
        self.color = None
        self.glyph = None
        self.blocking = True
        self.terrain_type = terrain_type

    # Do additional setup based on the provided terrain type.
    def setup(self):
        return False

    # What the terrain does when an actor interacts with it.
    def interact(self, actor):
        return False

# Generic staircase class.
class Stairs(Terrain):
    def __init__(self, which, destination):
        Terrain.__init__(self)
        self.name = "staircase " + which
        self.destination = destination
        self.glyph = ">"
        self.color = "green-black"
        self.blocking = False

    def react_on_use(self, user):
        self.cell.map.go(self.destination)
        return True

# Generic lever class.
class Lever(Terrain):
    def __init__(self, target):
        Terrain.__init__(self)
        self.name = "lever"
        self.target = target
        self.glyph = "|"
        self.color = "magenta-black"
        self.blocking = False

    def react_on_do_use(self, user):
        self.cell.map.go(self.destination)
        return True

# Meat Arena
class MeatWall(Terrain):
    def __init__(self, terrain_type=None):
        Terrain.__init__(self)
        self.name = "meat wall"
        self.glyph = "X"
        self.color = "red-black"
        self.setup(terrain_type)

    def setup(self, terrain_type):
        if terrain_type == 'inner':
            self.color = "yellow-black"
            self.name = "inner " + self.name

# Caves
class CaveWall(Terrain):
    def __init__(self, terrain_type=None):
        Terrain.__init__(self)
        self.name = "rough-hewn cave wall"
        self.glyph = "#"
        self.color = "yellow-black"
