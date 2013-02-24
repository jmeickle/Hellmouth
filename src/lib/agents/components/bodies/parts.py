import random

from src.lib.util.define import *
from src.lib.objects.items.item import Natural
from src.lib.objects.items.carrion import PartialCorpse

# Hit location
class BodyPart(object):
    def __init__(self, type, owner):
        self.type = type
        self.owner = owner

        # Combat stats
        self.hp = 0
        self.dr = 0
        self.wounds = []
        self.attack_options = {}

        self.multipliers = {
            "pi-" : .5,
            "cut" : 1.5,
            "pi+" : 1.5,
            "imp" : 2,
            "pi++" : 2,
        }

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

        self.sorting = 0
        self.crippleable = True

    def appearance(self):
        appearance = hit_locations.get(self.type)
        if self.severed() is True:
            appearance = "severed " + appearance
        elif self.dismembered() is True:
            appearance = "maimed " + appearance
        elif self.crippled() is True:
            appearance = "crippled " + appearance
        return appearance

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
        if natural is True:
            for appearance, weapons in self.attack_options.items():
                if self.holding() is False or random.choice(weapons).requires_empty_location is False:
                    found_weapons[appearance] = weapons
        if wielded is True:
            for appearance, weapons in self.readied.items():
                found_weapons[appearance] = weapons
        return found_weapons

    # Information about this location.
    def display(self):
        screen = []
        screen.append("<%s-black>%s:</>" % (self.color(), self.appearance()))
        for k, v in self.worn.items():
            screen.append("  %s (worn)" % k)
        for k, v in self.held.items():
            screen.append("  %s (held)" % k)
        for k, v in self.readied.items():
            screen.append("  %s (ready)" % k)
        if len(self.attack_options) > 0:
            for weapon in self.attack_options.keys():
                screen.append("  %s (natural)" % weapon)
        return screen

    # Return the healthiness of the limb
    # TODO: Injured status for extremities, rather than using 'major wound'.

    def status(self):
        wounds = sum(self.wounds)
        if wounds == 0:
            return UNHURT
        elif self.crippleable is True:
            if self.severed() is True:                    return SEVERED
            elif self.dismembered() is True:              return DISMEMBERED
            elif self.crippled() is True:                 return CRIPPLED
            elif sum(self.wounds) > 1:                    return INJURED
            else:                                         return SCRATCHED
        else:
            if wounds > self.owner.MaxHP() * 2:           return DISMEMBERED
            elif wounds > self.owner.MaxHP():             return CRIPPLED
            elif wounds > self.owner.MaxHP() / 2:         return INJURED
            else:                                         return SCRATCHED

    # Set up a parent/child relationship.
    def add_child(parent, child):
        parent.children.append(child)
        child.parent = parent

    # Add a sublocation of this part.
    def sublocation(self, part):
        self.sublocations.append(part)

    # ITEMS
    # Return whether we're holding anything.
    def holding(self):
        if len(self.held) > 0:
            return True
        return False

    # STUB: Can we hold the item?
    def can_hold(self, item):
        # HACK: It's possible to hold multiple items.
        if self.holding():
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
    def prepare_hurt(self, attack):
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
                    attack["crippling wound"] = True
                    if attack["wound"] > 2*self.crippling():
                        attack["dismembering wound"] = True

                # Further damage to a crippled limb causes wounds - but it
                # doesn't cause further injury over the crippling amount!
                if self.crippled() is True:
                    attack["injury"] = 0

                # Cap damage based on max crippling damage, then figure out
                # if this attack caused crippling or dismemberment.

                # This *won't* cause a major wound because it represents the
                # slow build-up of injury rather than a large wound.
                else:
                    attack["injury"] = min(attack["wound"] + sum(self.wounds), 1 + self.crippling()) - sum(self.wounds)

                    # If the wound itself wouldn't have caused crippling, but
                    # it's pushed the limb over the edge to become crippled:
                    if attack["wound"] + sum(self.wounds) > self.crippling():
                        attack["crippled"] = True

                    # Likewise, but for dismemberment.
                    if attack["wound"] + sum(self.wounds) > 2*self.crippling():
                        attack["dismembered"] = True

    # TODO: Remove.
    def DR(self):
        dr = 0
        # HACK: Use all items!
        import random
        for appearance, itemlist in self.worn.items():
            item = random.choice(itemlist) # MEGA HACK.
            dr += item.DR()
        dr += self.dr + self.owner.DR()
        return dr

    def get_dr_glyph(self):
        """Display a glyph representing this part's DR."""
        dr = self.DR()
        if dr == 0:
            return " "
        elif dr < 10:
            return dr
        else:
            return "+"

    def get_dr_colors(self, fg=True, bg=True):
        """Display a color representing this part's DR."""
        dr = self.DR()

        if self.severed() or dr == 0:
            if fg and bg:
                return "black-black"
            else:
                return "black"
        else:
            if fg and bg:
                return "cyan-black"
            elif fg:
                return "cyan"
            else:
                return "black"

    # TODO: Make this more useful for display
    def multiplier(self, type):
        return self.multipliers.get(type, 1)

    # Add a wound to this location.
    # TODO: Better tracking of wounds.
    def hurt(self, attack):
        self.wounds.append(attack["wound"])

        # BLOOD EVERYWHERE
        if attack.get("severing wound") is True:
            self.sever(attack)
            if self.owner.controlled is True:
                self.owner.screen("ouch", {"body_text" : self.owner.limbloss(attack)})

    def sever(self, attack):
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
            # TODO: Just mark as severed instead?
            del original.body.locs[part.type]
        # Put the corpse in the cell.
        original.cell().put(corpse)

    # Return a color for the limb status.
    def color(self):
        status = self.status()
        if status == SEVERED:       return "black"
        elif status == DISMEMBERED: return "magenta"
        elif status == CRIPPLED:    return "red"
        elif status == INJURED:     return "yellow"
        elif status == SCRATCHED:   return "cyan" # TODO: Change color.
        else:                       return "green"

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
        return False
        if self.status() == SEVERED:
            return True
        if self.parent is not None:
            return self.parent.severed()
        else:
            return False

