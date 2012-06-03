from dice import *
from generators.text.describe import describe
from text import *

def combat(attack):
    if attack.get("injury") is not None:
        formula = "%s [(%s-%s)*%s]" % (attack["injury"], attack["basic damage"], attack["basic damage blocked"], attack["multiplier"])
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
        string = "%s @dmg-%s-%s@ %s in the %s for %s" % (attack["attacker"].appearance(), attack["damage type"], attack["attack option"], attack["target"].appearance(), attack["location"].appearance(), formula)
        if wounds:
            string += " (%s!)" % commas(wounds)
    elif attack.get("defense-check") == SUCC:
        string = "%s @def@ %s" % (attack["target"].appearance(), attack["attacker"].appearance())
    else:
        string = "%s @miss@ %s" % (attack["attacker"].appearance(), attack["target"].appearance())

    return describe(string)
