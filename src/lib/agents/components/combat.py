from collections import deque
from operator import itemgetter
import random

from src.lib.agents.components.action import Action
from src.lib.agents.contexts.combat import CombatContext
from src.lib.agents.contexts.context import action_context, command_context
from src.lib.agents.components.component import Component
from src.lib.agents.components.phase import Phase

from src.lib.util.command import Command, CommandRegistry
from src.lib.util.debug import debug, die
from src.lib.util.define import *
from src.lib.util.hex import *
from src.lib.util.log import Log
from src.lib.util.mixin import Mixin

"""Actions."""

"""Offensive combat actions."""

class AttackWithWielded(Action):
    """Attack a target with a weapon wielded in a manipulator."""

    # Phase(required=): whether checking this condition is required for future phases
    # ctx(): override __call__ to check whether all currently required phases are met
    # ctx.start_rollback(): start tracking the phases being run
    # ctx.do_rollback(): iterate through phases since the rollback started in reverse
    #                    order, yielding the "un" version of each phase (e.g., "unwield)

    @action_context
    def get_phases(self, ctx):
        ctx.update_arguments(use="attack")
        # ctx.update_aliases(weapon="target")

        # Attacking requires a readied weapon.
        yield Phase("touch", "weapon", "manipulator", weapon="target")
        if ctx(): yield Phase("grasp", "weapon", "manipulator", weapon="target")
        if ctx(): yield Phase("ready", "weapon", "manipulator", weapon="target")

        if ctx():
            # ctx.start_rollback()
            # ctx.update_aliases(weapon="instrument")

            yield Phase("contact", "target", "weapon", "manipulator", weapon="instrument", required=False)
            # any number of these fallthrough if not satisfied:
            # if ctx(): yield ...
            if ctx(): yield Phase("use_at", "target", "weapon", "manipulator", "use", weapon="instrument")
            # does the reverse operation of any operations since the rollback started
            # for phase in ctx.do_rollback():
            #     yield phase

    # # Use a ready item to disarm.
    # # n.b. - The 'target' is the other item!
    # "disarm" : (
    #     ("touch", "item"),
    #     ("grasp", "item"),
    #     ("lift", "item"),
    #     ("handle", "item"),
    #     ("ready", "item"),
    #     ("contact", "target", "item"),
    #     ("use_at", "target", "item")
    # ),

"""Defensive combat actions."""

    # # Use a ready item to parry an attack.
    # # n.b. - The 'target' is the other item!
    # "parry" : (
    #     ("touch", "item"),
    #     ("grasp", "item"),
    #     ("lift", "item"),
    #     ("handle", "item"),
    #     ("ready", "item"),
    #     ("contact", "target", "item"),
    #     ("use_at", "target", "item")
    # ),

"""Commands."""

class Attack(Command):
    description = "attack"
    defaults = ("a",)

    @command_context
    def get_actions(self, ctx):
        yield AttackWithWielded

CommandRegistry.register(Attack)

