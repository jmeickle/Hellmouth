# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

from actor import Actor
import ai.astar

class NPC(Actor):
    def __init__(self):
        Actor.__init__(self)

        # TODO: Make an AI class.

        # AI-related properties.
        self.target = None

        self.ai = ai.astar.AStar()
        self.destination = None
        self.distance = None
        self.path = None

        self.attempts = 0

class MeatSlave(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow-black'
        self.description = "A pitiful wretch who long ago abandoned all hope of escaping the arena. It has covered itself in lunchmeat to hide its scent from the other occupants."

        self.damage = 1
        self.build(5)

class MeatGolem(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue-black'
        self.description = "A lumbering construct made of a great many pieces of spoiled meat. They appear to have been stapled together."

        self.damage = 1
        self.build(50)

class MeatWorm(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta-black'
        self.description = "These worms look like large sticks of pepperoni. A trail of grease glistens behind them."

        self.damage = 3
        self.build(10)

class MeatHydra(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta-black'
        self.description = 'A hydra made from the meat of lesser beings. Each "head" is a cracked ribcage.'

        self.damage = 5
        self.build(50)