# Arms, legs, pseudopods, etc.
class Limb(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi++"] = 1
        self.multipliers["pi+"] = 1
        self.multipliers["imp"] = 1

        self.crippleable = True

    # Returns the damage that must be *exceeded* to cripple a limb.
    def crippling(self):
        return self.owner.MaxHP()/2

class Leg(Limb):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

    def sever(self, attack):
        self.owner.knockdown()
        Limb.sever(self, attack)

# Hands, feet, etc.
class Extremity(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi++"] = 1
        self.multipliers["pi+"] = 1
        self.multipliers["imp"] = 1

        self.crippleable = True

    # Returns the damage that must be *exceeded* to cripple an extremity.
    def crippling(self):
        return self.owner.MaxHP()/3

class Foot(Extremity):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

    def sever(self, attack):
        self.owner.knockdown()
        Extremity.sever(self, attack)

# Brain containment
class Skull(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.dr = 2

        self.multipliers["tox"] = 1

    # QUAD DAMAGE
    def multiplier(self, type):
        return self.multipliers.get(type, 4)

# Internal organs.
class Vitals(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["pi-"] = 3
        self.multipliers["pi"] = 3
        self.multipliers["pi+"] = 3
        self.multipliers["pi++"] = 3
        self.multipliers["imp"] = 3

# Squishy seeing organs
class Eye(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["tox"] = 1

    # QUAD DAMAGE
    def multiplier(self, type):
        return self.multipliers.get(type, 4)

    # Eyes are very easy to cripple.
    def crippling(self):
        return self.owner.MaxHP()/10

# Face.
class Face(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["corr"] = 1.5

# Neck
class Neck(BodyPart):
    def __init__(self, type, owner):
        BodyPart.__init__(self, type, owner)

        self.multipliers["cr"] = 1.5
        self.multipliers["corr"] = 1.5
        self.multipliers["cut"] = 2
