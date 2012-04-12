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

        # References
        self.held = []
        self.worn = []

    # STUB: Figure out appearance here, based on provided precision options, statuses, etc.
    def appearance(self):
        return "%s %s" % (self.material, self.name)

    # STUB: Hit an item.
    def hit(self):
        return False

    # STUB: Do damage to an item.
    def damage(self, amt):
        return False

    # STUB: Return true/false, based on whether it's a wielded item (weapon, torch, tool, etc.)
    def wielded(self):
        return False

    # Return true if the item is being held, or with optional item parameter,
    # if the item is held by a specific location.
    def is_held(self, loc=None):
        if loc is None:
            if len(self.held) > 0:
                return True
        else:
            if held.count(loc) > 0:
                return True
        return False

    # Return true if the item is being worn, or with optional item parameter,
    # if the item is worn by a specific location.
    def is_worn(self, loc=None):
        if loc is None:
            if len(self.worn) > 0:
                return True
        else:
            if worn.count(loc) > 0:
                return True
        return False

class Weapon(Item):
    def __init__(self):
        Item.__init__(self)

        # Combat-only stats
        self.skill = None # Primary skill, for descriptions - there can be others.
        self.attackline = {} # Min ST in attackline

    def wielded(self):
        return True
