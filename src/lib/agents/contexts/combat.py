# TODO: Make the keys more consistent.
from src.lib.util.define import *
from src.lib.util.dice import *
from src.lib.generators.text.combat import combat

# KEY DEFINITIONS:
# attacker: who launched the attack
# target: who the attack was intended for
# defender: who actually received the attack
# location: which of the defender's parts was hit
#
# attack name: "swing", "punch", "bite", etc.
# attack stats: the "attack line" of the (weapon x skill x attack option)
# damage type: cr, cut, etc.
# damage roll: the damage a weapon gets to roll, like 1d-3
#
# basic damage: the rolled number on a damage roll
# basic damage blocked: amount of basic damage blocked by DR
# penetrating damage: amount of basic damage not blocked
# multiplier: the damage mod for that (damage type x location)
# wound: injury to a location: (penetrating damage x multiplier)
# injury: the amount of damage from a wound that affects HP total

# major wound: whether the wound was major
# crippling wound: whether the wound was enough to cripple in one hit
# dismembering wound: whether the wound was enough to dismember in one hit
# crippled: whether this attack pushed the limb over into "crippled"
# dismembered: whether this attack pushed the limb over into "dismembered"
# sever: whether to sever the limb during cleanup (dismembering wound + cut damage)

# TODO: Definitions for everything!

# For convenient reference, attack stats are structured as such:
#     skill          name     dmg    dtype  reach parry minST hands
#  "Broadsword" : { "swing" : ("sw+1", "cut", (1,), 0, 10, 1),

# TODO: Make this actually a type of Context!
class CombatContext(object):

    maneuver_id = 0

    def __init__(self):
        self.attacks = {}
        self.results = {}

    # TODO: Better way of getting IDs
    @staticmethod
    def get_maneuver_id():
        CombatContext.maneuver_id += 1
        return CombatContext.maneuver_id

    """Attack getter methods."""

    def get_attacks(self):
        return self.attacks.items()

    """Attack setter methods."""

    def add_attack(self, attacker, target, weapon, wielding_mode):
        # Wielding mode, for now:
        #  0      1        2      3      4      5       6,     7
        # trait, name, damage, d.type, reach, parry, min ST, hands
        trait, name, damage, damage_type, reach, parry, min_st, hands = wielding_mode
        min_reach, max_reach = weapon.call("Wielded", "get_reach").get_result()

        # TODO: better way of keying these
        maneuver = CombatContext.get_maneuver_id()

        self.attacks[maneuver] = {
            "attacker" : attacker,
            "target" : target,
            "weapon" : weapon,
            "trait_name" : trait,
            "attack_name" : name,
            "damage_roll" : damage,
            "damage_type" : damage_type,
            "min_reach" : min_reach,
            "max_reach" : max_reach,
         }

    """Attack processing methods."""

    def process_attacks(self):
        # TODO: different loop structure. Generator based?
        hits = []
        while len(self.attacks) > 0:
            maneuver, attack = self.attacks.popitem()

            # Attack roll.
            attack["attack_check"], attack["attack_margin"] = attack["attacker"].sc(attack["trait_name"])

            # TODO: defender not always == target, e.g., crit fails or cover
            attack["defender"] = attack["target"]
            # TODO: better way of choosing location
            attack.setdefault("location", attack["defender"].call("Body", "get_random_part").get_result())

            # Early exit if missed.
            if attack["attack_check"] < TIE:
                attack["outcome"] = "missed"
                self.results[maneuver] = attack
            else:
                attack["outcome"] = "hit"
                hits.append((maneuver, attack))

        landed = []
        for maneuver, attack in hits:
            # TODO: Make attacks and defenses into objects.
            # Example defense:
            # ('parry', <Natural object>, 15, (-1, 0))

            defense = attack["defender"].call("Combat", "get_defense", attack).get_result()

            if defense is None:
                defense = ('none', None, None, None)
            attack["defense_name"],\
            attack["defense_weapon"],\
            attack["defense_level"],\
            attack["retreat_position"] = defense

            # Let the defender retreat and store whether it was a success
            if attack.get("retreat_position"):
                if attack["defender"].move(attack["retreat_position"]):
                    attack["defender"].call("Status", "set_status", "Retreat", attack["attacker"])
                    attack["retreat"] = True
                else:
                    attack["retreat"] = False

            # Check whether the defense succeeded
            # TODO: componentize...
            if attack["defense_name"] != 'none':
                attack["defense_check"], attack["defense_margin"] = sc(attack["defense_level"])
                if attack["defense_check"] > TIE:
                    attack["outcome"] = "defended"
                    self.results[maneuver] = attack
                    continue

            # Fallthrough: they didn't provide a defense, or didn't defend.
            attack["outcome"] = "landed"
            landed.append((maneuver, attack))

        for maneuver, attack in landed:
            # Didn't defend? Generate damage for the attacks.
            attack["basic_damage"] = attack["attacker"].damage(attack["damage_roll"])
            attack["location"].prepare_hurt(attack)
            attack["defender"].prepare_hurt(attack)
            self.results[maneuver] = attack

        # Do everything that occurs at the *end* of this attack sequence.
        for maneuver, attack in landed:
            # Cause wounds to limbs.
            # TODO: Better tracking of wounds.
            if attack.get("wound") > 0:
                attack["location"].hurt(attack)
            # Cause wounds to actors.
            if attack.get("injury") > 0:
                attack["defender"].hurt(attack)
            # Check for dead actors.
            # TODO: Store text generation information here.
            if attack["defender"].is_dead():
                attack["defender"].process_death()

    # TODO: Move to generator file.
    # TODO: Generate a message (using text generator)
    def display(self):
        lines = []
        for attack in self.results.values():
            lines.extend(combat(attack))
        return lines