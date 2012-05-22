# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

from actor import Actor
import ai.astar

class NPC(Actor):
    def __init__(self):
        Actor.__init__(self)

        # AI-related properties.
        self.target = None

        self.ai = ai.astar.AStar()
        self.distance = None
        self.path = None

class MeatSlave(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow-black'
        self.hp = 1
        self.damage = 1

class MeatGolem(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue-black'
        self.hp = 50
        self.damage = 1

class MeatWorm(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta-black'
        self.hp = 20
        self.damage = 3

class MeatHydra(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta-black'
        self.hp = 80
        self.damage = 5
