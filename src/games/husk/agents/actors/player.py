# The player character(s).
from src.lib.agents.actors.player import PC
from src.lib.agents.components.equipment import Equipment
from src.lib.agents.components.manipulation import ManipulatingAgent
from src.lib.agents.components.status import Status

class Player(PC):

    def __init__(self):
        super(Player, self).__init__()
        self.glyph = '@'
        self.name = 'scarecrow'
        self.color = 'yellow'
        self.description = "A tatterdemalion shape of straw and rags. And... skin?"
        self.highlights = {}

        self.points["traits"]["DX"] += 100
        self.points["traits"]["ST"] += 100
        self.build(200)
        self.recalculate()
        self.controlled = True