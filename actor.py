from define import *
from dice import _3d6, _d6, roll
from random import choice
from describe import d
import hex
import ai.astar

# Players, monsters, etc.
class Actor:
    def __init__(self):
        # Text information (cosmetic)
        self.name = 'Default monster'
        self.description = 'This is the description'

        # Appearance (cosmetic)
        self.glyph = '@'
        self.color = 'magenta-black'

        # Highly mutable actor state
        self.body = Humanoid(self)
        self.effects = {}
        self.inventory = {}
        self.base_skills = {}

        # Positioning information
        self.map = None
        self.pos = None

        # More static information: points spent on your character
        self.points = {
            "total": 0,
            "attributes" : {},
            "skills" : {},
            "techniques" : {},
            "traits" : {},
        }

        # The 'character sheet': derived from points spent in the above
        # categories, and changing only when they do.
        self.attributes = {
                      "Strength" : 10,
                      "Dexterity" : 10,
                      "Intelligence" : 10,
                      "Health" : 10,
                     }

        self.skills = {}
        self.techniques = {}
        self.traits = {}

        # Purely interface nicety
        self.letters = {}

        # AI stuff
        # TODO: Move to another file
        self.ai = ai.astar.AStar()
        self.path = None
        self.target = None
        self.distance = None

    # UTILITY

    # AI actions. Currently: move in a random direction.
    def act(self):
        # TODO: Refactor some of this so that it is less buggy, but for now, it kinda-sorta-works.
        self.distance = hex.dist(self.pos, self.target.pos)

        # TODO: More intelligently decide when to re-path
        if self.distance > 1 and self.path is None:
            # TODO: Get target stuff in here.
            if self.target is not None:
                self.ai.__init__()
                path = self.ai.path(self.pos, self.target.pos)
                if self.path is False: # Could not find a path
                    self.path = None
                else: # Set the list of coords as our path
                    self.path = path.get_path()

        if self.distance > 1 and self.path is not None:
            if self.path:
                #exit(self.path)
                pos = self.path.pop()
                # TODO: Set up a real coord tuple class already, slacker
                dir = (pos[0] - self.pos[0], pos[1] - self.pos[1])
                #exit("Curr: (%s, %s)\nNext: (%s, %s)\nDir: (%s, %s)" % (pos[0], pos[1], self.pos[0], self.pos[1], dir[0], dir[1]))
                if not self.do(dir):
                    # Coinflip chance to try a new path
                    if _d6() > 3:
                        self.path = None
                    else:
                        self.path.append(pos)
                    #self.over()
            else:
                self.path = None
                #self.over()
        else:
            dir = (self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1])
            self.do(dir)

        # Fallback: random movement.
        #self.do(choice(dirs))

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        pos = (self.pos[0]+dir[0], self.pos[1]+dir[1])
        #exit("%s, %s" % pos)
        if self.map.valid(pos) is False:
            exit("Tried to move past map borders")
            return False

        if self.map.cell(pos).occupied() is True:
            return self.attack(self.map.actor(pos))
        else:
            return self.move(pos)

        self.over()
        return False

    # Mark self as done acting.
    def over(self):
        self.map.acting = None
        self.map.queue.append(self)

    # Return your own cell
    def cell(self):
        return self.map.cell(self.pos)

    # MOVEMENT

    # Change actor coords directly and update the relevant cells.
    def go(self, pos):
        self.cell().remove(self)
        self.pos = pos
        self.cell().add(self)

    # Try to move based on an input direction. Return whether it worked.
    def move(self, pos):
        if self.valid_move(pos):
            self.go(pos)
            self.over()
            return True
        else:
            return False

    # Check move validity.
    def valid_move(self, pos):
        # Map border checking:
        if self.map.valid(pos) is False:
            return False

        # Cell content checking:
        if self.map.cell(pos).blocked() is True:
            return False

        return True

    # SKILLS

    # Gets the level of a skill as well as any situational modifiers.
    def skill(self, skill):
        level = self.skills.get(skill)        
        return level, mod

    # Performs a skill check.
    def sc(self, skill):
        level = self.skill.get(skill)
        mod = 0
        return sc(skill, mod)

    # Performs a quick contest.
    def qc(self, them, skill):
        self_skill, self_mod = self.skill(skill)
        their_skill, their_mod = them.skill(skill)
        return qc(self_skill, self_mod, their_skill, their_mod)

    # COMBAT

    # Do a basic attack.
    def attack(self, target, loc=None):
        att_name = self.name
        def_name = target.name
        verb = "s"
        if self == self.map.player:
            att_name = "you"
            verb = ""
        if target == self.map.player:
            def_name = "you"

        if _3d6() > 8:
            str = "%s @dmg@%s %s" % (att_name, verb, def_name)

            # Mute non-nearby messages
            if str is not None and hex.dist(self.map.player.pos, target.pos) <= 3:
                self.map.log.add(d(str))

            amt = sum(roll(_d6, self.damage))
            target.hit(amt)

        self.over()
        return True

    # Process damage when you are hit by something.
    def hit(self, amt):
        loc = self.randomloc()
        loc.hurt(amt)
        self.hp -= amt
        if self.check_dead() is True:
            self.die()

    # Check whether you are dead.
    def check_dead(self):
        if self.hp <= 0:
            return True

    # Remove self from the map and the queue
    def die(self):
        if hex.dist(self.map.player.pos, self.pos) <= self.map.viewrange:
            self.map.log.add(d("%s has been slain!" % self.name))
        if self == self.map.acting:
            self.map.acting = None
        self.map.queue.remove(self)
        self.cell().remove(self)

    # STATS

    # Retrieve actor stat.
    def stat(self, stat):
        val = self.stats.get(stat)
        if val is None:
            return self.calc_stat(stat)
        else:
            return val

    # If it wasn't found in self.stats, it must need to be calculated.
    def calc_stat(self, stat):
        func = getattr(Actor, stat.replace(' ', ''))
        return func(self)

    # STUB: Insert formulas
    # Formulas for calculated stats.
    def HitPoints(self):       return 33
    def MaxHitPoints(self):       return 33
    def ManaPoints(self):       return 33
    def MaxManaPoints(self):       return 33
    def FatiguePoints(self):       return 33
    def MaxFatiguePoints(self):       return 33
    def Will(self):       return 33
    def Perception(self): return 33
    def Move(self):       return 33
    def Speed(self):      return 33
    def Dodge(self):      return 33
    def Block(self):      return 32
    def Parry(self):      return 31

    # INJURY / HIT LOCATIONS

    # Choose a random hit location
    def randomloc(self):
        roll = _3d6()
        loc = self.body.table.get(roll, None)
        if loc is None:
            subroll = _d6()
            loc = self.body.table[("%s-%s" % (roll, subroll))]
        return loc

    # Choose the color for a hit location.
    def loccol(self, loc):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return "white-black"
        else:
            return "%s-black" % loc.color()

    # Return how many points of wounds a location has. Optional parameter: wrap that
    # string in a color tag.
    def wound(self, loc, col=True):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return 0
        else:
            wounds = sum(loc.wounds)
            col = loc.color()
            if loc.status() == SEVERED:
                wounds = 'X'
            elif wounds >= 10:
                wounds = '*'
            if col is True:
                return "<%s-black>%s</>" % (col, wounds)
            else:
                return wounds

    # INVENTORY
    # STUB: Return a sorted section of the inventory, or ground items, based on args
    def items(self):
        items = []
        index = 0
        for appearance, item in self.inventory.items():
            items.append((index, appearance, item))
            index += 1
        return items

    # Convert an item appearance to an item (randomly). False if nothing by that appearance.
    def item(self, appearance):
        list = self.inventory.get(appearance, None)
        if list is not None:
            item = choice(list)
            return item
        else:
            return False

    # 'Forcibly' add an inventory item
    def _add(self, item):
        list = self.inventory.get(item.appearance(), None)
        if list is not None:
            list.append(item)
        else:
            self.inventory[item.appearance()] = [item]

    # STUB: This should perform sanity checks that _add doesn't.
    def add(self, item):
        self._add(item)

    # 'Forcibly' remove a specific inventory item (and return it).
    # Returns false if the list doesn't exist or is empty.
    def _remove(self, item):
        list = self.inventory[item.appearance()]
        if list is not None:
            list.remove(item)
            if len(list) == 0:
                del self.inventory[item.appearance()]
            return item
        else:
            return False

    # Remove a single item (randomly chosen) based on its appearance (and return it).
    # Returns false if the list doesn't exist or is empty.
    def remove(self, appearance):
        list = self.inventory.get(appearance, None)
        if list is not None:
            item = choice(list)
            list.remove(item)
            if len(list) == 0:
                del self.inventory[appearance]
            return item
        else:
            return False

    # TODO: Support getting from any cell
    # Get item(s) with an appearance from a cell and put them in inventory.
    def get(self, appearance, num=1):
        cell = self.cell()
        for x in range(num):
            item = cell.get(appearance)
            if item is not False:
                self.add(item)

    # Get everything from the current cell.
    def get_all(self): 
        cell = self.cell()
        while len(cell.items) > 0:
            appearance, list = cell.items.popitem()
            self._merge(appearance, list)

    # TODO: Support dropping to any cell
    # 'Forcibly' drop a specific inventory item.
    # Returns false if the item wasn't found in the player's inventory.
    def _drop(self, item):
        if self.can_drop_item(item) is True:
            drop = self._remove(item)
            if drop is not False:
                self.cell().put(drop)
            else:
                exit("Lost an item: it was removed, but not returned.")
        return False

    # TODO: Support dropping to any cell
    # Take item(s) with the same appearance from the inventory and put them on the ground.
    def drop(self, appearance, num=1):
        cell = self.cell()
        for x in range(num):
            item = self._drop(self.item(appearance))
            if item is not False:
                cell.put(item)
            else:
                return False

    # Drop everything to the current cell.
    def drop_all(self): 
        cell = self.cell()
        while len(self.inventory) > 0:
            appearance, list = self.inventory.popitem()
            cell._merge(appearance, list)

    # Tack an appearance and associated list of items from a cell into your own inventory.
    def _merge(self, appearance, list):
        current = self.inventory.get(appearance, None)
        if current is not None:
            return current.extend(list)
        else:
            self.inventory[appearance] = list

    # Misc. map-item checking functions

    # Can stuff be gotten from a pos?
    def _can_get(self, item):
        return self.cell().can_get()

    # TODO: Sanity checks not handled above
    def can_get(self):
        return _can_get(self)

    # Can stuff be dropped into a pos?
    def _can_drop(self):
        return self.cell().can_drop()

    # TODO: Sanity checks not handled above
    def can_drop(self):
        return _can_drop(self)

    # Can this specific item be dropped?
    def can_drop_item(self, item):
        # Worn (as opposed to held) items cannot be dropped.
        if self.worn(item):
            return False
        return True

    # INVENTORY

    # STUB: Needed functions:
    # TODO: Everything with inventory lettering
    # recalculate letters
    # swap letters

    # reassign letter
    # find appropriate letter

    # Turn a letter into an item appearance.
    # Returns false if there is no appearance associated with the letter.
    #def l2i(self, letter):
    #    return self.letters.get(letter, False)

    #def i2l(self, letter):
    #    return l2i(letter)

    # TODO: Input a list of possible drop/get cells, then call cell class to check them.

    # TRY_DROP, general process:
    # See if you can drop into that cell.
    # Accept a letter. Get the appearance from the letter. Get an item from the appearance.
    # See if you can drop that item.
    # Only then, drop the item.

    # TRY_GET, general process:
    # See if you can get from that cell.
    # Accept a letter. Get the appearance from the get view's letter index.
    # Get an item from the appearance. See if you can get that item.
    # Only then, get the item.

    # Either hold or wear the item as appropriate.
    # Return false if nothing could be equipped.
    def _equip(self, item, loc, worn, weapon):
        if loc is None:
            slot = item.preferred_slot()
            loc = self.body.locs.get(slot, self.body.primary_slot)

        # If worn T/F is not provided, ask the item whether it's to be worn.
        if worn is None:
            worn = item.can_be_worn()

        # If weapon T/F is not provided, ask the item whether it's a weapon.
        if weapon is None:
            weapon = item.can_be_weapon()

        # Try to wear the item, if possible and if it's not already worn.
        if worn is True and self.worn(item) is False:
            loc.wear(item)
            return True

        # Can't wear it? Ready it as a weapon, if applicable and not already readied.
        elif weapon is True and self.readied(item) is False:
            # Hold the weapon, if it needs it.
            if item.must_be_held() is True:
                loc.hold(item)
            # Then ready it.
            loc.ready(item)

        # The only remaining option is to just hold the item.
        elif self.held(item) is False:
            loc.hold(item)

        # Otherwise, we fail.
        else:
            return False

    # TODO: Sanity checks not handled above.
    # Return false if nothing could be equipped.
    def equip(self, appearance, loc=None, worn=None, weapon=None):
        return self._equip(self.item(appearance), loc, worn, weapon)

    # Unhold or unwear the item in all appropriate ways.
    def _unequip(self, item):
        if item.is_held() is True:
            locs = item.held
            for loc in locs:
                if loc.owner == self:
                    loc.unhold(item)

        if item.is_readied() is True:
            locs = item.readied
            for loc in locs:
                if loc.owner == self:
                    loc.unready(item)

        if item.is_worn() is True:
            locs = item.worn
            for loc in locs:
                if loc.owner == self:
                    loc.unwear(item)

    # TODO: Sanity checks not handled above.
    def unequip(self, appearance):
        self._unequip(self.item(appearance))

    # Misc. inventory checking functions

    # Returns true if the item is held by (at least) you.
    def held(self, item):
        locs = item.held
        for loc in locs:
            if loc.owner == self:
                return True
        return False

    # Returns true if the item is readied by (at least) you.
    def readied(self, item):
        locs = item.readied
        for loc in locs:
            if loc.owner == self:
                return True
        return False

    # Returns true if the item is worn by (at least) you.
    def worn(self, item):
        locs = item.worn
        for loc in locs:
            if loc.owner == self:
                return True
        return False

    # Returns true if the item is held or worn by you.
    def equipped(self, item):
        if self.held(item) is True or self.worn(item) is True:
            return True
        return False

