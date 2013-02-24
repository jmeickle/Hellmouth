from random import choice
from operator import itemgetter

from src.lib.util.define import *
from src.lib.util.dice import *
from src.lib.util.hex import *
from src.lib.util.key import *
from src.lib.util.text import *

from src.lib.generators.text.describe import describe
from src.lib.generators.items import EquipmentGenerator

# TODO: Better data importing.
import src.lib.data
from src.lib.data import skills
from src.lib.data import traits

import src.lib.generators.points
from src.lib.agents.components.bodies import body

from src.lib.agents.contexts.combat import CombatAction
from src.lib.util.log import Log
from src.lib.util.debug import *

from src.lib.objects.items.carrion import Corpse

from src.lib.agents.agent import Agent

from src.lib.agents.components.action import Action
from src.lib.agents.components.combat import Combat
from src.lib.agents.components.container import Container
from src.lib.agents.components.manipulation import ManipulatingAgent

class Actor(Agent, ManipulatingAgent):
    """Monster-like Agents. Most typically, players and monsters."""

    components = [Combat, Container]

    def __init__(self, components=[]):
        super(Actor, self).__init__(components)

        # Text information (cosmetic)
        self.name = 'Default monster'
        self.description = 'This is the description'
        self.voice = "speak"

        # Appearance (cosmetic)
        self.glyph = '@'
        self.color = 'magenta-black'

        # Highly mutable actor state
