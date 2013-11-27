from random import choice

from src.lib.agents.agent import Agent
from src.lib.agents.components.action import Action
from src.lib.agents.components.bodies import body
from src.lib.agents.components.combat import Combat
from src.lib.agents.components.container import Containing
from src.lib.agents.components.equipment import Equipment
from src.lib.agents.components.manipulation import ManipulatingTraits, Manipulation
from src.lib.agents.components.status import Status
from src.lib.agents.contexts.context import Context
# TODO: Better data importing.
import src.lib.data
from src.lib.data import skills
from src.lib.data import traits
from src.lib.generators.items import EquipmentGenerator
from src.lib.generators.text.describe import describe
import src.lib.generators.points
from src.lib.objects.items.carrion import Corpse

from src.lib.util.command import CommandRegistry as CMD
from src.lib.util.debug import *
from src.lib.util.define import *
from src.lib.util.dice import *
from src.lib.util.hex import *
from src.lib.util.key import *
from src.lib.util.log import Log
from src.lib.util.text import *
from src.lib.util.trait import Trait

@Trait.use(*ManipulatingTraits)
class Actor(Agent):
    """Monster-like Agents. Most typically, players and monsters."""
    components = [Equipment, Combat, Containing, Manipulation, Status]

    def __init__(self, components=[]):
        super(Actor, self).__init__(components + self.__class__.components)

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

    def trigger(self, *triggers):
        """Respond to triggers."""
        if "rebuild" or "spawned" in triggers:
            self.trigger_components("rebuild")
        if "equipped" or "unequipped" in triggers:
            self.trigger_components("modified", domain="Equipment")
        if not self.controlled and "placed" in triggers:
            self.trigger_components("placed", domain="AI")

    def provide_commands(self, context):
        """Yield the interaction commands an Agent provides to another Agent
        within a Context.
        """
        if "Combat" in context.domains:
            yield CMD("Attack", target=self, weapon=None)
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

    # TODO: Componentize
    def get_movement_modes(self):
        yield "walk"

    # Whether we can actually move to a pos.
    # TODO: Action chain
    def can_move(self, pos, dir=CC):
        if self.can_walk() is False:
            return False
        if self.valid_move(pos, dir) is False:
            return False
        return True

    # Check move validity.
    def valid_move(self, pos, direction=CC):
        # Map border checking:
        if self.map.valid(pos) is False:
            return False

        # Cell content checking:
        if self.map.cell(pos).can_block(self, direction):
            return False
        return True

    # TODO: Componentize.
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
        # Let Components react to the start of the turn.
        self.call([], "before_turn")
        # Do Nothing.
        if self.controlled is False and self.can_maneuver() is False:
            self.end_turn()
            return False
        return True

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
        if self.get("Status", "Unconscious"):
            return False
        return True

    # STUB: Figure out whether we are currently subject to stun.
    def can_be_stunned(self):
        if self.get("Status", "Stun"):
            return False
        return True

    # Get knocked out (and also knocked down.)
    def knockout(self):
        if self.can_be_knocked_out() is False:
            return False
        if self.controlled is True:
            self.screen("KO")
        self.call("Status", "set_status", "Unconscious", True)
        self.call("Manipulation", "drop_grasped")
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

    # Do something in a direction - this could be an attack or a move.
    def do(self, direction):
        if self.controlled is True and self.can_maneuver() is False:
            if self.alive is False:
                Log.add("%s is dead. Press Ctrl-q to quit the game." % self.appearance())
            else:
                Log.add("%s can't act in its current state." % self.appearance())
            self.end_turn()
            return False

        # Actors that are in our cell.
        # HACK: Need to fix this function to not include self.
        # actors = self.cell().intervening_actors(self.subposition, dir)

        # Within-hex attacks.
        # if actors and self.preferred_reach(0) is True:
        #     for actor in actors:
        #         if self.controlled != actor.controlled:
        #             return self.attack(actor)

        # Can't move if there are intervening actors in that direction.
        # if actors:
        #     return False
        # HACK
        # else:
        #     self.subposition = CC

        # OK, nobody in the way. We're doing something in another hex.
        # Which one?
        pos = add(self.pos, direction)

        # Check for invalid hexes.
        if not self.map.valid(pos):
            if self.controlled:
                Log.add("It would be a long, long way down into that yawning abyss.")
            return False

        cell = self.map.cell(pos)

        # TODO: Make bump attacks cleaner
        if cell and cell.occupied() and self.has_domain("Combat"):
            context = Context(agent=self, domains=["Combat"], intent={"attempt" : True}, participants=self.map.actors(pos))
            for command_class, command_arguments in context.get_commands():
                command = command_class(context)
                context.update_arguments(**command_arguments)
                result = self.process_command(command)
                outcome, cause = context.parse_result(result)
                self.end_turn()
                return outcome

        # The only option left.
        if self.can_move(pos, direction):
            if self.move(pos, direction):
                self.end_turn()
                return True
            if self.controlled:
                Log.add("Bonk! You ran headfirst into a bug. Report it.")
            return False
        else:
            if self.controlled:
                Log.add("Something's blocking the way.")
            return False

    # STUB: Whether the actor can take *any* actions.
    def can_act(self):
        if self.get("Status", "Unconscious"):
            return False
        return True

    # STUB: Whether actor can take maneuvers.
    def can_maneuver(self):
        if self.can_act() is False:
            return False
        if self.get("Status", "Stun"):
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
        if not level:
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
    # TODO: Move to Trait component.
    def stat(self, stat_name, temporary=True):
        if not hasattr(self, stat_name):
            return
        return getattr(self, stat_name)(temporary)

    # Formulas for calculated stats.
    def ST(self, temporary=True):
        ST = self.attributes.get('ST')
        if temporary:
            if self.get("Status", "Exhausted"):
                ST = (ST + 1) / 2
        return ST

    def DX(self, temporary=True):
        DX = self.attributes.get('DX')
        if temporary:
            DX -= self.get("Status", "Shock", 0)
        return DX

    def IQ(self, temporary=True):
        IQ = self.attributes.get('IQ')
        if temporary:
            IQ -= self.get("Status", "Shock", 0)
        return IQ

    def HT(self, temporary=True):
        HT = self.attributes.get('HT')
        #if temporary is True:
        #    HT -= self.effects.get("Shock", 0)
        return HT

    def HP(self, temporary=False):          return self.MaxHP(temporary) - self.hp_spent
    def MaxHP(self, temporary=False):       return self.stat('ST', temporary) # + levels of HP
    def FP(self, temporary=False):          return self.MaxFP(temporary) - self.fp_spent # + levels of FP
    def MaxFP(self, temporary=False):       return self.stat('HT', temporary) # + levels of FP
    def MP(self, temporary=False):          return self.MaxMP(temporary) - self.mp_spent # + levels of MP
    def MaxMP(self, temporary=False):       return self.stat('IQ', temporary) # + levels of MP, magery

    def Will(self, temporary=False):        return self.stat('IQ', temporary) # + levels of Will
    def Perception(self, temporary=False):  return self.stat('IQ', temporary) # +levels of Per

    # STUB: Insert formulas
    def Move(self, temporary=True):

        # TODO: Buying basic move.
        move = int(self.Speed(temporary) * (1 - .2 * self.Encumbrance()))

        if temporary:
            # Penalty from reeling: halve move.
            if self.get("Status", "Reeling"):
                move = (move + 1) / 2

            # Penalty from exhaustion: halve move.
            if self.get("Status", "Exhausted"):
                move = (move + 1) / 2

        return move

    def Speed(self, temporary=True):
        # TODO: buying levels of speed
        return self.stat('DX', temporary) + self.stat('HT', temporary)

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
    # TODO: Componentize!
    def prepare_hurt(self, attack):
        # Shock:
        attack["shock"] = min(attack["injury"], 4)

        # Effects of a major wound:
        if attack.get("major_wound"):
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
                attack["dropped_items"] = self.values("Manipulation", "get_wielded")

                # Knockout:
                if margin <= -5 or check == CRIT_FAIL:
                    if self.can_be_knocked_out() is True:
                        attack["knockout"] = True

    def hurt(self, attack):
        """Cause the effects decided in prepare_hurt()."""
        if attack.get("knockout") is not None:
            # TODO: Improve messaging
            Log.add("%s is knocked unconscious!" % self.appearance())
            self.knockout()

        if attack.get("knockdown") is not None:
            self.knockdown()

        if attack.get("dropped items") is not None:
            self.drop_all_held()

        if attack.get("stun") is not None and self.get("Status", "Unconscious") is False:
            self.call("Status", "set_status", "Stun", attack["stun"])
            # TODO: Change message.
            Log.add("%s is stunned!" % self.appearance())

        # Handle shock (potentially from multiple sources.)
        if attack.get("shock") is not None:
            shock = self.get("Status", "Shock", 0)
            self.call("Status", "set_status", "Shock", min(4, shock + attack["shock"]))

        # Cause HP loss.
        self.hp_spent += attack["injury"]
        hp = self.HP() # Store HP prior to the attack

        # Decide whether this blow killed you.
        # TODO: Refactor!
        if self.HP() < -self.MaxHP():
            death_checks_made = (min(0,hp) - 1)/self.MaxHP() + 1
            death_checks = (self.HP()-1)/self.MaxHP() + 1
            for death_check in range(-1*(death_checks - death_checks_made)):
                check, margin = self.sc('HT')
                if check < TIE:
                    self.alive = False

        # TODO: Return the effects tried/succeeded, and then offload text gen.

    def limbloss(self, attack):
        """Process loss of a limb."""
        # TODO: Refactor
        limbnames = []
        descendants = attack["location"].descendants()
        for descendant in descendants:
            limbnames.append(hit_locations.get(descendant.type))
        return "Auuuuugh! Your %s has been severed!<br><br>In total, you've lost the use of your %s." % (attack["location"].appearance(), commas(limbnames, False))

    def is_dead(self):
        """Return whether this Actor is dead."""
        if self.alive is False:
            return True
        # TODO: Move?
        if self.HP() <= -5*self.MaxHP():
            return True
        return False

    def process_death(self):
        """Process this Actor's death."""
        # Allow the Actor to respond before its death.
        self.react(identifier="before")

        # Set the Actor to dead.
        self.alive = False

        # Allow the Actor to respond on its death.
        self.react()

        # Place a corpse.
        # TODO: Make this a factory method.
        self.cell().put(self.generate_corpse())

        # Hand over cleanup to the map's level.
        # TODO: use a method here
        self.map.remove_actor(self)

    def before_process_death(self):
        """Allow this Actor to respond before its death."""
        self.drop_all()
        if self.controlled is True:
            self.screen("meat-death")

    def on_process_death(self):
        """Allow this Actor to respond on its death."""
        # TODO: make this based on whether we can see the dead creature
        # TODO: no messaging here - text generation belongs elsewhere
        Log.add(describe("%s has been slain!" % self.name))

    def generate_corpse(self):
        """Generate this Actor's Corpse."""
        if not self.is_dead():
            die("Tried to generate the Corpse of a living Actor.")
        return Corpse(self)

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

    # Returns a list of lines to go into a character sheet.
    # TODO: Move to a View!
    def get_view_data(self, view=None):
        yield self.description
        yield ""
        yield "HP: %s/%s" % (self.HP(), self.MaxHP())
        yield ""
        yield "--Wielding--"
        for wielded in self.values("Manipulation", "get_wielded"):
            yield wielded.appearance()
        # sheet.append("--Weapons--")
        # for slot, appearance, trait, trait_level, item in self.weapons:
        #     sheet.append("  %s: %s (%s-%s)" % (slot, appearance, trait, trait_level))
        yield ""
        yield "--Effects--"
        for effect, details in self.values("Status", "get_view_data"):
            yield "%s: %s" % (effect, details)
        yield "Posture: %s" % self.posture
        yield ""
        yield "--Attributes--"
        for attribute in primary_attributes:
            level = self.attributes[attribute]
            yield "%s: %s" % (attribute, level)
        yield ""
        # TODO: Make point printing nicer
#        sheet.append("--Points--")
#        for skill, points in self.points["skills"].items():
#            sheet.append("%s: %s points" % (skill, points))
#        sheet.append("")
#        sheet.append("--Skill Ranks--")
#        for skill, info in self.skills.items():
#            sheet.append("%s (%s/%s): %s%+d" % (skill, labels[skills.skill_list[skill]["attribute"]], labels[skills.skill_list[skill]["difficulty"]], labels[info[0]], info[1]))
#        sheet.append("")
        yield "--Skill Levels--"
        for skill, level in self.base_skills.items():
            skill = "%s (%s/%s)" % (skill, skills.skill_list[skill]["attribute"], skills.skill_list[skill]["difficulty"])
            level = level[0]
            yield "%-25s- %2s" % (skill, level)
            #if level[1] is not False:
            #    str += " " + "(default: %s%d)" % (level[1][0], level[1][1])

        # Print information about your body.
        yield ""
        yield "--DEBUG--"
        for line in self.values("Body", "get_view_data"):
            yield line

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