from random import choice

from define import *
from dice import *
from hex import *
from text import *
from generators.text.describe import describe

from data import skills
from data import traits
import generators.points
import body

from combat import CombatAction
import log
from operator import itemgetter

from objects.items.carrion import Corpse

# Players, monsters, etc.
class Actor:
    def __init__(self):
        # Text information (cosmetic)
        self.name = 'Default monster'
        self.description = 'This is the description'
        self.voice = "speak"

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

        # Can be run at any time, but this will at least grab the natural weapons.
        self.weapons = []
        self.weapon = 0
        self.attack_options = []
        self.attack_option = 0
        self.parries = []
        self.parry = 0

        self.posture = "standing"

    def appearance(self):
#        if self.controlled is True:
#            return "<green-black>" + self.name + "</>"
#        else:
            return self.name

    # UTILITY
    def ready(self):
        # HACK: We don't need to check this every turn!
        self.check_weapons()

    # STUB: Things to do before taking a turn.
    def before_turn(self):
        # Do Nothing.
        if self.can_maneuver() is False:
            self.over()

    # STUB: Things to do at the end of your turn.
    def after_turn(self):
        # Shock ends at the end of your turn.
        # TODO: Handle the case of getting shock in your own turn.
        if self.effects.get("Shock") is not None:
            del self.effects["Shock"]
            # TODO: Real message.
            log.add("%s shrugs off the shock." % self.appearance())

        for effect, details in self.effects.items():
            if effect == "Stun":
                # TODO: Mental Stun
                check, margin = self.sc('HT')
                if check > TIE:
                    del self.effects["Stun"]
                    # TODO: Real message.
                    log.add("%s shrugs off the stun." % self.appearance())

    # Display the attack line for the current combination of weapon/attack option.
    # TODO: Multiple attacks.
    def attackline(self):
        weapon = self.weapons[self.weapon]
        attack_option = self.attack_options[self.attack_option]
        return weapon, attack_option

    def choose_weapon(self, scroll):
        assert len(self.weapons) != 0, "Had 0 weapons: %s" % self.__dict__
        self.weapon += scroll
        if self.weapon >= len(self.weapons):
            self.weapon = 0
        if self.weapon < 0:
            self.weapon = len(self.weapons) - 1

        weapon = self.weapons[self.weapon]
        slot, appearance, trait, trait_level, item = weapon
        self.attack_options = sorted(item.attack_options[trait].items(), key=itemgetter(0))
        self.choose_attack_option(0)

    def choose_attack_option(self, scroll):
        assert len(self.attack_options) != 0, "Had 0 attack options: %s" % self.__dict__
        self.attack_option += scroll
        if self.attack_option >= len(self.attack_options):
            self.attack_option = 0
        if self.attack_option < 0:
            self.attack_option = len(self.attack_options) - 1

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

    # Change posture.
    def change_posture(self, posture):
        self.posture = posture

    # Returns whether we're on the ground (either side).
    def prone(self):
        if self.posture == "lying prone" or self.posture == "lying face up":
            return True
        return False

    # Returns whether we're conscious.
    def conscious(self):
        if self.effects.get("Unconscious") is not None:
            return False
        return True

    # STUB: Figure out whether we are subject to knockdown.
    def can_be_knocked_down(self):
        if self.prone() is True:
            return False
        return True

    # STUB: Figure out whether we are subject to knockout.
    def can_be_knocked_out(self):
        if self.conscious() is False:
            return False
        return True

    # STUB: Figure out whether we are currently subject to stun.
    def can_be_stunned(self):
        if self.effects.get("Stun") is None:
            return True
        return False

    # Get knocked down.
    def knockdown(self):
        if flip() == SUCC:
            self.change_posture("lying prone")
        else:
            self.change_posture("lying face up")

    # Recalculate only skills (usually this will be all that changed.)
    def recalculate_skills(self):
        skills.calculate_ranks(self)
        skills.calculate_skills(self)
        # TODO: Fix default calculation.
