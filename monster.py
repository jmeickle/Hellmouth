from actor import Actor
import ai.astar

class Monster(Actor):
    def __init__(self):
        Actor.__init__(self)

        # Set up AI stuff
        self.ai = ai.astar.AStar()
        self.path = None
        self.target = None
        self.distance = None

class MeatSlave(Monster):
    def __init__(self):
        Monster.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow-black'
        self.hp = 1
        self.damage = 1

class MeatGolem(Monster):
    def __init__(self):
        Monster.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue-black'
        self.hp = 50
        self.damage = 1

class MeatWorm(Monster):
    def __init__(self):
        Monster.__init__(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta-black'
        self.hp = 20
        self.damage = 3

class MeatHydra(Monster):
    def __init__(self):
        Monster.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta-black'
        self.hp = 80
        self.damage = 5