class Combat(Component):
    """Allows an Agent to engage in combat with other Agents."""
    commands = []

    def __init__(self, owner):
        super(Combat, self).__init__(owner)

        self.weapons = deque()
        self.attack_options = deque()
        self.parries = deque()

    def trigger(self, *triggers):
        """Respond to triggers."""
        if "rebuild" in triggers:
            self.update_weapons()

    """Weapon getter methods."""

    def get_active_weapon(self):
        """Return this Component's active weapon."""
        if self.weapons:
            return self.weapons[0]

    def get_default_weapon(self, context):
        """Returns the weapon to default to within a Context."""
        weapon = self.get_active_weapon()
        if not weapon:
            self.update_weapons()
            weapon = self.get_active_weapon()
            if not weapon:
                die("After update, had no active weapon from list of weapons: %s" % self.weapons)
        return weapon

    def get_weapons(self):
        """Yield this Component's weapons."""
        for weapon in self.weapons:
            yield weapon

    """Weapon setter methods."""

    def update_weapons(self, natural=True, wielded=True):
        self.weapons = deque()

        for weapon in self.owner.values("Body", "get_natural_weapons"):
            if not weapon: die("Component %s tried to add an invalid natural weapon: %s." % (self, weapon))
            self.weapons.append(weapon)
        for weapon in self.owner.values("Manipulation", "get_wielded"):
            if not weapon: die("Component %s tried to add an invalid equipped weapon: %s." % (self, weapon))
            self.weapons.append(weapon)

    """Attack processing methods."""

    def process_attack(self, target, weapon, manipulator):
        """Process a single attack."""
        if weapon != self.get_active_weapon():
            die("Tried to attack with inactive weapon %s" % weapon)
        if not manipulator.is_wield(weapon):
            die("Tried to attack with unwielded weapon %s" % weapon)

        wielding_mode = weapon.call("Wielded", "get_wielding_mode").get_result()

        if not wielding_mode:
            die("Weapon %s had no wielding mode" % weapon)

        ctx = CombatContext()
        ctx.add_attack(self.owner, target, weapon, wielding_mode)
        ctx.process_attacks()

        # TODO: Replace with check for whether it's interesting.
        for line in ctx.display():
            Log.add(line)

        return True

    """Defense getter methods."""

    # TODO: Defense object
    def get_defense(self, attack):
        """Return the best defense to an attack."""
        defenses = sorted([defense for defense in self.get_defenses(attack)], key=itemgetter(2), reverse=True)
        # TODO: Apply logic here to pick best defense
        return defenses[0]

    # TODO: Defense object
    def get_defenses(self, attack):
        """Yield all possible defenses to an attack."""
        if self.can_defend():
            can_retreat, retreat_positions = self.choose_retreat(attack)
            # for block in self.get_blocks(can_retreat, retreat_positions):
            #     yield block
            for dodge in self.get_dodges(can_retreat, retreat_positions):
                yield dodge
            for parry in self.get_parries(can_retreat, retreat_positions):
                yield parry

    # # TODO: Block object
    # def get_blocks(self, can_retreat, retreat_positions):
    #     yield "block", blocking, block_value, retreat_position

    # # STUB: Currently always returns highest parry.
    # def Parry(self, retreat=False, list=False):
    #     if self.can_defend() is False:
    #         return None

    #     status_mod = 0
    #     if self.get("Status", "Stun"):
    #         status_mod -= 4

    #     posture_mod = postures[self.posture][1]

    #     parries = []
    #     for slot, appearance, trait, trait_level, attack_data, weapon in self.get_parries():
    #         # Get the parry modifier from the attack data.
    #         parry_mod = attack_data[4]
    #         # HACK: Weapon balance.
    #         if isinstance(parry_mod, tuple):
    #             parry_mod, balanced = parry_mod

    #         # Recalculate trait level for this weapon.
    #         trait_level = self.trait(trait, False)

    #         # TODO: Check whether the skill has had points paid for it (imp. retreat)
    #         if retreat is True:
    #             retreat_mod = 1
    #             if trait in skills.skill_list:
    #                 retreat_mod = skills.skill_list[trait].get("retreat", 1)
    #         else:
    #             retreat_mod = 0

    #         parry = 3 + trait_level/2 + parry_mod + status_mod + posture_mod + retreat_mod
    #         parries.append((slot, appearance, trait, parry, attack_data, weapon))

    #     if list is True:
    #         return sorted(parries, key=itemgetter(3), reverse=True)
    #     else:
    #         if parries:
    #             return sorted(parries, key=itemgetter(3), reverse=True)[0][3]

    # TODO: Dodge object
    # TODO: Multiple kinds of dodge (e.g., normal vs. acrobatic)
    def get_dodges(self, can_retreat, retreat_positions):
        dodging = self.owner

        status_mod = -4 if dodging.get("Status", "Stun") else 0
        # ugh...
        posture_mod = postures[dodging.posture][1]

        # TODO: Choose intelligently
        retreat_position = random.choice(retreat_positions) if retreat_positions else None
        # TODO: per-skill
        retreat_mod = 3 if can_retreat else 0

        # trait-ize
        # /4 is because no /4 is performed in Speed().
        dodge_value = self.owner.Speed()/4 + 3 + status_mod + posture_mod + retreat_mod

        # Penalty from reeling: halve dodge.
        if dodging.get("Status", "Reeling"):
            dodge_value = (dodge_value + 1) / 2

        # Penalty from exhaustion: halve dodge.
        if dodging.get("Status", "Exhausted"):
            dodge_value = (dodge_value + 1) / 2

        yield "dodge", dodging, dodge_value, retreat_position

    # TODO: Parry object
    def get_parries(self, can_retreat, retreat_positions):
        """Yield available parries."""
        for weapon in self.weapons:
            parry_value, retreat_position = weapon.call("Wielded", "get_parry", can_retreat, retreat_positions).get_result()
            if parry_value:
                yield "parry", weapon, parry_value, retreat_position

