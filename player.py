from actor import Actor

class Player(Actor):
    def __init__(self):
        Actor.__init__(self, 0, 0)
        self.hp = 1
        self.glyph = '@'
        self.map = None
