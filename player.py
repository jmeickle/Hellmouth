from actor import Actor

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '@'
        self.name = 'Player'