# Body layouts - humanoid, hexapod, etc.
class BodyPlan:
    def __init__(self, parent):
        # Size (0 for a human)
        self.size = None
        # Shape (tall, long, or full)
        self.shape = None
        # Body parts indexed by key
        self.locs = {}
        # Body parts indexed by 3d6 roll
        self.table = {}
        # Primary slot
        self.primary_slot = None

    # Build a body from the class information.
    def build(self, owner):
        for partname, parent, sublocation, rolls in self.parts:
            part = HitLoc(partname, owner)
            self.locs[partname] = part
            if parent is not None:
                HitLoc.add_child(self.locs[parent], part)
            for roll in rolls:
                if isinstance(roll, list) is True:
                    base = roll[0]
                    for x in range(len(roll)):
                        if x == 0:
                            continue;
                        subroll = roll[x]
                        self.table["%s-%s" % (base, subroll)] = part
                else:
                    self.table[roll] = part

class Humanoid(BodyPlan):
    # These tuples represent:
    # 1: Part name.
    # 2: Parent part. Only list parts that have already been listed.
    # 3: True if it's a sublocation rather than a real one.
    # 4: List representing what 3d6 rolls hit that spot.
    #    If a further d6 roll is required, use a list like:
    #        [15, [16, 1, 2, 3], 17]
    parts = (
             ('Torso', None, False, [9, 10]),
             ('Groin', 'Torso', False, [11]),
             ('Neck', 'Torso', False, [17, 18]),
             ('Head', 'Neck', False, [3, 4, 5]),
             ('RArm', 'Torso', False, [8]),
             ('LArm', 'Torso', False, [12]),
             ('RHand', 'RArm', False, [15, 1, 2, 3]),
             ('LHand', 'LArm', False, [15, 4, 5, 6],),
             ('RLeg', 'Groin', False, [6, 7]),
             ('LLeg', 'Groin', False, [13, 14]),
             ('RFoot', 'RLeg', False, [[16, 1, 2, 3]]),
             ('LFoot', 'LLeg', False, [[16, 4, 5, 6]]),
    )

    primary_slot = 'RHand'

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)

