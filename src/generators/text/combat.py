from dice import *
from generators.text.describe import describe
from text import *

def combat(attack):
    # Hit and did 0 or more points of injury.
    if attack.get("injury") is not None:
        formula = "%s [(%s-%s)*%s]" % (attack["injury"], attack["basic damage"], attack["basic damage blocked"], attack["multiplier"])

        # Damage level tokens
        if attack.get("dismembering major wound") is not None:
            damage_level = "dismember"
        elif attack.get("crippling major wound") is not None:
            damage_level = "cripple"
        elif attack.get("major wound") is not None:
            damage_level = "wound"
        elif attack["injury"] > 1:
            damage_level = "injure"
        elif attack["injury"] == 1:
            damage_level = "scratch"
        else:
            damage_level = "none"

        # DEBUG: Explicitly list wounds
        wounds = []
        if attack.get("major wound") is not None:
            wounds.append("major")
        if attack.get("crippled") is not None:
            wounds.append("crippled")
        if attack.get("dismembered") is not None:
            if attack.get("severed") is not None:
                wounds.append("severed")
            else:
                wounds.append("dismembered")

        # TODO: Have other kinds of basic strings.
        string = "%s @dmg-%s-%s-%s@ %s in the %s for %s" % (attack["attacker"].appearance(), damage_level, attack["damage type"], attack["attack name"], attack["target"].appearance(), attack["location"].appearance(), formula)
        if wounds:
            string += " (%s!)" % commas(wounds)

    # Hit, but the target defended.
    elif attack.get("defense-check") > TIE:
        # Defense level tokens
        margin = attack["defense-margin"]

        # Critical successes
        if attack["defense-check"] == CRIT_SUCC:
            defense_level = "crit-"
            if margin >= 6:
                defense_level += "trivial"
            elif margin >= 4:
                defense_level += "easy"
            elif margin >= 2:
                defense_level += "normal"
            elif margin >= 1:
                defense_level += "hard"
            elif margin == 0:
                defense_level += "difficult"
            # If your roll only succeeded because it was a crit :D
            else:
                defense_level += "insane"
        # Normal successes
        else:
            if margin >= 6:
                defense_level = "trivial"
            elif margin >= 4:
                defense_level = "easy"
            elif margin >= 2:
                defense_level = "normal"
            elif margin == 1:
                defense_level = "hard"
            else:
                defense_level = "difficult"

        string = "%s @def-%s-%s@ against %s" % (attack["target"].appearance(), attack["defense"], defense_level, attack["attacker"].appearance())
    # Miss!
    else:
        string = "%s @miss@ %s" % (attack["attacker"].appearance(), attack["target"].appearance())

    return describe(string)
