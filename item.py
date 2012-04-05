import random

# Items.
class Item:
    def __init__(self):
        # Flavor
        self.name = "debugger"
        self.description = "Debug description"

        # Basic characteristics
        self.hp = None
        self.hp_max = None
        self.dr = None
        self.effects = None

        # Construction
        self.size = None
        self.quality = None
        self.material = random.choice(("iron", "gold", "copper", "steel"))

    # STUB: Figure out appearance here, based on provided precision options, statuses, etc.
    def appearance(self):
        return "%s %s" % (self.material, self.name)

    # STUB: Hit an item.
    def hit(self):
        return False

    # STUB: Do damage to an item.
    def damage(self, amt):
        return False

class Weapon(Item):
    def __init__(self):
        Item.__init__(self)

        # Combat-only stats
        self.skill = None # Primary skill, for descriptions - there can be others.
        self.attackline = {} # Min ST in attackline
