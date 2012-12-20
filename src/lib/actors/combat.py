# TODO: Make the keys more consistent.
from define import *
from dice import *
from hex import *
from generators.text.combat import combat

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

class CombatAction:
    def __init__(self, attacks):
        self.attacks = attacks
        self.hits = {}
        self.results = {}

    # Decide which attacks are or aren't going to work, but don't actually
    # do anything to actors yet.
    def setup(self):
        # Key ripostes / etc. off of maneuver (a hashable tuple)
        while len(self.attacks) > 0:
            maneuver, attack = self.attacks.popitem()

# TODO: Remove?
#            if self.reach(attack) is False:
#                continue

            # Attack roll
            attack["attack-check"], attack["attack-margin"] = attack["attacker"].sc(attack["skill"])

            # Early exit.
            if attack["attack-check"] < TIE:
                attack["status"] = "missed"
                self.results[maneuver] = attack
            else:
                hits = self.hits.get(attack["target"], [])
                hits.append((maneuver, attack))
                self.hits[attack["target"]] = hits

        if len(self.hits) > 0:
            return True

    # Attack(s) are stored relative to the defender. The defender chooses a
    # response - or multiple responses - based on the attack(s).
    def fire(self):
        for defender, hits in self.hits.items():
            for maneuver, attack in hits:
                # Permit the actor to decide which defense they want to use.
                attack["target"].choose_defense(attack)
                if attack.get("defense") is not None:
                    attack["defense-check"], attack["defense-margin"] = sc(attack["defense level"])
                    if attack["defense-check"] > TIE:
                        attack["status"] = "defended"
                        self.results[maneuver] = attack
                        continue

                # Didn't defend? Generate damage for the attack.
                attack["damage roll"] = attack["attack stats"][0]
                attack["damage type"] = attack["attack stats"][1]
                attack["basic damage"] = attack["attacker"].damage(attack["damage roll"])
                if attack.get("location") is None:
                    attack["location"] = attack["target"].randomloc()
                attack["location"].prepare_hurt(attack)
                attack["target"].prepare_hurt(attack)
                attack["status"] = "hit"
                self.results[maneuver] = attack

    # Do everything that occurs at the *end* of this attack sequence.
    # Examples: falling, retreating, shock, etc.
    def cleanup(self):
        for maneuver, attack in self.results.items():
            if attack.get("retreat position") is not None:
                attack["target"].retreat(attack)
            # Cause wounds to limbs.
            # TODO: Better tracking of wounds.
            if attack.get("wound") > 0:
                attack["location"].hurt(attack)
            # Cause wounds to actors.
            if attack.get("injury") > 0:
                attack["target"].hurt(attack)
            # Check for dead actors.
            if attack["target"].check_dead() is True:
                attack["target"].die()

    # TODO: Duplicated code with actor reach method.
    # Check whether the attack is within the weapon's valid reach.
    def reach(self, attack, actual=False):
        distance = dist(attack["attacker"].pos, attack["target"].pos)
        min_reach = attack["attack stats"][3][0]
        max_reach = attack["attack stats"][3][-1]

        # TODO: Check current reach on weapons that require shifting distance.
        # TODO: Different return values
        if distance < min_reach:
            return False
        if distance > max_reach:
            return False

        # The attack's reach is the current dist.
        attack["reach"] = distance
        return True

    # TODO: Move to generator file.
    # TODO: Generate a message (using text generator)
    def display(self):
        lines = []
        for attack in self.results.values():
            lines.extend(combat(attack))
        return lines