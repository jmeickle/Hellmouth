from define import *
from objects.items.item import Natural
from objects.items.carrion import PartialCorpse

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

        # A layer can have multiple items (like several rings).
        self.layers = [[]]

    def appearance(self):
        return hit_locations.get(self.type)

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

    # Calculate what happens when a limb is hit, but don't actually apply the
    # effects, in order to handle simultaneous actions.
    def hit(self, attack):
        # TODO: (Source, DR blocked) for messaging
        # TODO: Damage to items.
        # TODO: Min damage properly
        attack["basic damage blocked"] = self.DR()
        attack["penetrating damage"] = max(0, attack["basic damage"] - attack["basic damage blocked"])
        attack["multiplier"] = self.multiplier(attack["damage type"])
        # No wound is necessarily no injury.
        if attack["penetrating damage"] <= 0:
            attack["wound"] = 0
            attack["injury"] = 0
        else:
            # Wounds are always at least one damage, but they may not cause injury.
            attack["wound"] = max(1, int(attack["penetrating damage"] * attack["multiplier"]))

            # Any hit location can suffer a major wound.
            if attack["wound"] > self.owner.MaxHP()/2:
                attack["major wound"] = True

            # Less complicated case.
            if self.crippling() is False:
                attack["injury"] = attack["wound"]

            # More complicated case: some hit locations can be crippled.
            else:
                if attack["wound"] > self.crippling():
                    attack["major wound"] = True
                    attack["crippled"] = True
                    attack["crippling major wound"] = True
                    if attack["wound"] > 2*self.crippling():
                        attack["dismembered"] = True
                        attack["dismembering major wound"] = True

                # Further damage to a crippled limb causes wounds - but it
                # doesn't cause further injury over the crippling amount!
                if self.crippled() is True:
                    attack["injury"] = 0

                # Cap damage based on max crippling damage, then figure out
                # if this attack caused crippling or dismemberment.
                else:
                    attack["injury"] = min(attack["wound"] + sum(self.wounds), 1 + self.crippling()) - sum(self.wounds)

                    # If the wound itself wouldn't have caused crippling, but
                    # it's pushed the limb over the edge to become crippled:
                    if attack["wound"] + sum(self.wounds) > self.crippling():
                        attack["crippled"] = True

                    # Likewise, but for dismemberment.
                    if attack["wound"] + sum(self.wounds) > 2*self.crippling():
                        attack["dismembered"] = True
                        if attack["damage type"] == "cut":
                            attack["severed"] = True

#            if attack["location"].severed() is True:
#                self.screen("ouch!", {"body_text" : self.limbloss(attack)})

    # TODO: Make this a display-only function, not for handling damage done.
    def DR(self):
        dr = 0
        # HACK: Use all items!
        import random
        for appearance, itemlist in self.worn.items():
            item = random.choice(itemlist)
            dr += item.dr
        dr += self.dr + self.owner.DR()
        return dr

    # TODO: Make this more useful for display
    def multiplier(self, type):
        multipliers = {"cut" : 1.5, "imp" : 2}
        return multipliers.get(type, 1)

    # Add a wound to this location.
    # TODO: Better tracking of wounds.
    def hurt(self, attack):
        self.wounds.append(attack["wound"])
        # BLOOD EVERYWHERE
        if attack.get("severed") is True:
            self.sever()

    def sever(self):
        # Store the original.
        original = self.owner
        # Generate a corpse.
        corpse = PartialCorpse(original)
        # Get affected parts.
        parts = self.descendants()
        # Reset the corpse's locations.
        corpse.actor.body.locs = {}
        # Stick the affected parts in the corpse and change their owner.
        for part in parts:
            # Change the part's owner.
            part.owner = corpse.actor
            # Store the same part object in the copy's locations.
            corpse.actor.body.locs[part.type] = part
            # Delete the part from the original actor.
            original.body.locs[part.type] = None
        # Put the corpse in the cell.
        original.cell().put(corpse)

    # Return a color for the limb status.
    # TODO: Move the limb glyph code here.
    def color(self):
        if self.severed() is True:       return "black"
        elif self.status() == CRIPPLED:  return "magenta"
        elif self.status() == INJURED:   return "red"
        elif self.status() == SCRATCHED: return "yellow"
        else:                            return "green"

    # Returns the damage that must be *exceeded* to cripple a limb.
    def crippling(self):
        return False

    # Is the limb crippled yet?
    def crippled(self):
        if self.crippling() is not False:
            if sum(self.wounds) > self.crippling():
                return True
        return False

    # Is the limb dismembered yet?
    def dismembered(self):
        if self.crippling() is not False:
            if sum(self.wounds) > 2*self.crippling():
                return True
        return False

    # STUB: Better severed status.
    def severed(self):
        if self.status() == SEVERED:
            return True
        if self.parent is not None:
            return self.parent.severed()
        else:
            return False

# Arms, legs, pseudopods, etc.
class Limb(HitLoc):
    def __init__(self, type, owner):
        HitLoc.__init__(self, type, owner)

    # Returns the damage that must be *exceeded* to cripple a limb.
    def crippling(self):
        return self.owner.MaxHP()/2

# Hands, feet, etc.
class Extremity(HitLoc):
    def __init__(self, type, owner):
        HitLoc.__init__(self, type, owner)

    # Returns the damage that must be *exceeded* to cripple an extremity.
    def crippling(self):
        return self.owner.MaxHP()/3
