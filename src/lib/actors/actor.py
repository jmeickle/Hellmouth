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
import body
import action

from combat import CombatAction
from src.lib.util import log
from src.lib.util.debug import *

from src.lib.objects.items.carrion import Corpse

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
        self.subposition = CC

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

        # Can be run at any time, but this will at least grab the natural weapons.
        self.weapons = []
        self.weapon = 0
        self.attack_options = []
        self.attack_option = 0
        self.parries = []
        self.parry = 0

        self.posture = "standing"
        self.commands = {
            CMD_ATTACK : self.attack,
            CMD_ATTACK : self.attack,
        }

        self.knowledge = {}

    #
    # MOVEMENT AND POSITIONING:
    #

    # Return your own cell
    def cell(self):
        return self.map.cell(self.pos)

    # Calculate the distance between an actor and a target.
    def dist(self, target):
        return dist(self.pos, target.pos)

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

    def ready(self):
        # HACK: We don't need to check this every turn!
        self.check_weapons()

    # STUB: Things to do before taking a turn.
    def before_turn(self):
        # Clear retreats.
        if self.effects.get("Retreat") is not None:
            del self.effects["Retreat"]

        if self.conscious() is True and self.HP() < 0:
            check, margin = self.sc('HT', self.MaxHP() / self.HP())
            if check < TIE:
                # TODO: Improve messaging
                log.add("%s passes out." % self.appearance())
                self.knockout()

        # Do Nothing.
        if self.controlled is False and self.can_maneuver() is False:
            self.over()

    # STUB: Things to do at the end of your turn.
    def after_turn(self):
        # Shock ends at the end of your turn.
        # TODO: Handle the case of getting shock in your own turn.
        if self.effects.get("Shock") is not None:
            del self.effects["Shock"]

        for effect, details in self.effects.items():
            if effect == "Stun":
                # TODO: Mental Stun
                check, margin = self.sc('HT')
                if check > TIE:
                    del self.effects["Stun"]
                    # TODO: Real message.
                    if self.conscious() is True:
                        log.add("%s shrugs off the stun." % self.appearance())


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
        if self.effects.get("Stun") is not None:
            return False
        return True

    # Get knocked out (and also knocked down.)
    def knockout(self):
        if self.can_be_knocked_out() is False:
            return False
        if self.controlled is True:
            self.screen("KO")
        self.effects["Unconscious"] = True
        self.drop_all_held()
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
        log.add("%s falls over!" % self.appearance())

    # Perform a command.
    def perform(self, command, target):
        return self.commands.get(command)(target)

    # Do something in a dir - this could be an attack or a move.
    def do(self, dir):
        if self.controlled is True and self.can_maneuver() is False:
            if self.alive is False:
                log.add("%s is dead. Press Ctrl-q to quit the game." % self.appearance())
            else:
                log.add("%s can't act in its current state." % self.appearance())
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
                log.add("It would be a long, long way down into that yawning abyss.")
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

    def list_commands(self):
        commands = []
        commands.append(CMD_ATTACK)
        commands.append(CMD_TALK)
        return commands

    # Silly utility function that puts necessary information into kwargs
    # TODO: Rewrite.
    def prep_kwargs(self, kwargs):
        kwargs["actor"] = self
        return kwargs

    #
    # COMBAT
    #

    # TODO: Move all combat 'thinking' into src/lib/actor/ai/combat.

    def choose_weapon(self, scroll):
        assert len(self.weapons) != 0, "Had 0 weapons: %s" % self.__dict__
        self.weapon += scroll
        if self.weapon >= len(self.weapons):
            self.weapon = 0
        if self.weapon < 0:
            self.weapon = len(self.weapons) - 1

        weapon = self.weapons[self.weapon]
        slot, appearance, trait, trait_level, item = weapon
        self.attack_options = item.attack_options[trait]
        self.attack_option = 0

    def choose_attack_option(self, scroll):
        assert len(self.attack_options) != 0, "Had 0 attack options: %s" % self.__dict__
        self.attack_option += scroll
        if self.attack_option >= len(self.attack_options):
            self.attack_option = 0
        if self.attack_option < 0:
            self.attack_option = len(self.attack_options) - 1

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
                            for attack_data in attack_options:
                                parry_mod = attack_data[4]
                                if parry_mod is not None:
                                    # HACK: Handle balanced status.
                                    if isinstance(parry_mod, tuple):
                                        parry_mod, balanced = parry_mod
                                    # TODO: Handle U weapons.
                                    parries.append((slot, appearance, trait, trait_level + parry_mod, attack_data, weapon))
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

        if self._attack(maneuvers) is True:
            self.over()
            return True

    # Use attack maneuvers to do an attack.
    def _attack(self, maneuvers):
        attacks = {}

        for maneuver in maneuvers:
            # NOTE: This will fail when rapid strikes come into play, of course!
            # Same target, item, skill, *and* attack option.
            target, item, skill, attack_option = maneuver
            distance = dist(self.pos, target.pos)

            # TODO: Improve how this is called. attack_option[0] ?
            # Instantiate this action's object.
            attack = action.Action("attack")

            # Continue to the next maneuver if we failed our attempt.
            # TODO: Analyze failure reason here instead
            if self.attempt(attack, target=target, item=item) is False:
                continue

            attacks[maneuver] = {}
            attacks[maneuver]["attacker"] = self
            attacks[maneuver]["target"] = target
            attacks[maneuver]["distance"] = dist(self.pos, target.pos)
            attacks[maneuver]["item"] = item
            attacks[maneuver]["skill"] = skill
            attacks[maneuver]["attack name"] = attack_option[0]
            attacks[maneuver]["attack stats"] = attack_option[1:]

        # Couldn't reach with any of our desired attacks.
        if len(attacks) == 0:
            return False

        combat_action = CombatAction(attacks)

        if combat_action.setup() is True:
            combat_action.fire()

        # TODO: Replace with check for whether it's interesting.
        for line in combat_action.display():
            log.add(line)
        combat_action.cleanup()
        return True

    # STUB: Handle movement on a retreat.
    def retreat(self, attack):
        self.move(attack["retreat position"])

    # Decide whether to retreat or not.
    def choose_retreat(self, attack):
        # No sleep-dodging!
        if self.can_act() is False:
            return False
        # Already retreated against this attacker - still get a bonus.
        if self.effects.get("Retreat") == attack["attacker"]:
            return True
        # Already retreated, but not against this attacker. No bonus.
        elif self.effects.get("Retreat") is not None:
            return False

        # Otherwise, we can retreat if we can find a spot to move to.
        # TODO: Handle sideslips and slips
        mode = 1
        cells = perimeter(attack["attacker"].pos, attack["distance"] + mode)
        options = []
        for cell in cells:
            if dist(self.pos, cell) == 1 and self.valid_move(cell):
                options.append(cell)
        if options:
            attack["retreat position"] = random.choice(options)
            return True
        else:
            return False

    # Choose a defense and set information about it in the attack.
    def choose_defense(self, attack):
        # Whether to apply the retreat bonus to this attack.
        retreat = self.choose_retreat(attack)

        # Get possible defenses.
        dodge = self.Dodge(retreat)
        parries = self.Parry(retreat, True)
        # TODO: Block
        # TODO: Figure out expected number of attacks to decide whether multiple parries would be worth it.

        if dodge is not None:
            attack["defense"] = "dodge"
            attack["defense level"] = dodge
            attack["information"] = None

        if parries:
            parry = parries[0]
            if parry[3] > dodge:
                attack["defense"] = "parry"
                attack["defense level"] = parry[3]
                attack["defense information"] = parry

        # The default is attack["defense"] == None.
        if attack.get("defense") is not None and retreat is True:
            attack["retreat target"] = attack["attacker"]
            self.effects["Retreat"] = attack["retreat target"]

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
    # INTERACTION:
    #

    # Returns true if the currently preferred weapon has reach.
    # TODO: Remove this function.
    def preferred_reach(self, dist):
        attack_option = self.attack_options[self.attack_option]
        min_reach = attack_option[3][0]
        max_reach = attack_option[3][-1]
        if dist >= min_reach and dist <= max_reach:
            return True
        else:
            return False

    # STUB: Natural reach. Always 0.
    def min_reach(self):
        return 0

    # STUB: Natural reach. Depends on size.
    def max_reach(self):
        return 0
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
            if self.exhausted() is True:
                ST = (ST + 1) / 2
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
        if self.effects.get("Stun") is not None:
            status_mod -= 4

        posture_mod = postures[self.posture][1]

        retreat_mod = 0
        if retreat is True:
            retreat_mod += 3

        dodge = self.Speed()/4 + 3 + status_mod + posture_mod + retreat_mod# /4 because no /4 in speed.

        # Penalty from reeling: halve dodge.
        if self.reeling() is True:
            dodge = (dodge + 1) / 2

        # Penalty from exhaustion: halve dodge.
        if self.exhausted() is True:
            dodge = (dodge + 1) / 2

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
        for slot, appearance, trait, trait_level, attack_data, weapon in self.parries:
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

    # Whether you're so injured as to be reeling.
    def reeling(self):
        if self.HP() < self.MaxHP()/3:
            return True
        else:
            return False

    # Whether you're so fatigued as to be exhausted.
    def exhausted(self):
        if self.FP() < self.MaxFP()/3:
            return True
        else:
            return False
   
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
            log.add("%s is knocked unconscious!" % self.appearance())
            self.knockout()

        if attack.get("knockdown") is not None:
            self.knockdown()

        if attack.get("dropped items") is not None:
            self.drop_all_held()

        if attack.get("stun") is not None and self.conscious() is True:
            self.effects["Stun"] = attack["stun"]
            # TODO: Change message.
            log.add("%s is stunned!" % self.appearance())

        # Handle shock (potentially from multiple sources.)
        if attack.get("shock") is not None:
            shock = self.effects.get("Shock", 0)
            self.effects["Shock"] = min(4, shock + attack["shock"])

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
            log.add(describe("%s has been slain!" % self.name))
        self.cell().put(self.corpse())
        return self.check_dead()

    # Generate a corpse of ourselves.
    def corpse(self):
        return Corpse(self)

    #
    # INVENTORY:
    #

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

            log.add("%s picks up the %s." % (self.appearance(), commas(appearances, False)))

    # TODO: Support dropping to any cell
    # 'Forcibly' drop a specific inventory item.
    # Returns false if the item wasn't found in the player's inventory.
    def _drop(self, item):
        assert self._unequip(item) is True, "Lost an item: it was removed, but not returned."
        self._remove(item)
        self.cell().put(item)
        log.add("%s drops a %s." % (self.appearance(), item.appearance()))
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
        for loc in self.body.locs.values():
            itemlist = loc.items()
            while itemlist:
                self._drop(itemlist.pop())

    # TODO: Less hack-ish.
    def drop_all_held(self):
        if self.is_holding_items() is False:
            return False
        for loc in self.body.locs.values():
            for appearance, itemlist in loc.held.items():
                for item in itemlist:
                    self._drop(item)
        # TODO: Change message.
        #log.add("%s drops its items!" % self.appearance())
            
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
            log.add("%s can't equip the %s right now." % (self.appearance(), item.appearance()))
            return False

        # HACK: Remove the equipped item from inventory.
        self._remove(item)
        self.check_weapons()
        # HACK: Later add a flag.
        if self.controlled is True:
            log.add("%s equips the %s." % (self.appearance(), item.appearance()))
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
            log.add("%s unequips the %s." % (self.appearance(), item.appearance()))

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
    # ACTION PROCESSING:
    #

    def action(self, methods, act, **kwargs):
        # Setup keyword arguments.
        kwargs = self.prep_kwargs(kwargs)

        # Get the results of processing the action.
        results = act.process(methods, **kwargs)

        # TODO: Return the full results!
        # A full attempt returns len(methods) * len(self.definition) results.
        if len(results) != len(act.definition) * len(methods):
            return False

        # If we did reach the end, we only need to check the last primitive.
        return results[-1][0]


    # Action helper functions - shorthand for calls to self.action().

    # Check whether an action is believed to be attemptable.
    def believe(self, act, **kwargs):
        return self.action(["believe"], act **kwargs)

    # Check whether an action can actually be attempted.
    def can(self, act, **kwargs):
        return self.action(["can"], act, **kwargs)

    # Check whether an action can actually be attempted, and if so, attempt it.
    def attempt(self, act, **kwargs):
        return self.action(["can", "attempt"], act, **kwargs)

    #
    # ACTION PRIMITIVE CALLBACKS:
    #

    # STUB
    def can_touch(self, target):
        return True

    # STUB
    def can_grasp(self, target):
        return True

    # STUB
    def can_ready(self, target):
        return True

    # Return whether the actor can touch the target with the item.
    # TODO: Enhanced return values.
    def can_contact(self, target, item):
        # TODO: Restructure attack option structure so that items can figure
        # this out based on how they are being held
        target_dist = self.dist(target)
        attack_option = self.attack_options[self.attack_option]
        min_reach = attack_option[3][0] + self.min_reach()
        max_reach = attack_option[3][-1] + self.max_reach()

        # Check whether it's too close to reach
