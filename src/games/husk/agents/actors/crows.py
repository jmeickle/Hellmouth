# Poor, defenseless humans.

from src.lib.agents.actors.npc import NPC

class Crow(NPC):

    def __init__(self):
        super(Crow, self).__init__()

        self.glyph = "C"
        self.name = 'crow'
        self.color = 'blue'
        self.description = "A dark shape flitting between the branches."

        self.loadouts = []
        self.generator = "slave"
        self.build(25)