#     def check_weapons(self):
#         weapons = []
#         parries = []
#         for slot, loc in self.get("Equipment", "weapons"):
#             if loc is None:
#                 continue
#             for appearance, weaponlist in loc.weapons().items():
#                 for weapon in weaponlist:
#                     for trait, attack_options in weapon.attack_options.items():
#                         trait_level = self.trait(trait)
#                         if trait_level > 0: # HACK: Magic number!
#                             weapons.append((slot, appearance, trait, trait_level, weapon))
#                             for attack_data in attack_options:
#                                 parry_mod = attack_data[4]
#                                 if parry_mod is not None:
#                                     # HACK: Handle balanced status.
#                                     if isinstance(parry_mod, tuple):
#                                         parry_mod, balanced = parry_mod
#                                     # TODO: Handle U weapons.
#                                     parries.append((slot, appearance, trait, trait_level + parry_mod, attack_data, weapon))
#         self.weapons = sorted(weapons, key=itemgetter(3,0,2,1), reverse=True)
#         self.parries = sorted(parries, key=itemgetter(3,0,2,1), reverse=True)

    """Defense helper methods."""

    def can_defend(self):
        if not self.owner.can_act():
            return False
        return True

    def can_retreat(self):
        if not self.owner.can_act():
            return False
        return True

    # TODO: Move to AI!
    # TODO: Componentize
    def choose_retreat(self, attack):
        """Given an attack, return retreat bonus and retreat options."""

        # No sleep-dodging!
        if not self.can_retreat():
            return False, None

        retreated_against = self.owner.get("Status", "Retreat")

        # Already retreated against this attacker - still get a bonus.
        if retreated_against == attack["attacker"]:
            return True, None

        # Already retreated, but not against this attacker. No bonus.
        elif retreated_against:
            return False, None

        # Otherwise, we can retreat if we can find a spot to move to.
        # TODO: Handle sideslips and slips (dist == 0, dist == -1)
        retreat_distance = 1

        # Must retreat to 1 further away than the attack came from
        cells = perimeter(attack["attacker"].pos, self.owner.dist(attack["attacker"]) + retreat_distance)

        # TODO: Allow retreats > 1
        options = []
        for cell in cells:
            # TODO: Check whether we can move properly here
            if dist(self.owner.pos, cell) == 1 and self.owner.valid_move(cell):
                options.append(cell)
        if options:
            return True, options
        else:
            return False, None

#     # TODO: Support more than one weapon
#     # TODO: Oh god this is terrible
#     def get_view_data(self):
#         """Get view data about the chosen weapon and attack option."""
#         weapon = self.weapons[self.weapon]
#         attack_option = self.attack_options[self.attack_option]

#         return weapon, attack_option

#     # TODO: Move all combat 'thinking' into src/lib/actor/ai/combat.

#     # Display the attack line for the current combination of weapon/attack option.
#     # TODO: Multiple attacks.
#     def attackline(self):
#         weapon = self.weapons[self.weapon]
#         attack_option = self.attack_options[self.attack_option]
#         return weapon, attack_option

#     def choose_weapon(self, scroll):
#         weapons = self.get
# #        assert len(self.weapons) != 0, "Had 0 weapons: %s" % self.__dict__
#         self.weapon += scroll
#         if self.weapon >= len(self.weapons):
#             self.weapon = 0
#         if self.weapon < 0:
#             self.weapon = len(self.weapons) - 1

#         weapon = self.weapons[self.weapon]
#         slot, appearance, trait, trait_level, item = weapon
#         self.attack_options = item.attack_options[trait]
#         self.attack_option = 0

#     def choose_attack_option(self, scroll):
#         assert len(self.attack_options) != 0, "Had 0 attack options: %s" % self.__dict__
#         self.attack_option += scroll
#         if self.attack_option >= len(self.attack_options):
#             self.attack_option = 0
#         if self.attack_option < 0:
#             self.attack_option = len(self.attack_options) - 1

#     # Find eligible weapons.
#     # TODO: Rewrite.
#     def check_weapons(self):
#         weapons = []
#         parries = []
#         for slot, loc in self.get("Equipment", "weapons"):
#             if loc is None:
#                 continue
#             for appearance, weaponlist in loc.weapons().items():
#                 for weapon in weaponlist:
#                     for trait, attack_options in weapon.attack_options.items():
#                         trait_level = self.trait(trait)
#                         if trait_level > 0: # HACK: Magic number!
#                             weapons.append((slot, appearance, trait, trait_level, weapon))
#                             for attack_data in attack_options:
#                                 parry_mod = attack_data[4]
#                                 if parry_mod is not None:
#                                     # HACK: Handle balanced status.
#                                     if isinstance(parry_mod, tuple):
#                                         parry_mod, balanced = parry_mod
#                                     # TODO: Handle U weapons.
#                                     parries.append((slot, appearance, trait, trait_level + parry_mod, attack_data, weapon))
#         self.weapons = sorted(weapons, key=itemgetter(3,0,2,1), reverse=True)
#         self.parries = sorted(parries, key=itemgetter(3,0,2,1), reverse=True)

#         # HACK: Shouldn't always reset like this.
#         self.parry = 0
#         self.choose_weapon(0)

#     # Function called to produce a simple, single attack maneuver.
#     # TODO: Rewrite.

#     # STUB: Handle movement on a retreat.
#     def retreat(self, attack):
#         self.move(attack["retreat position"])

#     # Returns true if the currently preferred weapon has reach.
#     # TODO: Remove this function.
#     def preferred_reach(self, dist):
#         attack_option = self.attack_options[self.attack_option]
#         min_reach = attack_option[3][0]
#         max_reach = attack_option[3][-1]
#         if dist >= min_reach and dist <= max_reach:
#             return True
#         else:
#             return False

#     # STUB: Natural reach. Always 0.
#     def min_reach(self):
#         return 0

#     # STUB: Natural reach. Depends on size.
#     def max_reach(self):
#         return 0