# Terrain objects.

class Terrain():
    def __init__(self, terrain_type=None):
        self.name = None
        self.color = None
        self.glyph = None
        self.blocking = True
        self.terrain_type = terrain_type

    # Do additional setup based on the provided terrain type.
    def setup():
        return False

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