#        min_reach = self.min_reach() + item.min_reach(self.attack_option)
        if target_dist < min_reach:
            return (False,)

        # Check whether it's too far to reach
#        max_reach = self.max_reach() + item.max_reach(self.attack_option)
        if target_dist > max_reach:
            return (False,)
        return (True,)

    # STUB
    def can_use_at(self, target, item):
        return True

    # STUB
    def attempt_touch(self, target):
        return True

    # STUB
    def attempt_grasp(self, target):
        return True

    # STUB
    def attempt_ready(self, target):
        return True

    # STUB
    def attempt_contact(self, target, item):
        return True

    # STUB
    def attempt_use_at(self, target, item):
        return True

    #
    # INFORMATION DISPLAYS:
    #

    def appearance(self):
    # TODO: Add real coloring support.
#        if self.controlled is True:
#            return "<green-black>" + self.name + "</>"
#        else:
            return self.name

    # Display the attack line for the current combination of weapon/attack option.
    # TODO: Multiple attacks.
    def attackline(self):
        weapon = self.weapons[self.weapon]
        attack_option = self.attack_options[self.attack_option]
        return weapon, attack_option

    # Returns a list of lines to go into a character sheet.
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
    def paperdoll(self):
        return self.body.paperdoll()

    # Show a screen.
    def screen(self, screenname, arguments=None, screenclass=None):
        self.map.screen(screenname, arguments, screenclass)

    # STUB:
    def cursor_color(self):
        return self.dialogue_color()

    def dialogue_color(self):
        if self.controlled is True:
            return "green-black"
        else:
            return "red-black"

    #
    # GENERATION AND IMPROVEMENT:
    #

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