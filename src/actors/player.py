# The player character(s).
from actor import Actor

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '@'
        self.name = 'adventurer'
        self.color = 'cyan'
        self.description = "Some hapless adventurer who stumbled across the arena. It looks pretty feeble."
        self.highlights = {}

        self.build(200)
        self.attributes["ST"] += 10
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
