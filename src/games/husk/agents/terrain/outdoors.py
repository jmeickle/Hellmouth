from src.lib.agents.terrain.terrain import Terrain

class Corn(Terrain):
    def __init__(self, terrain_type=None):
        super(Corn, self).__init__()
        self.name = "row of corn"
        self.glyph = "|"
        self.color = "yellow-black"

    def can_block(self, agent, direction):
        if "flight" in agent.get_movement_modes():
            return False
        return True

class TrampledCorn(Terrain):
    def __init__(self, terrain_type=None):
        super(TrampledCorn, self).__init__()
        self.name = "section of trampled corn"
        self.glyph = ","
        self.color = "yellow-black"