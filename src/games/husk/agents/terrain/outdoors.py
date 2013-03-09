from src.lib.objects.terrain import Terrain

# Meat Arena
class Corn(Terrain):
    def __init__(self, terrain_type=None):
        Terrain.__init__(self)
        self.name = "corn"
        self.glyph = "|"
        self.color = "yellow-black"