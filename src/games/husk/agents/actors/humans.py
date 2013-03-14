# Poor, defenseless humans.

from src.lib.agents.actors.npc import NPC
from src.lib.agents.components.faction import EnemyFaction

class Human(NPC):
    """Default human enemy."""
    def __init__(self, components=[]):
        super(Human, self).__init__(components)

        self.glyph = '@'
        self.name = 'human'
        self.color = 'white'
        self.description = "A normal human."

        self.loadouts = []
        self.generator = "farmer"
        self.build(50)
        self.recalculate()
        self.append_component(EnemyFaction(owner=self, controller=None))