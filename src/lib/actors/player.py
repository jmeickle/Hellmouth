# The player character(s).
from actor import Actor
from src.lib.agents.components.equipment import Equipment
from src.lib.agents.components.manipulation import ManipulatingAgent
from src.lib.agents.components.status import Status

class Player(Actor, ManipulatingAgent):

    def __init__(self, components=[Equipment, Status]):
        super(Player, self).__init__(components)
        self.glyph = '@'
        self.name = 'adventurer'
        self.color = 'cyan'
        self.description = "Some hapless adventurer who stumbled across the arena. It looks pretty feeble."
        self.highlights = {}

        self.points["traits"]["DX"] += 100
        self.points["traits"]["ST"] += 100
        self.build(200)
        self.recalculate()
        self.controlled = True

    # Use stairs that you are standing on.
    def stairs(self):
        stairs = self.map.terrain(self.pos)
        if stairs is not None:
            return self.interact(stairs)

    # Interact with terrain.
    # TODO: Flags, etc.
    def interact(self, terrain):
        return terrain.interact(self)
