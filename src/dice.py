import random
import re

SUCC = 1
TIE = 0
FAIL = -1

# Basic coinflip
def flip():
    if random.randint(0, 1) == 1:
        return SUCC
    else:
        return FAIL

# Roll an n-sized die.
def r1d(n):
    return random.randint(1, n)

# Basic d6 roll
def r1d6():
    return random.randint(1, 6)

# Basic 3d6 roll
def r3d6():
    return sum(roll(r1d6, 3))

# Return n rolls of either d6 or 3d6, with per-roll modifiers
def roll(func, n, per=0):
    return [func() + per for x in range(n)]

# Skill check
# TODO: Handle critical successes/failures
def sc(skill, mod=0):
    roll = r3d6()
    margin = skill + mod - roll
    if margin > 0:
        return SUCC, margin
    else:
        return FAIL, margin

# Quick contest: attacker vs. defender
#def qc(att, att_mod, def, def_mod):
#    att_succ, att_marg = sc(att, att_mod)
#    def_succ, def_marg = sc(def, def_mod)
#    if att_succ and 
#        return att
#    elif def_succ and :
#    else 
#    else:
#        return TIE

# Convert text representation of dice to a roll
def dice(text, roll=True, capped=True):
    parts = re.split('(\d+)d([+-]?\d*)', text)
    dice = int(parts[1])
    if parts[2] == "":
        mod = 0
    else:
        mod = int(parts[2])

    # Convert modifiers in excess of +3 to extra dice
    if dice > 1 or mod > 0:
        dice += mod / 4
        mod = mod % 4

    if roll is False:
        if mod == 0:
            return "%dd" % dice
        else:
            return "%dd%+d" % (dice, mod)

    # Roll
    result = sum(roll(r1d6, dice)) - mod

    # Whether we can go below 0
    if capped is True:
        return max(0, result)
    else:
        return result

# Return an appropriate text representation of your damage.
def damage_dice(amount):
    dice = 1
    mod = amount

    if amount > 0:
        dice += amount / 4
        mod = mod % 4

    if mod == 3:
        dice += 1
        mod -= 4

    if mod == 0:
        return "%dd" % dice
    else:
        return "%dd%+d" % (dice, mod)

# Test function
if __name__ == '__main__':
    #print "Ten 1d6 rolls:", roll(r1d6, 10)
    #print "Ten 3d6 rolls:", roll(r3d6, 10)
    print "Dice interpretation test"
    print dice("3d+9")
    print dice("2d+4")
    print dice("1d+3")
