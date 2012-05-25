from define import *

# Hit location
class HitLoc:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner

        # Combat stats
        self.HP = 0
        self.DR = 0
        self.wounds = []

        # Connectivity
        self.parent = None
        self.children = []
        self.sublocations = []

        # Item-related
        self.held = []
        self.readied = []
        self.worn = []

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
        self.held.append(item)
        item.held.append(self)

    def ready(self, item):
        self.readied.append(item)
        item.readied.append(self)

    def wear(self, item):
        self.worn.append(item)
        item.worn.append(self)

    def unhold(self, item):
        self.held.remove(item)
        item.held.remove(self)

    def unready(self, item):
        self.readied.remove(item)
        item.readied.remove(self)

    def unwear(self, item):
        self.worn.remove(item)
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