class Octopod(BodyPlan):
    # See Humanoid for a description.
    parts = (
             ('Mantle', None, None),
             ('Arm1', 'Mantle', None),
             ('Arm2', 'Mantle', None),
             ('Arm3', 'Mantle', None),
             ('Arm4', 'Mantle', None),
             ('Arm5', 'Mantle', None),
             ('Arm6', 'Mantle', None),
             ('Arm7', 'Mantle', None),
             ('Arm8', 'Mantle', None),
    )

    primary_slot = 'Arm1'

    def __init__(self, parent):
        BodyPlan.__init__(self, parent)
        self.build(parent)

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
        if self.status() == SEVERED:     return "cyan"
        elif self.status() == CRIPPLED:  return "magenta"
        elif self.status() == INJURED:   return "red"
        elif self.status() == SCRATCHED: return "yellow"
        else:                            return "white"

    # TODO: Move the limb glyph code here.

# Actor test code
if __name__ == "__main__":
    testactor = Actor()
    print "Stats:", testactor.stats

    print "Random movement choice:", choice(dirs)

    print "Actor's parts:"
    for index, part in testactor.body.locs.items():
        print "Part: %s - Children: %s - Parent:%s" % (part.type, part.children, part.parent)

    print "Connectivity test:"
    start = "RFoot"
    curr = testactor.body.locs.get(start)
    while curr.parent is not None:
        print "%s bone's connected to the %s bone..." % (curr.type, curr.parent.type)
        curr = curr.parent

    print "To-hit chart:"
    print "\n".join("%s - %s" % (x[0], x[1].type) for x in sorted(testactor.body.table.items()))

    #print "Connectivity test (Octo):"
    #testactor.body = Octopod(testactor)
    #start = "Arm1"
    #curr = testactor.body.locs.get(start)
    #while curr.parent is not None:
    #    print "%s bone's connected to the %s bone..." % (curr.type, curr.parent.type)
    #    curr = curr.parent
