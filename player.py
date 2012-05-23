# The player character(s).
from actor import Actor

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '@'
        self.name = 'player character'
        self.color = 'cyan-black'
        self.hp = 100
        self.damage = 1
        self.build(150)
        self.controlled = True
        self.location = None
