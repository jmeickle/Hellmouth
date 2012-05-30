from dice import *
from generators.text.describe import describe

def combat(attack):
    if attack.get("damage done") is not None:
        formula = "%s [(%s-%s)*%s]" % (attack["damage done"], attack["damage rolled"], attack["damage blocked"], attack["multiplier"])
        string = "%s @dmg-%s-%s@ %s for %s" % (attack["attacker"].name, attack["damage type"], attack["attack option"], attack["target"].name, formula)
    elif attack.get("defense-check") == SUCC:
        string = "%s @def@ %s" % (attack["target"].name, attack["attacker"].name)
    else:
        string = "%s @miss@ %s" % (attack["attacker"].name, attack["target"].name)

    return describe(string)
