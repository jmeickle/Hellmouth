# The player character(s).
from src.lib.agents.actors.player import PC
from src.lib.agents.components.commander import Commander, CommandingAgent

class Player(PC, CommandingAgent):
    """Default player."""
    def __init__(self, components=[Commander]):
        super(Player, self).__init__(components)
        self.glyph = 'T'
        self.name = 'scarecrow'
        self.color = 'yellow'
        self.description = "A tatterdemalion shape of straw and rags. And... skin?"
        self.highlights = {}

        self.points["traits"]["DX"] += 100
        self.points["traits"]["ST"] += 100
        self.build(200)
        self.recalculate()
        self.controlled = True