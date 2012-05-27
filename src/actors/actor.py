from random import choice

from define import *
from dice import *
from hex import *

from generators.text.describe import describe

from data import skills
from data import traits
import generators.points
import body

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
        self.body = body.Humanoid(self)
        self.effects = {}
        self.inventory = {}
        self.base_skills = {}

        self.hp_spent = 0
        self.fp_spent = 0
        self.mp_spent = 0

        self.alive = True

        # Positioning information
        self.map = None
        self.pos = None

        # More static information: points spent on your character
        self.points = {
            "total": 0,
            "unspent" : 0,
            "skills" : {},
            "techniques" : {},
            "traits" : {
                "ST" : 0,
                "DX" : 0,
                "IQ" : 0,
                "HT" : 0,
            },
        }

        # The 'character sheet': derived from points spent in the above
        # categories, and changing only when they do.
        self.attributes = {}
        self.skills = {}
        self.techniques = {}
        self.advantages = {}
        self.disadvantages = {}

        # Purely interface nicety
        self.letters = {}

        # Whether this thing accepts keyboard control currently
        self.controlled = False

        self.generator = None
        self.weapons = {}

        # Can be run at any time, but this will at least grab the natural weapons.
        self.check_weapons()

    # UTILITY

    # Actor generation/improvement.
    # 'unspent' determines whether to try to re-spend unspent points, as well
    # as whether to save unspent points accrued during generation.
    def build(self, points, unspent=True):
        self.points["total"] += points
        if unspent is True:
            points += self.points["unspent"]
            self.points["unspent"] = 0
        spent = generators.points.spend_points(self)
        for k, v in spent.items():
            if k == 'unspent' and unspent is True:
                self.points["unspent"] += v
            else:
                for entry, points in v.items():
                    if self.points[k].get(entry) is not None:
                        self.points[k][entry] += points
                    else:
                        self.points[k][entry] = points
        self.recalculate()

    # Recalculate the character sheet from points spent.
    def recalculate(self):
        self.recalculate_attributes()
        self.recalculate_skills()

    # Reset attributes and recalculate from points.
    def recalculate_attributes(self):
        self.attributes = {}
        for attribute in primary_attributes + secondary_attributes:
            points = self.points["traits"].get(attribute)
            if points is not None:
                trait = traits.trait_list[attribute]
                levels = points / trait["cost"]
                self.attributes[attribute] = trait.get("default", 0) + min(levels, trait["max"])

    # Recalculate only skills (usually this will be all that changed.)
    def recalculate_skills(self):
        skills.calculate_ranks(self)
        skills.calculate_skills(self)
        skills.calculate_defaults(self)

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        pos = add(self.pos, dir)
        if self.map.valid(pos) is False:
            if self.controlled is True:
                self.map.log.add("You can't bring yourself to dive into the yawning abyss before you.")
            return False

        if self.map.cell(pos).occupied() is True:
            return self.attack(self.map.actor(pos))
        else:
            return self.move(pos)

        self.over()
        return False

    # Mark self as done acting.
    def over(self):
        if self.map.acting == self:
            self.map.acting = None
            self.map.queue.append(self)
            if self.controlled is False:
                self.attempts = 0

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

    # TODO: Support armor divisors.
    def damage(self, damage):
        damage = re.split('(\w*)([+-]?\d*)', damage)
        type = damage[1]
        mod = int(damage[2])
        if type == "thr":
            return dice(self.Thrust(), mod)
        elif type == "sw":
            return dice(self.Swing(), mod)
    # COMBAT
    def check_weapons(self):
        for locname, loc in self.body.locs.items():
            for appearance, weapons in loc.weapons().items():
                self.weapons[(appearance, locname)] = weapons

    # Do a basic attack.
    def attack(self, target, loc=None):
    # TODO: Make sure this can only happen within weapon range.
        att_name = self.name
        def_name = target.name
        verb = "s"
        if self == self.map.player:
            att_name = "you"
            verb = ""
        if target == self.map.player:
            def_name = "you"

        if r3d6() > 8:
            str = "%s @dmg@%s %s" % (att_name, verb, def_name)

            # Mute non-nearby messages
            if str is not None and dist(self.map.player.pos, target.pos) <= 3:
                self.map.log.add(describe(str))
            # TODO: Replace roll() with dice()
            amt = sum(roll(r1d6, self.damage))
            target.hit(amt)

        self.over()
        return True

    # Process damage when you are hit by something.
    def hit(self, amt):
        loc = self.randomloc()
        loc.hurt(amt)
        self.hp_spent += amt
        if self.check_dead() is True:
            self.die()

    # Check whether you are dead.
    def check_dead(self):
        if self.HP() <= -5*self.MaxHP():
            return True

    # Remove self from the map and the queue
    def die(self):
        if dist(self.map.player.pos, self.pos) <= 10: # HACK: Shouldn't be a magic number
            self.map.log.add(describe("%s has been slain!" % self.name))
        #if self == self.map.acting:
        #    self.map.acting = None
        self.map.queue.remove(self)
        self.cell().remove(self)
        self.alive = False

    # STATS

    # Retrieve actor stat.
    def stat(self, stat):
        val = self.attributes.get(stat)
        # Not an attribute? Must be a calculcated stat.
        if val is None:
            return self.calc_stat(stat)
        else:
            return val

    # If it wasn't found in self.stats, it must need to be calculated.
    def calc_stat(self, stat):
        func = getattr(Actor, stat)
        return func(self)

    # Formulas for calculated stats.
    def HP(self):          return self.MaxHP() - self.hp_spent
    def MaxHP(self):       return self.stat('ST') # + levels of HP
    def FP(self):          return self.MaxFP() - self.fp_spent # + levels of FP
    def MaxFP(self):       return self.stat('HT') # + levels of FP
    def MP(self):          return self.MaxMP() - self.mp_spent # + levels of MP
    def MaxMP(self):       return self.stat('IQ') # + levels of MP, magery
    def Will(self):        return self.stat('IQ') # + levels of Will
    def Perception(self):  return self.stat('IQ') # +levels of Per
    # STUB: Insert formulas
    def Move(self):        return int(self.Speed() * (1 - .2 * self.Encumbrance())) # Plus basic move
    def Speed(self):       return self.stat('DX') + self.stat('HT') # Plus buying speed
    def Dodge(self):       return self.Speed()/4 + 3# Can be modified by acrobatics, etc.
    def Block(self):       return None # STUB: depends on skill
    def Parry(self):       return None # STUB: depends on skill
    def Lift(self):        return int(round(self.stat('ST')*self.stat('ST') / float(5)))
    def Encumbrance(self): return 0 # STUB

    def Thrust(self):
        assert self.stat('ST') <= 70, "ST value exceeded accurate range."
        return damage_dice((self.stat('ST')+1) / 2 - 7)

    # Three part piecewise function
    def Swing(self):
        assert self.stat('ST') <= 45, "ST value exceeded accurate range."
        if self.stat('ST') > 27:
            return damage_dice((self.stat('ST')-1)/2 + 4)
        elif self.stat('ST') > 8:
            return damage_dice(self.stat('ST')-10)
        else:
            return damage_dice((self.stat('ST')-1)/2-5)

    # UI / DIALOGUE
    # STUB:
    def cursor_color(self):
        return self.dialogue_color()

    def dialogue_color(self):
        if self.controlled is True:
            return "green-black"
        else:
            return "red-black"
    
    # INJURY / HIT LOCATIONS

    # Choose a random hit location
    def randomloc(self):
        roll = r3d6()
        loc = self.body.table.get(roll, None)
        if loc is None:
            subroll = r1d6()
            loc = self.body.table[("%s-%s" % (roll, subroll))]
        return loc

    # Choose the color for a hit location.
    def loccol(self, loc):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return "white-black"
        else:
            return "%s-black" % loc.color()

    # Calculate how many points of wounds a location has, then return
    # it as a single character. Optional parameter: wrap the character
    # in a color tag.
    def wound(self, loc, col=True):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return "?"
        else:
            wounds = sum(loc.wounds)
            if wounds == 0:
                return " "
            col = loc.color()
            if loc.status() == SEVERED:
                wounds = 'X'
            elif wounds >= 10:
                wounds = '!'
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

    # Returns a list of lines to go into a character sheet.
    def character_sheet(self, chargen=False):
        sheet = []
        if chargen is False:
            sheet.append("==%s==" % self.name)
            sheet.append("")
            sheet.append(self.description)
            sheet.append("")
        sheet.append("--Attributes--")
        for attribute in primary_attributes:
            level = self.attributes[attribute]
            sheet.append("%s: %s" % (attribute, level))
        sheet.append("")
#        sheet.append("--Points--")
#        for skill, points in self.points["skills"].items():
#            sheet.append("%s: %s points" % (skill, points))
#        sheet.append("")
#        sheet.append("--Skill Ranks--")
#        for skill, info in self.skills.items():
#            sheet.append("%s (%s/%s): %s%+d" % (skill, labels[skills.skill_list[skill]["attribute"]], labels[skills.skill_list[skill]["difficulty"]], labels[info[0]], info[1]))
#        sheet.append("")
        sheet.append("--Skill Levels--")
        for skill, level in self.base_skills.items():
            skill = "%s (%s/%s)" % (skill, skills.skill_list[skill]["attribute"], skills.skill_list[skill]["difficulty"])
            level = level[0]
            str = "%-20s- %2s" % (skill, level)
            #if level[1] is not False:
            #    str += " " + "(default: %s%d)" % (level[1][0], level[1][1])
            sheet.append(str)
        return sheet

    # Paperdolls are based on body, of course.
    def paperdoll(self):
        return self.body.paperdoll()

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
