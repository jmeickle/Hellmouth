# Terrain objects.

class Terrain():
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

# Meat Arena
class Stairs(Terrain):
    def __init__(self, which, destination):
        Terrain.__init__(self)
        self.name = "staircase " + which
        self.destination = destination
        self.glyph = ">"
        self.color = "black-red"
        self.blocking = False

    def interact(self, actor):
        self.cell.map.travel = self.destination
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
