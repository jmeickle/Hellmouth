from define import *
from objects.items.item import Natural

# Hit location
class HitLoc:
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner

        # Combat stats
        self.hp = 0
        self.dr = 0
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

    def appearance(self):
        return hit_locations.get(self.type)

    def severed(self):
        if self.status() == SEVERED:
            return True
        if self.parent is not None:
            return self.parent.severed()
        else:
            return False

    def descendants(self):
        descendants = [self]
        if self.children:
            for child in self.children:
                descendants.extend(child.descendants())
        return descendants

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
        # HACK: Not all natural attacks will be blocked like this!
        if natural is True and len(self.readied) == 0:
            for appearance, weapons in self.attack_options.items():
                found_weapons[appearance] = weapons
        if wielded is True:
            for appearance, weapons in self.readied.items():
                found_weapons[appearance] = weapons
        return found_weapons

    # Information about this location.
    def display(self):
        screen = []
        screen.append("%s:" % self.type)
        for k, v in self.worn.items():
            screen.append(k)
        for k, v in self.held.items():
            screen.append(k)
        for k, v in self.readied.items():
            screen.append(k)
        if len(self.attack_options) > 0:
            for weapon in self.attack_options.keys():
                screen.append("  %s" % weapon)# (%s)" % (weapon, object))
        return screen

    # Return the healthiness of the limb
    # TODO: Base these values on self.owner
    def status(self):
        if sum(self.wounds) > 10:    return SEVERED
        elif sum(self.wounds) >= 6:  return CRIPPLED
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
    # STUB: Can we hold the item?
    def can_hold(self, item):
        if len(self.held) > 0:
            return False
        return True

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
        held = self.held.pop(item.appearance(), [])
        held.remove(item)
        if held:
            self.held[item.appearance()] = held
        item.held.remove(self)

    def unready(self, item):
        readied = self.readied.pop(item.appearance(), [])
        readied.remove(item)
        if readied:
            self.readied[item.appearance()] = readied
        item.readied.remove(self)

    def unwear(self, item):
        worn = self.worn.pop(item.appearance(), [])
        worn.remove(item)
        if worn:
            self.worn[item.appearance()] = worn
        item.worn.remove(self)

    # COMBAT
    def hit(self, attack, reciprocal=False):
        if reciprocal is False:
            attack["damage blocked"] = self.DR()
            self.reciprocal(attack)
        else:
            attack["reciprocal damage blocked"] = self.DR()

    def DR(self):
        dr = 0
        # HACK: Use all items!
        import random
        for appearance, itemlist in self.worn.items():
            item = random.choice(itemlist)
            dr += item.dr
        dr += self.dr + self.owner.DR()
        return dr

    # TODO: Locational and actor spikes
    def reciprocal(self, attack):
        # HACK: Use all items!
        import random
        if len(self.worn) > 0:
            for appearance, itemlist in self.worn.items():
                item = random.choice(itemlist)

            spikes = item.spikes()
            if spikes is not None:
                attack["reciprocal damage rolled"] = dice(spikes)


    def multiplier(self, attack):
        multipliers = {"cut" : 1.5, "imp" : 2}
        attack["multiplier"] = multipliers.get(attack["damage type"], 1)

    # Add a wound to this location.
    def hurt(self, amt):
        self.wounds.append(amt)

    # Return a color for the limb status.
    def color(self):
        if self.severed() is True:       return "black"
        elif self.status() == CRIPPLED:  return "magenta"
        elif self.status() == INJURED:   return "red"
        elif self.status() == SCRATCHED: return "yellow"
        else:                            return "green"

    # TODO: Move the limb glyph code here.