#        self.register_component(self, component, domain=None):
#        self.body = body.Humanoid(self)
        self.component_registry["Body"] = [body.Humanoid(self)]

        self.base_skills = {}

        self.hp_spent = 0
        self.fp_spent = 0
        self.mp_spent = 0

        self.alive = True

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

        self.generator = "default"
        self.loadouts = None

        self.posture = "standing"

        self.knowledge = {}

    #
    # MOVEMENT AND POSITIONING:
    #

    # Change actor coords directly and update the relevant cells.
    def go(self, pos, dir=CC):
        if self.map.cell(pos).occupied() is True:
            actors = self.map.cell(pos).actors
            self.subposition = flip(dir)
            for actor in actors:
                actor.subposition = dir
        else:
            self.subposition = CC
        self.cell().remove(self)
        self.pos = pos
        self.cell().add(self)

    # Try to move based on an input direction. Return whether it worked.
    # TODO: Action chain
    def move(self, pos, dir=CC):
        if self.can_move(pos, dir):
            self.go(pos, dir)
            return True
        else:
            return False

    # Whether we can actually move to a pos.
    # TODO: Action chain
    def can_move(self, pos, dir=CC):
        if self.can_walk() is False:
            return False
        if self.valid_move(pos, dir) is False:
            return False
        return True

    # Check move validity.
    def valid_move(self, pos, dir=CC):
        # Map border checking:
        if self.map.valid(pos) is False:
            return False

        # Cell content checking:
        if self.map.cell(pos).blocked(dir) is True:
            return False

        return True

    # Change posture.
    def change_posture(self, posture):
        self.posture = posture

    # Returns whether we're on the ground (either side).
    def prone(self):
        if self.posture == "lying prone" or self.posture == "lying face up":
            return True
        return False

    #
    # UTILITY
    #

    # TODO: Get rid of this; namespace conflict!
    def ready(self):
        """Called when an actor is ready to act."""
        pass
        # HACK: We don't need to check this every turn!
        # self.check_weapons()

    # STUB: Things to do before taking a turn.
    def before_turn(self):

        # Do Nothing.
        if self.controlled is False and self.can_maneuver() is False:
            self.over()

    # STUB: Things to do at the end of your turn.
    def after_turn(self):
        pass

    # STUB: Figure out whether we are subject to knockdown.
    def can_be_knocked_down(self):
        if self.prone() is True:
            return False
        return True

    # STUB: Figure out whether we are subject to knockout.
    def can_be_knocked_out(self):
        if self.has("Status", "Unconscious"):
            return False
        return True

    # STUB: Figure out whether we are currently subject to stun.
    def can_be_stunned(self):
        if self.has("Status", "Stun"):
            return False
        return True

    # Get knocked out (and also knocked down.)
    def knockout(self):
        if self.can_be_knocked_out() is False:
            return False
        if self.controlled is True:
            self.screen("KO")
        self.set("Status", "unconscious", True)
        self.process("Equipment", "drop_all_held")
        self.knockdown()

    # Get knocked down.
    def knockdown(self):
        if self.can_be_knocked_down() is False:
            return False
        if coin() == SUCC:
            self.change_posture("lying prone")
        else:
            self.change_posture("lying face up")
        # TODO: Improve messaging
        Log.add("%s falls over!" % self.appearance())

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        if self.controlled is True and self.can_maneuver() is False:
            if self.alive is False:
                Log.add("%s is dead. Press Ctrl-q to quit the game." % self.appearance())
            else:
                Log.add("%s can't act in its current state." % self.appearance())
            self.over()
            return False

        # Actors that are in our cell.
        # HACK: Need to fix this function to not include self.
        actors = self.cell().intervening_actors(self.subposition, dir)

        # Within-hex attacks.
        if actors and self.preferred_reach(0) is True:
            for actor in actors:
                if self.controlled != actor.controlled:
                    return self.attack(actor)

        # Can't move if there are intervening actors in that direction.
        if actors:
            return False
        # HACK
        else:
            self.subposition = CC

        # OK, nobody in the way. We're doing something in another hex.
        # Which one?
        pos = add(self.pos, dir)

        # Range 1 bump-attacks.
        if self.map.cell(pos).occupied() is True:
            for actor in self.map.actors(pos):
                if self.controlled != actor.controlled:
                    if self.preferred_reach(1) is True:
                        return self.attack(actor)

        # Check for invalid hexes.
        if self.map.valid(pos) is False:
            if self.controlled is True:
                Log.add("It would be a long, long way down into that yawning abyss.")
            return False

        # The only option left.
        if self.can_move(pos, dir):
            self.over()
            return self.move(pos, dir)

    # Mark self as done acting.
    def over(self):
        if self.map.acting == self:
            self.after_turn()
            self.map.acting = None
            self.map.queue.append(self)
            if self.controlled is False:
                self.attempts = 0

    # STUB: Whether the actor can take *any* actions.
    def can_act(self):
        if self.has("Status", "Unconscious"):
            return False
        return True

    # STUB: Whether actor can take maneuvers.
    def can_maneuver(self):
        if self.can_act() is False:
            return False
        if self.has("Status", "Stun"):
            return False
        return True

    # STUB: Whether actor can walk.
    def can_walk(self):
        if self.can_act() is False:
            return False
        # HACK
        if self.prone() is True:
            return False
        return True

    # STUB: Whether actor can defend.
    def can_defend(self):
        if self.can_act() is False:
            return False
        return True

    # Silly utility function that puts necessary information into kwargs
    # TODO: Rewrite.
    def prep_kwargs(self, kwargs):
        kwargs["actor"] = self
        return kwargs

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

    #
    # SKILLS
    #

    # STUB Gets the level of a skill as well as any situational modifiers.
    def skill(self, skill, temporary=True):
        attribute, level = self.skills.get(skill, (None, 0))

        if attribute is not None:
            return self.stat(attribute, temporary) + level

        # TODO: Fix attr defaulting.
        # Didn't have it, or anything that defaults to it. So:
        else:
            skill_data = skills.skill_list.get(skill)
            default = skill_data.get("attribute_default")
            # If default is False, no default from attr for that skill.
            if default is False:
                return False
            elif default is None:
                # Default: -4 easy, -5 average, -6 hard
                level = - 4 + difficulties[skill_data["difficulty"]]
            else:
                level = default

            return self.stat(skill_data["attribute"], temporary) + level

    # Get the actor's level in a skill/stat.
    def trait(self, traitname, temporary=True):
        level = self.stat(traitname, temporary)
        if level is None:
            level = self.skill(traitname, temporary)
        return level

    # Performs a stat or skill check.
    def sc(self, traitname, modifier=0):
        level = self.trait(traitname)
        return sc(level, modifier)

    # Performs a quick contest.
    def qc(self, them, skill):
        self_skill, self_mod = self.skill(skill, True)
        their_skill, their_mod = them.skill(skill, True)
        return qc(self_skill, self_mod, their_skill, their_mod)

    #
    # STATS
    #

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
        if temporary is True:
            if self.has("Status", "Exhausted") is True:
                ST = (ST + 1) / 2
        return ST

    def DX(self, temporary=True):
        DX = self.attributes.get('DX')
        if temporary is True:
            DX -= self.get("Status", "Shock", 0)
        return DX

    def IQ(self, temporary=True):
        IQ = self.attributes.get('IQ')
        if temporary is True:
            IQ -= self.get("Status", "Shock", 0)
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
    def Move(self):

        # TODO: Buying basic move.
        move = int(self.Speed() * (1 - .2 * self.Encumbrance()))

        # Penalty from reeling: halve move.
        if self.reeling() is True:
            move = (move + 1) / 2

        # Penalty from exhaustion: halve move.
        if self.exhausted() is True:
            move = (move + 1) / 2

        return move

    def Speed(self):
        # TODO: buying speed
        speed = self.stat('DX', False) + self.stat('HT', False)
        return speed

    # STUB: Can be modified by acrobatics, etc.
    def Dodge(self, retreat=False):
        if self.can_defend() is False:
            return None

        status_mod = 0
        if self.has("Status", "Stun"):
            status_mod -= 4

        posture_mod = postures[self.posture][1]

        retreat_mod = 0
        if retreat is True:
            retreat_mod += 3

        dodge = self.Speed()/4 + 3 + status_mod + posture_mod + retreat_mod# /4 because no /4 in speed.

        # Penalty from reeling: halve dodge.
        if self.has("Status", "Reeling"):
            dodge = (dodge + 1) / 2

        # Penalty from exhaustion: halve dodge.
        if self.has("Status", "Exhausted"):
            dodge = (dodge + 1) / 2

        return dodge

    # STUB: depends on skill
    def Block(self, retreat=False):
        if self.can_defend() is False:
            return None
        return None

    # STUB!!!
    def get_parries(self):
        return []

    # STUB: Currently always returns highest parry.
    def Parry(self, retreat=False, list=False):
        if self.can_defend() is False:
            return None

        status_mod = 0
        if self.has("Status", "Stun"):
            status_mod -= 4

        posture_mod = postures[self.posture][1]

        parries = []
        for slot, appearance, trait, trait_level, attack_data, weapon in self.get_parries():
            # Get the parry modifier from the attack data.
            parry_mod = attack_data[4]
            # HACK: Weapon balance.
            if isinstance(parry_mod, tuple):
                parry_mod, balanced = parry_mod

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
            parries.append((slot, appearance, trait, parry, attack_data, weapon))

        if list is True:
            return sorted(parries, key=itemgetter(3), reverse=True)
        else:
            if parries:
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
            return "black-black"
        else:
            return "%s-black" % loc.color()

    # DR number for a location.
    def locdr(self, slot):
        loc = self.body.locs.get(slot, None)
        if loc is None:
            return " "
        if loc.severed() is True:
            return " "

        dr = loc.DR()
        if dr == 0:
            return " "
        elif dr < 10:
            return "<cyan-black>%s</>" % dr
        else:
            return "<cyan-black>+</>"

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
        if attack.get("knockout") is not None:
            # TODO: Improve messaging
            Log.add("%s is knocked unconscious!" % self.appearance())
            self.knockout()

        if attack.get("knockdown") is not None:
            self.knockdown()

        if attack.get("dropped items") is not None:
            self.drop_all_held()

        if attack.get("stun") is not None and self.has("Status", "Unconscious") is False:
            self.set("Status", "status", "Stun", attack["stun"])
            # TODO: Change message.
            Log.add("%s is stunned!" % self.appearance())

        # Handle shock (potentially from multiple sources.)
        if attack.get("shock") is not None:
            shock = self.get("Status", "Shock", 0)
            # shock = self.effects.get("Shock", 0)
            self.set("Status", "Shock", min(4, shock + attack["shock"]))

        # Cause HP loss.
        hp = self.HP()
        self.hp_spent += attack["injury"]

        if self.HP() < -self.MaxHP():
            death_checks_made = (min(0,hp) - 1)/self.MaxHP() + 1
            death_checks = (self.HP()-1)/self.MaxHP() + 1
            for death_check in range(-1*(death_checks - death_checks_made)):
                check, margin = self.sc('HT')
                if check < TIE:
                    self.alive = False

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
            self.drop_all()
            self.cell().remove(self)
            if self.controlled is True:
                self.screen("meat-death")

    # *Mechanical* actions to perform on death. Return whether we actually died.
    # For example, extra lives happen here - you die, but then come back.
    def death(self):
        # HACK: Shouldn't be a magic number
        if dist(self.map.player.pos, self.pos) <= 10:
            Log.add(describe("%s has been slain!" % self.name))
        self.cell().put(self.corpse())
        return self.check_dead()

    # Generate a corpse of ourselves.
    def corpse(self):
        return Corpse(self)

    #
    # INVENTORY:
    #

    #
    # EQUIPMENT:
    #

    # Either hold or wear the item as appropriate.
    # Return false if nothing could be equipped.
    def _equip(self, item, slots=None, wear=None, weapon=None):
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
            Log.add("%s can't equip the %s right now." % (self.appearance(), item.appearance()))
            return False

        # HACK: Remove the equipped item from inventory.
        self._remove(item)
        self.check_weapons()
        # HACK: Later add a flag.
        if self.controlled is True:
            Log.add("%s equips the %s." % (self.appearance(), item.appearance()))
        return True

    # TODO: Sanity checks not handled above.
    # Return false if nothing could be equipped.
    def equip(self, appearance, slots=None, wear=None, weapon=None):
        return self._equip(self.item(appearance), slots, wear, weapon)

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
        # HACK: Later, make this a flag
        if self.controlled is True:
            Log.add("%s unequips the %s." % (self.appearance(), item.appearance()))

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

    #
    # INFORMATION DISPLAYS:
    #

    # TODO: Add real coloring support.
    def appearance(self):
        return self.name

    # Returns a list of lines to go into a character sheet.
    # TODO: Move to a View!
    def character_sheet(self, chargen=False):
        sheet = []
        if chargen is False:
            sheet.append(self.description)
            sheet.append("")
        sheet.append("--Weapons--")
        for slot, appearance, trait, trait_level, item in self.weapons:
            sheet.append("  %s: %s (%s-%s)" % (slot, appearance, trait, trait_level))
        sheet.append("")
        sheet.append("--Effects--")
        for effect, details in self.effects.items():
            sheet.append("%s: %s" % (effect, details))
        sheet.append("Posture: %s" % self.posture)
        sheet.append("")
        sheet.append("--Attributes--")
        for attribute in primary_attributes:
            level = self.attributes[attribute]
            sheet.append("%s: %s" % (attribute, level))
        sheet.append("")
        # TODO: Make point printing nicer
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
            str = "%-25s- %2s" % (skill, level)
            #if level[1] is not False:
            #    str += " " + "(default: %s%d)" % (level[1][0], level[1][1])
            sheet.append(str)

        # Print information about your body.
        sheet.extend(self.body.display())
        return sheet

    # Paperdolls are based on body, of course.
    # TODO: Componentize.
    def paperdoll(self):
        return self.body.paperdoll()

    # Show a screen.
    # TODO: Refactor this so it isn't touching map?
    def screen(self, screenname, arguments=None, screenclass=None):
        self.map.screen(screenname, arguments, screenclass)

    # STUB:
    def cursor_color(self):
        return self.dialogue_color()
    # STUB:
    def dialogue_color(self):
        if self.controlled is True:
            return "green-black"
        else:
            return "red-black"

    #
    # GENERATION AND IMPROVEMENT:
    #

    # TODO: Move all of this to its own module.

    # Actor generation/improvement.
    # 'unspent' determines whether to try to re-spend unspent points, as well
    # as whether to save unspent points accrued during generation.
    def build(self, points, unspent=True):
        self.points["total"] += points
        if unspent is True:
            points += self.points["unspent"]
            self.points["unspent"] = 0
        spent = src.lib.generators.points.spend_points(self)
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

    # Generate, add to inventory, and equip some generated items.
    def generate_equipment(self, loadouts=None):
        return False
        if loadouts is None:
            if self.loadouts is not None:
                loadouts = self.loadouts
            else:
                return False

        equipment = []
        for loadout in loadouts:
            generator = EquipmentGenerator(src.lib.data.generators.equipment.generators)
            equipment.extend(generator.generate_equipment(loadout))

        for item in equipment:
            self._add(item)
            self._equip(item)

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
        # TODO: Fix default calculation.
#        skills.calculate_defaults(self)
