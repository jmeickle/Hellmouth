from actor import Actor

class Player(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '@'
        self.name = 'Player'
        self.color = 'cyan-black'

# NOT THE PLAYER BUT GOES IN HERE ANYWAYS

class MeatSlave(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow-black'
        self.hp = 1

class MeatGolem(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue-black'
        self.hp = 50

class MeatWorm(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta-black'
        self.hp = 20

class MeatHydra(Actor):
    def __init__(self):
        Actor.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta-black'
        self.hp = 80