#        skills.calculate_defaults(self)

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        pos = add(self.pos, dir)
        if self.map.valid(pos) is False:
            if self.controlled is True:
                log.add("You can't bring yourself to dive into the yawning abyss before you.")
            return False

        if self.map.cell(pos).occupied() is True:
            if self.controlled != self.map.actor(pos).controlled:
                return self.attack(self.map.actor(pos))
        else:
            return self.move(pos)

        self.over()
        return False

    # Mark self as done acting.
    def over(self):
        if self.map.acting == self:
            self.after_turn()
            self.map.acting = None
            self.map.queue.append(self)
            if self.controlled is False:
                self.attempts = 0

    # Return your own cell
    def cell(self):
        return self.map.cell(self.pos)

    # Show a screen.
    def screen(self, screenname, arguments=None, screenclass=None):
        self.map.screen(screenname, arguments, screenclass)

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

    # STUB Gets the level of a skill as well as any situational modifiers.
    def skill(self, skill, temporary=True):
        attribute, level = self.skills.get(skill, (None, 0))
        # TODO: Fix attr defaulting.
        # Didn't have it, or anything that defaults to it. So:
#        if level is None:
#            skill_data = skills.skill_list.get(skill)
#            default = skill_data.get("attribute_default")
            # If default is False, no default from attr for that skill.
#            if default is None:
                # Default: -4 easy, -5 average, -6 hard
