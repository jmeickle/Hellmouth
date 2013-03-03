from collections import deque

from src.lib.agents.components.action import Action
from src.lib.agents.components.component import Component
from src.lib.util.command import Command, CommandRegistry
from src.lib.util.mixin import Mixin

"""Actions."""

"""Offensive combat actions."""

class AttackWithWielded(Action):
    """Attack a target with a weapon wielded in a manipulator."""
    sequence = [
        ("touch", "weapon"),
        ("grasp", "weapon"),
        # ("lift", "weapon"),
        # ("handle", "weapon"),
        ("ready", "weapon"),
        ("contact", "target", "weapon"),
        ("use_at", "target", "weapon")
    ]

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

CommandRegistry.register(Attack)

class Combat(Component):
    """Allows an Agent to engage in combat with other Agents."""

    def __init__(self, owner):
        super(Combat, self).__init__(owner)

        self.weapons = []
        self.weapon = 0
        self.attack_options = []
        self.attack_option = 0
        self.parries = []
        self.parry = 0

    def get_weapons(self):
        return self.owner.get("Equipment", "usable_weapons") + self.owner.get("Body", "usable_weapons")

    # TODO: Support more than one weapon
    # TODO: Oh god this is terrible
    def get_view_data(self):
        """Get view data about the chosen weapon and attack option."""
        weapon = self.weapons[self.weapon]
        attack_option = self.attack_options[self.attack_option]

        return weapon, attack_option

    # TODO: Move all combat 'thinking' into src/lib/actor/ai/combat.

    # Display the attack line for the current combination of weapon/attack option.
    # TODO: Multiple attacks.
    def attackline(self):
        weapon = self.weapons[self.weapon]
        attack_option = self.attack_options[self.attack_option]
        return weapon, attack_option

    def choose_weapon(self, scroll):
        weapons = self.get
#        assert len(self.weapons) != 0, "Had 0 weapons: %s" % self.__dict__
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

    # Find eligible weapons.
    # TODO: Rewrite.
    def check_weapons(self):
        weapons = []
        parries = []
        for slot, loc in self.get("Equipment", "weapons"):
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
    # TODO: Rewrite.
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
    # TODO: Rewrite.
    def _attack(self, maneuvers):
        attacks = {}

        for maneuver in maneuvers:
            # NOTE: This will fail when rapid strikes come into play, of course!
            # Same target, item, skill, *and* attack option.
            target, item, skill, attack_option = maneuver
            distance = dist(self.pos, target.pos)

            # TODO: Improve how this is called. attack_option[0] ?
            # Instantiate this action's object.
            attack = action.Attack

            # Continue to the next maneuver if we failed our attempt.
            # TODO: Analyze failure reason here instead
            if self.attempt([attack], target=target, item=item) is False:
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
            Log.add(line)
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