from define import *
from objects.items.item import Natural

# Hit location
class HitLoc:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner

        # Combat stats
        self.HP = 0
        self.DR = 0
        self.wounds = []
        self.attack_options = {}

        # Connectivity
        self.parent = None
        self.children = []
        self.sublocations = []

        # TODO: These will have to be inventories later.
        # Item-related
        self.held = {}
        self.readied = {}
        self.worn = {}

    # Return a list of unique items.
    def items(self):
        # DARK MAGIC
        items = set()

        for itemlist in self.held.values():
            items.update(itemlist)
        for itemlist in self.readied.values():
            items.update(itemlist)
        for itemlist in self.worn.values():
            items.update(itemlist)

        return items

    def weapons(self, natural=True, wielded=True, improvised=False):
        found_weapons = {}
        if natural is True:
            for appearance, weapons in self.attack_options.items():
                found_weapons[appearance] = weapons
        if wielded is True:
            for appearance, weapons in self.held.items():
                found_weapons[appearance] = weapons
        return found_weapons

    # Information about this location.
    def display(self):
        screen = []
        if len(self.attack_options) > 0:
            screen.append("%s:" % self.type)
            for weapon in self.attack_options.keys():
                screen.append("  %s" % weapon)# (%s)" % (weapon, object))
        return screen

    # Return the healthiness of the limb
    # TODO: Base these values on self.owner
    def status(self):
        if sum(self.wounds) > 15:    return SEVERED
        elif sum(self.wounds) >= 10: return CRIPPLED
        elif sum(self.wounds) > 4:   return INJURED
        elif sum(self.wounds) > 1:   return SCRATCHED
        else:                        return UNHURT

    # Set up a parent/child relationship.
    def add_child(parent, child):
        parent.children.append(child)
        child.parent = parent

    # Add a sublocation of this part.
    def sublocation(self, part):
        self.sublocations.append(part)

    # ITEMS
    def hold(self, item):
        held = self.held.get(item.appearance(), [])
        held.append(item)
        self.held[item.appearance()] = held
        item.held.append(self)

    def ready(self, item):
        readied = self.readied.get(item.appearance(), [])
        readied.append(item)
        self.readied[item.appearance()] = readied
        item.readied.append(self)

    def wear(self, item):
        worn = self.worn.get(item.appearance(), [])
        worn.append(item)
        self.worn[item.appearance()] = worn
        item.worn.append(self)

    def unhold(self, item):
        held = self.held.get(item.appearance(), [])
        held.remove(item)
        self.held[item.appearance()] = held
        item.held.remove(self)

    def unready(self, item):
        readied = self.readied.get(item.appearance(), [])
        readied.remove(item)
        self.readied[item.appearance()] = readied
        item.readied.remove(self)

    def unwear(self, item):
        worn = self.worn.get(item.appearance(), [])
        worn.remove(item)
        self.worn[item.appearance()] = worn
        item.worn.remove(self)

    # COMBAT

    # Add a wound to this location.
    def hurt(self, amt):
        self.wounds.append(amt)

    # Return a color for the limb status.
    def color(self):
        if self.status() == SEVERED:     return "white"
        elif self.status() == CRIPPLED:  return "magenta"
        elif self.status() == INJURED:   return "red"
        elif self.status() == SCRATCHED: return "yellow"
        else:                            return "green"

    # TODO: Move the limb glyph code here.

