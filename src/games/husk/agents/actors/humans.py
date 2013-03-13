# Poor, defenseless humans.

from src.lib.agents.actors.npc import NPC

class Human(NPC):

    def __init__(self):
        super(Human, self).__init__()

        self.glyph = '@'
        self.name = 'human'
        self.color = 'white'
        self.description = "A normal human."

        self.loadouts = []
        self.generator = "slave"
        self.build(25)