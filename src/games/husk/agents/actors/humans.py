# Poor, defenseless humans.

from src.lib.agents.actors.npc import NPC

class Human(NPC):

    def __init__(self):
        super(MeatSlave, self).__init__()

        self.glyph = '@'
        self.name = 'human'
        self.color = 'blue'
        self.description = "A normal human."

        self.loadouts = []
        self.generator = "slave"
        self.build(25)