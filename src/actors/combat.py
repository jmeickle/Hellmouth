# TODO: Make the keys more consistent.
from define import *
from dice import *
from hex import *
from generators.text.describe import describe

# For convenient reference, attack lines are structured as such:
#     skill          name     dmg    dtype  reach parry minST hands
#  "Broadsword" : { "swing" : ("sw+1", "cut", (1,), 0, 10, 1),

class CombatAction:
    def __init__(self, attacks):
        self.attacks = attacks
        self.hits = {}
        self.results = {
            "missed" : {},
            "defended" : {},
            "landed" : {},
        }

    # Decide which attacks are or aren't going to work, but don't actually
    # do anything to actors yet.
    def setup(self):
        # Key ripostes / etc. off of maneuver (a hashable tuple)
        while len(self.attacks) > 0:
            maneuver, attack = self.attacks.popitem()
            attack["attackline"] = attack["item"].attack_options[attack["skill"]][attack["attack option"]]

            if self.reach(attack) is False:
                continue

            # Attack roll
            attack["attack-check"], attack["attack-margin"] = attack["attacker"].sc(attack["skill"])

            # Early exit.
            if attack["attack-check"] == FAIL or attack["attack-check"] == CRIT_FAIL:
                self.results["missed"][maneuver] = attack
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
                attack["defense"] = "Dodge"#preferred_defense(self.attack)
                attack["defense-check"], attack["defense-margin"] = sc(attack["target"].stat(attack["defense"]))

                if attack["defense-check"] == SUCC:
                    self.results["defended"][maneuver] = attack
                else:
                    # Generate damage for the attack
                    attack["damage"] = attack["attackline"][0]
                    attack["damage type"] = attack["attackline"][1]
                    attack["damage rolled"] = attack["attacker"].damage(attack["damage"])
                    #attack["damage done"], attack["damage blocked"] =
                    attack["target"].hit(attack)
                    self.results["landed"][maneuver] = attack
                    # TODO: Trigger effects that depend on hitting, etc.

    def cleanup(self):
        for maneuver, attack in self.results["landed"].items():
            if attack["target"].check_dead() is True:
                attack["target"].die()

    # Check whether the attack is within the weapon's valid reach.
    def reach(self, attack, actual=False):
        distance = dist(attack["attacker"].pos, attack["target"].pos)
        min_reach = attack["attackline"][2][0]
        # HACK: Remove when sharing the same hex is implemented.
        max_reach = 1+ attack["attackline"][2][-1]

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
        for attack in self.results["landed"].values():
            string = describe("%s @dmg-%s-%s@ %s for %s" % (attack["attacker"].name, attack["damage type"], attack["attack option"], attack["target"].name, attack["damage done"]))
            lines.append(string)
        return lines
