# The player character(s).
from src.lib.agents.actors.actor import Actor
from src.lib.agents.components.commander import Commander, CommandingAgent

class Player(Actor, CommandingAgent):
    """Default player."""
    def __init__(self, components=[Commander]):
        super(Player, self).__init__(components)
        self.glyph = 'T'
        self.name = 'scarecrow'
        self.color = 'yellow'
        self.description = "A tatterdemalion shape of straw and rags. And... skin?"
        self.highlights = {}

        self.generator = "scarecrow"
        self.build(100)
        self.recalculate()
        self.controlled = True