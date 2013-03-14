# Poor, defenseless humans.

from src.lib.agents.actors.npc import NPC
from src.lib.agents.components.faction import NeutralFaction

class Crow(NPC):
    """Default crow."""
    def __init__(self, components=[]):
        super(Crow, self).__init__(components)

        self.glyph = "C"
        self.name = 'crow'
        self.color = 'blue'
        self.description = "A dark shape flitting between the branches."

        self.loadouts = []
        self.generator = "wild"
        self.points["traits"]["DX"] += 40
        self.points["traits"]["ST"] -= 60
        self.build(5)
        self.recalculate()
        self.append_component(NeutralFaction(owner=self, controller=None))

    def get_movement_modes(self):
        yield "walk"
        yield "flight"