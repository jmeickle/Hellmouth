# Derived from the Actor class, NPCs:
# 1) Do not check keyin
# 2) Have AI to control them
# 3) Do need any interface niceties (e.g., figuring out item letters)

from actor import Actor
import ai.astar
from hex import *

class NPC(Actor):
    def __init__(self):
        Actor.__init__(self)

        # TODO: Make an AI class.

        # AI-related properties.
        self.target = None

        self.astar = None
        self.destination = None
        self.distance = None
        self.path = False

        self.attempts = 0

    # AI actions. Currently: move in a random direction.
    def act(self):
        assert self.controlled is not True, "A player-controlled actor tried to hit AI code."

        self.attempts += 1
        if self.attempts > 10:
            self.over()
            return False

        self.distance = dist(self.pos, self.target.pos)
        repath = False

        # TODO: Refactor some of this so that it is less buggy, but for now, it kinda-sorta-works.
        if self.distance > 1 and self.path is False:
            repath = True
        if self.destination != self.target.pos:
            if random.randint(1, dist(self.destination, self.target.pos)) == 1:
                repath = True

        # TODO: More intelligently decide when to re-path
        if repath is True:
            # TODO: Get target stuff in here.
            if self.target is not None:
                self.destination = self.target.pos
                self.repath()

        if self.distance > 1 and self.path is not False:
            if self.path: # i.e., a list with entries
                pos = self.path.pop()
                dir = sub(pos, self.pos)
                if not self.do(dir):
                    # Chance to flat out abandon the path
                    if r1d6() == 6:
                        self.path = False
                    else:
                        # Try again
                        self.path.append(pos)
            else:
                self.path = False # Remove the empty list

        # This should only happen if stuff is adjacent and without a path.
        else:
            dir = sub(self.target.pos, self.pos)
            self.do(dir)

    # Reset A* and generate a new path.
    def repath(self):
        self.astar = ai.astar.AStar(self.map)
        self.path = self.astar.path(self.pos, self.destination)

# Monster definitions. TODO: Move elsewhere.

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
