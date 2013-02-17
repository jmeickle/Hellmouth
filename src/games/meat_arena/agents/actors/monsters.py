# MEAT ARENA's monster definitions.
#
# TODO: Define these with json rather than Python code.

from src.lib.actors.npc import NPC

class MeatSlave(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'meat slave'
        self.color = 'yellow'
        self.description = "A pitiful wretch who long ago abandoned all hope of escaping the arena. It has covered itself in lunchmeat to hide its scent from the other occupants."

        self.loadouts = ["light armor", "knives"]
        self.generator = "slave"
        self.build(25)

class MeatGolem(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '8'
        self.name = 'meat golem'
        self.color = 'blue'
        self.description = "A lumbering construct made of a great many pieces of spoiled meat. They appear to have been stapled together."
        self.voice = None
        self.generator = "wild"
        self.build(50)

    # HACK: To be removed when the advantage works.
    def DR(self):
        return 3

class MeatWorm(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.body = body.Vermiform(self)
        self.glyph = '~'
        self.name = 'meat worm'
        self.color = 'magenta'
        self.description = "This worm looks like a large stick of pepperoni. A trail of grease glistens behind it."
        self.voice = "screech"

        self.generator = "wild"
        self.build(10)

class MeatHydra(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'D'
        self.name = 'meat hydra'
        self.color = 'magenta'
        self.description = 'A hydra made from the meat of lesser beings. Each "head" is a cracked ribcage.'
        self.voice = "roar"

        self.generator = "wild"
        self.build(50)

class MeatCommander(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = 'C'
        self.name = 'Meat Commander'
        self.color = 'magenta'
        self.description = "This beefy champion wears a full set of bone armor decorated with dozens of veal medallions and bacon ribbons. A crown roast rests atop its noble brow."

        self.generator = "elite"
        self.build(700)
        self.loadouts = ["heavy weapon", "heavy armor"]

class Sauceror(NPC):
    def __init__(self):
        NPC.__init__(self)
        self.glyph = '@'
        self.name = 'Sauceror'
        self.color = 'magenta'
        self.description = "A slight figure clad in dark cloth robes. Its flesh is pale and unappetizing, but its brain is perhaps the meatiest of all."

        self.generator = "sauceror"
        self.build(400)