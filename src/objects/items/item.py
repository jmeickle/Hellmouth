import random

# Items.
class Item():
    def __init__(self):
        # Flavor
        self.name = "debugger"
        self.description = "Debug description"

        # Basic characteristics
        self.size = None
        self.hp = None
        self.hp_max = None
        self.dr = None
        self.effects = None

        # Construction
        self.quality = None
        self.material = random.choice(("iron", "gold", "copper", "steel"))

        # References
        self.held = []
        self.readied = []
        self.worn = []

    # STUB: Figure out appearance here, based on provided precision options, statuses, etc.
    def appearance(self):
        return "%s %s" % (self.material, self.name)

    # STUB: Preferred slot for this kind of item.
    def preferred_slot(self):
        return 'RHand'

    # STUB: Hit an item.
    def hit(self):
        return False

    # STUB: Do damage to an item.
    def damage(self, amt):
        return False

    # Whether the item is intended to be used as a weapon. Note that
    # some objects, like torches or shields, fit into this category
    # despite not being 'weapon' objects.
    def can_be_weapon(self):
        return True

    # Whether this particular weapon needs to be held to be used. True for almost everything.
    def must_be_held(self):
        return True
	
    # Whether the item is intended to be worn. Note that some objects,
    # like bags, might be perfectly serviceable wearables without being
    # armor or clothing.
    def can_be_worn(self):
        return False

    # Return true if the item is held, or with optional loc parameter,
    # if the item is held by a specific location.
    def is_held(self, loc=None):
        if loc is None:
            if len(self.held) > 0:
                return True
        else:
            if held.count(loc) > 0:
                return True
        return False

    # Return true if the item is being readied, or with optional loc parameter,
    # if the item is readied by a specific location.
    def is_readied(self, loc=None):
        if loc is None:
            if len(self.readied) > 0:
                return True
        else:
            if readied.count(loc) > 0:
                return True
        return False

    # Return true if the item is being worn, or with optional loc parameter,
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
        self.primary_skill = None # Primary skill, for descriptions - there can be others.
        self.attacks = {} # Min ST in attackline

class Sword(Weapon):
    def __init__(self):
        Weapon.__init__(self)