#                level = self.stat(skill_data["attribute"]) - 4 + difficulties[skill_data["difficulty"]]
#            elif default is not False:
#                level = self.stat(skill_data["attribute"]) - default
#        if situational is True:
#            return level, 0
#        else:
        if attribute is not None:
            return self.stat(attribute, temporary) + level

    # Get the actor's level in a skill/stat.
    def trait(self, traitname, temporary=True):
        level = self.stat(traitname, temporary)
        if level is None:
            level = self.skill(traitname, temporary)
        return level

    # Performs a stat or skill check.
    def sc(self, traitname):
        level = self.trait(traitname)
        mod = 0 # TODO: Get mod.
        return sc(level, mod)

    # Performs a quick contest.
    def qc(self, them, skill):
        self_skill, self_mod = self.skill(skill, True)
        their_skill, their_mod = them.skill(skill, True)
        return qc(self_skill, self_mod, their_skill, their_mod)

    # TODO: Support armor divisors.
    def damage(self, damage, do_roll=True):
        damage = re.split('(\w*)([+-]?\d*)', damage)
        type = damage[1]
        mod = 0
        if damage[2] != '':
            mod += int(damage[2])
        if type == "thr":
            return dice(self.Thrust(), mod, do_roll)
        elif type == "sw":
            return dice(self.Swing(), mod, do_roll)

    # COMBAT
    # Find eligible weapons.
    def check_weapons(self):
        weapons = []
        parries = []
        for slot, loc in self.body.locs.items():
            if loc is None:
                continue
            for appearance, weaponlist in loc.weapons().items():
                for weapon in weaponlist:
                    for trait, attack_options in weapon.attack_options.items():
                        trait_level = self.trait(trait)
                        if trait_level > 0: # HACK: Magic number!
                            weapons.append((slot, appearance, trait, trait_level, weapon))
                            for attack_name, attack_data in attack_options.items():
                                parry_mod = attack_data[3]
                                if parry_mod is not None:
                                    # TODO: Handle U weapons.
                                    parries.append((slot, appearance, trait, trait_level + parry_mod, attack_name, weapon))
        self.weapons = sorted(weapons, key=itemgetter(3,0,2,1), reverse=True)
        self.parries = sorted(parries, key=itemgetter(3,0,2,1), reverse=True)

        # HACK: Shouldn't always reset like this.
        self.parry = 0
        self.choose_weapon(0)

    # Function called to produce a simple, single attack maneuver.
    def attack(self, target):
        maneuvers = []
        # Can have multiple items here, weirdly enough...
        weapon = self.weapons[self.weapon]
        attack_option = self.attack_options[self.attack_option]
        slot, appearance, trait, trait_level, item = weapon
        # Overwrite with current level of the trait.
        trait_level = self.trait(trait)

        maneuvers.append((target, item, trait, attack_option))
        self._attack(maneuvers)
        self.over()
        return False

    # Use attack maneuvers to do an attack.
    def _attack(self, maneuvers):
        attacks = {}

        for maneuver in maneuvers:
            target, item, skill, attack_option = maneuver
            attack_name, attack_stats = attack_option
            attacks[maneuver] = {}
            attacks[maneuver]["attacker"] = self
            attacks[maneuver]["target"] = target
            attacks[maneuver]["item"] = item
            attacks[maneuver]["skill"] = skill
            attacks[maneuver]["attack name"] = attack_name
            attacks[maneuver]["attack stats"] = attack_stats

        action = CombatAction(attacks)

        if action.setup() is True:
            action.fire()

        # TODO: Replace with check for whether it's interesting.
        for line in action.display():
            log.add(line)
        action.cleanup()
        self.over()
        return True

    # Choose a defense and set information about it in the attack.
    def choose_defense(self, attack):
        # Get possible defenses.
        retreat = False # TODO: Decide whether to retreat.
        dodge = self.Dodge(retreat)
        parries = self.Parry(retreat, True)
        # TODO: Block

        # TODO: Figure out expected number of attacks to decide whether multiple parries would be worth it.
        if parries is not None:
            parry = parries[0]
            if parry[3] > dodge:
                attack["defense"] = "parry"
                attack["defense level"] = parry[3]
                attack["defense information"] = parry

        elif dodge is not None:
            attack["defense"] = "dodge"
            attack["defense level"] = dodge
            attack["information"] = None

        # The default is attack["defense"] == None.
        if attack.get("defense") is not None and retreat is True:
            attack["retreat"] = True

    # Decide which entire-actor effects will happen in response to injury.
    def prepare_hurt(self, attack):
        # Shock:
        attack["shock"] = min(attack["injury"], 4)

        # Effects of a major wound:
        if attack.get("major wound") is True:
            # TODO: Face/vital/etc. hits
            check, margin = self.sc('HT')
            if check < TIE:
                # Stun:
                if self.can_be_stunned() is True:
                    attack["stun"] = True

                # Knockdown:
                if self.can_be_knocked_down() is True: 
                    attack["knockdown"] = True

                # Disarmament:
                # TODO: Force dropping held items
                if self.is_holding_items() is True:
                    attack["dropped items"] = True

                # Knockout:
                if margin <= -5 or check == CRIT_FAIL:
                    if self.can_be_knocked_out() is True:
                        attack["knockout"] = True

    # Cause the effects decided in prepare_hurt().
    def hurt(self, attack):
        # Handle shock (potentially from multiple sources.)
        if attack.get("shock") is not None:
            shock = self.effects.get("Shock", 0)
            self.effects["Shock"] = min(4, shock + attack["shock"])

        if attack.get("stun") is not None:
            self.effects["Stun"] = attack["stun"]
            # TODO: Change message.
            log.add("%s is stunned!" % self.appearance())

        if attack.get("dropped items") is not None:
            # TODO: Change message.
            log.add("%s drops items!" % self.appearance())

        if attack.get("knockout") is not None:
            self.effects["Unconscious"] = attack["knockout"]
            # TODO: Improve messaging
            log.add("%s was knocked unconscious!" % self.appearance())

        # Cause HP loss.
        self.hp_spent += attack["injury"]

    # We just lost a limb :(
    def limbloss(self, attack):
        limbnames = []
        descendants = attack["location"].descendants()
        for descendant in descendants:
            limbnames.append(hit_locations.get(descendant.type))
        return "Auuuuugh! Your %s has been severed!<br><br>In total, you've lost the use of your %s." % (attack["location"].appearance(), commas(limbnames, False))

    # Check whether you are dead.
    def check_dead(self):
        if self.alive is False:
            return True

        if self.HP() <= -5*self.MaxHP():
            return True

    # Remove self from the map and the queue
    def die(self):
        if self.death() is True:
            self.alive = False
            if self == self.map.acting:
                self.map.acting = None
            self.map.queue.remove(self)
            self.cell().remove(self)

    # *Mechanical* actions to perform on death. Return whether we actually died.
    # For example, extra lives happen here - you die, but then come back.
    def death(self):
        # HACK: Shouldn't be a magic number
        if dist(self.map.player.pos, self.pos) <= 10:
            log.add(describe("%s has been slain!" % self.name))
        self.cell().put(self.corpse())
        return self.check_dead()

    # Generate a corpse of ourselves.
    def corpse(self):
        return Corpse(self)

    # STUB: Whether the actor can take *any* actions.
    def can_act(self):
        if self.conscious() is False:
            return False
        return True

    # STUB: Whether actor can take maneuvers.
    def can_maneuver(self):
        if self.can_act() is False:
            return False
        if self.effects.get("Stun") is not None:
            return False
        return True

    # STUB: Whether actor can defend.
    def can_defend(self):
        if self.can_act() is False:
            return False
        return True

    # STATS

    # Retrieve actor stat.
    def stat(self, stat, temporary=True):
        if not hasattr(self, stat):
            return
        func = getattr(Actor, stat)
        if temporary is True:
            return func(self)
        else:
            return func(self, temporary)

    # Formulas for calculated stats.
    def ST(self, temporary=True):
        ST = self.attributes.get('ST')
        #if temporary is True:
        #    ST -= self.effects.get("Shock", 0)
        return ST

    def DX(self, temporary=True):
        DX = self.attributes.get('DX')
        if temporary is True:
            DX -= self.effects.get("Shock", 0)
        return DX

    def IQ(self, temporary=True):
        IQ = self.attributes.get('IQ')
        if temporary is True:
            IQ -= self.effects.get("Shock", 0)
        return IQ

    def HT(self, temporary=True):
        HT = self.attributes.get('HT')
        #if temporary is True:
        #    HT -= self.effects.get("Shock", 0)
        return HT

    def HP(self):          return self.MaxHP() - self.hp_spent
    def MaxHP(self):       return self.stat('ST', False) # + levels of HP
    def FP(self):          return self.MaxFP() - self.fp_spent # + levels of FP
    def MaxFP(self):       return self.stat('HT', False) # + levels of FP
    def MP(self):          return self.MaxMP() - self.mp_spent # + levels of MP
    def MaxMP(self):       return self.stat('IQ', False) # + levels of MP, magery

    def Will(self):        return self.stat('IQ') # + levels of Will
    def Perception(self):  return self.stat('IQ') # +levels of Per

    # STUB: Insert formulas
    def Move(self):        return int(self.Speed() * (1 - .2 * self.Encumbrance())) # Plus basic move
    def Speed(self):       return self.stat('DX', False) + self.stat('HT', False) # Plus buying speed

    # STUB: Can be modified by acrobatics, etc.
    def Dodge(self, retreat=False):
        if self.can_defend() is False:
            return None

        status_mod = 0
        if self.effects.get("Stun") is not None:
            status_mod -= 4

        posture_mod = postures[self.posture][1]

        retreat_mod = 0
        if retreat is True:
            retreat_mod += 3

        dodge = self.Speed()/4 + 3 + status_mod + posture_mod + retreat_mod# /4 because no /4 in speed.
        return dodge

    # STUB: depends on skill
    def Block(self, retreat=False):
        if self.can_defend() is False:
            return None
        return None

    # STUB: Currently always returns highest parry.
    def Parry(self, retreat=False, list=False):
        if self.can_defend() is False:
            return None

        status_mod = 0
        if self.effects.get("Stun") is not None:
            status_mod -= 4

        posture_mod = postures[self.posture][1]

        parries = []
        for slot, appearance, trait, trait_level, attack_name, weapon in self.parries:
            # Get the attack data, and parry modifier from it.
            attack_data = weapon.attack_options[trait][attack_name]
            parry_mod = attack_data[3]

            # Recalculate trait level for this weapon.
            trait_level = self.trait(trait, False)

            # TODO: Check whether the skill has had points paid for it (imp. retreat)
            if retreat is True:
                retreat_mod = 1
                if trait in skills.skill_list:
                    retreat_mod = skills.skill_list[trait].get("retreat", 1)
            else:
                retreat_mod = 0

            parry = 3 + trait_level/2 + parry_mod + status_mod + posture_mod + retreat_mod
            parries.append((slot, appearance, trait, parry, attack_name, weapon))
        if list is True:
            return sorted(parries, key=itemgetter(3), reverse=True)
        else:
            return sorted(parries, key=itemgetter(3), reverse=True)[0][3]

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

    # STUB: Return body-wide damage resistance.
    def DR(self):
        return 0

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

    # TODO: Move this to body class.
    # Choose a random hit location
    # TODO: Handle severed rerolling.
    def randomloc(self):
        roll = r3d6()
        loc = self.body.table.get(roll, None)
        if loc is None:
            subroll = r1d6()
            loc = self.body.table[("%s-%s" % (roll, subroll))]
        return loc

    # TODO: Get rid of this?
    # Choose the color for a hit location.
    def loccol(self, loc):
        loc = self.body.locs.get(loc, None)
        if loc is None:
            return "white-black"
        else:
            return "%s-black" % loc.color()

    # DR number for a location.
    def locdr(self, slot):
        loc = self.body.locs.get(slot, None)
        if loc.severed() is True:
            return " "

        dr = loc.DR()
        if dr == 0:
            return " "
        elif dr < 10:
            return "<cyan-black>%s</>" % dr
        else:
            return "<cyan-black>!</>"

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
    # TODO: Print this more nicely after new inventory scheme.
    def list_carried(self):
        items = []
        for appearance, itemlist in self.inventory.items():
            append = True
            for item in itemlist:
                if item.is_equipped() is True:
                    append = False
            if append is True:
                items.append((appearance, itemlist))
        return sorted(items, key=itemgetter(0))

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
        itemlist = self.inventory[item.appearance()]
        if itemlist is not None:
            itemlist.remove(item)
            if len(itemlist) == 0:
                del self.inventory[item.appearance()]
            else:
                self.inventory[item.appearance()] = itemlist
            return item
        else:
            return False

    # Remove a single item (randomly chosen) based on its appearance (and return it).
    # Returns false if the list doesn't exist or is empty.
    def remove(self, appearance):
        itemlist = self.inventory.get(appearance, None)
        if itemlist is not None:
            item = choice(itemlist)
            itemlist.remove(item)
            if len(itemlist) == 0:
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
    # HACK: Appearances might change in picking them up!
    def get_all(self): 
        cell = self.cell()
        if len(cell.items) > 0:
            appearances = []

            while len(cell.items) > 0:
                appearance, itemlist = cell.items.popitem()
                self._merge(appearance, itemlist)
                appearances.append(appearance)

            log.add("You pick up the %s." % commas(appearances, False))

    # TODO: Support dropping to any cell
    # 'Forcibly' drop a specific inventory item.
    # Returns false if the item wasn't found in the player's inventory.
    def _drop(self, item):
        if self._can_drop_item(item) is True:
            assert self._unequip(item) is True, "Lost an item: it was removed, but not returned."
            self._remove(item)
            self.cell().put(item)
            log.add("You drop the %s." % item.appearance())
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
            appearance, itemlist = self.inventory.popitem()
            cell._merge(appearance, itemlist)

    # Tack an appearance and associated list of items from a cell into your own inventory.
    def _merge(self, appearance, itemlist):
        current = self.inventory.get(appearance, [])
        current.extend(itemlist)
        self.inventory[appearance] = current

    # Misc. map-item checking functions

    # Can stuff be gotten from a pos?
    def _can_get(self):
        return self.cell().can_get()

    # TODO: Sanity checks not handled above
    def can_get(self):
        return self._can_get()

    # Whether there is anything both interesting and possible to get.
    def can_get_items(self):
        if len(self.cell().items) == 0:
            return False
        return self.can_get()

    # Can stuff be dropped into a pos?
    def _can_drop(self):
        return self.cell().can_drop()

    # TODO: Sanity checks not handled above
    def can_drop(self):
        return self._can_drop()

    # Can this specific appearance be dropped?
    def can_drop_item(self, appearance):
        return self._can_drop_item(self.item(appearance))

    # Can this specific item be dropped?
    def _can_drop_item(self, item):
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
    def _equip(self, item, slots, wear, weapon):
        if self._can_equip_item(item, slots) is False:
            return False

        # If worn T/F is not provided, ask the item whether it's to be worn.
        if wear is None:
            wear = item.can_be_worn()

        # If weapon T/F is not provided, ask the item whether it's a weapon.
        if weapon is None:
            weapon = item.can_be_weapon()

        # Use the item's slots if provided.
        if item.slots is not None:
            slots = item.slots
        # Otherwise use the preferred slot.
        elif slots is None:
            # TODO: Make this check alternate slots, rather than primary_slot.
            slots = [item.preferred_slot()]

        # Get the location objects for the slot.
        locs = []
        for slot in slots:
          locs.append(self.body.locs.get(slot, self.body.primary_slot))

        # Try to wear the item, if possible and if it's not already worn.
        if wear is True and self.worn(item) is False:
            for loc in locs:
                loc.wear(item)

        # Can't wear it? Ready it as a weapon, if applicable and not already readied.
        elif weapon is True and self.readied(item) is False:
            # Hold the weapon, if it needs it.
            if item.requires_empty_location() is True:
                for loc in locs:
                    loc.hold(item)
            # Then ready it.
            for loc in locs:
                loc.ready(item)

        # The only remaining option is to just hold the item.
        elif self.held(item) is False:
            for loc in locs:
                loc.hold(item)

        # Otherwise, we fail.
        else:
            log.add("You can't equip the %s right now." % item.appearance())
            return False

        # HACK: Remove the equipped item from inventory.
        self._remove(item)
        self.check_weapons()
        log.add("You equip the %s." % item.appearance())
        return True

    # TODO: Sanity checks not handled above.
    # Return false if nothing could be equipped.
    def equip(self, appearance, loc=None, worn=None, weapon=None):
        return self._equip(self.item(appearance), loc, worn, weapon)

    # Can we equip an item of a specific appearance?
    def can_equip_item(self, appearance, loc=None):
        return self._can_equip_item(self.item(appearance), loc)

    # Can we equip a specific item?
    def _can_equip_item(self, item, loc=None):
        # HACK: Should not proceed this far.
        if item is False or item is None:
            return False

        if item.is_worn():
            return False

        # HACK: Prevent armor layering.
        if item.slots is not None:
            for slot in item.slots:
                loc = self.body.locs[slot]
                if len(loc.worn) > 0:
                    return False

        # HACK: Prevent wielding more than one weapon.
        if item.can_be_weapon():
            loc = self.body.locs[self.body.primary_slot]
            if loc.can_hold(item) is False:
                return False
        return True

    # Unhold or unwear the item in all appropriate ways.
    def _unequip(self, item):
        if item.is_held() is True:
            locs = item.held[:]
            for loc in locs:
                if loc.owner == self:
                    loc.unhold(item)

        if item.is_readied() is True:
            locs = item.readied[:]
            for loc in locs:
                if loc.owner == self:
                    loc.unready(item)

        if item.is_worn() is True:
            locs = item.worn[:]
            for loc in locs:
                if loc.owner == self:
                    loc.unwear(item)

        self.check_weapons()
        # HACK: Add back to inventory after unequipping.
        self._add(item)
        log.add("You unequip the %s." % item.appearance())

        return True

    # TODO: Sanity checks not handled above.
    def unequip(self, appearance):
        self._unequip(self.item(appearance))

    # Can we unequip an item of a specific appearance?
    def can_unequip_item(self, appearance):
        return self._can_unequip_item(self.item(appearance))

    # Can we unequip a specific item?
    def _can_unequip_item(self, item):
        if not item.is_equipped():
            return False
        return True

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

    # Are we holding any items?
    def is_holding_items(self):
        for loc in self.body.locs.values():
            if loc.holding() is True:
                return True
        return False

    # Returns a list of lines to go into a character sheet.
    def character_sheet(self, chargen=False):
        sheet = []
        if chargen is False:
            sheet.append(self.description)
            sheet.append("")
        sheet.append("--Attributes--")
        for attribute in primary_attributes:
            level = self.attributes[attribute]
            sheet.append("%s: %s" % (attribute, level))
        sheet.append("")
        sheet.append("--Weapons--")
        for slot, appearance, trait, trait_level, item in self.weapons:
            sheet.append("  %s: %s (%s-%s)" % (slot, appearance, trait, trait_level))
        sheet.append("")
        sheet.append("--Effects--")
        for effect, details in self.effects.items():
            sheet.append("%s: %s" % (effect, details))
        sheet.append(self.posture)
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

        # Print information about your body.
        sheet.extend(self.body.display())
        return sheet

    # Paperdolls are based on body, of course.
    def paperdoll(self):
        return self.body.paperdoll()
