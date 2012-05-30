import copy
import re
import random
from data.generators.text import tokens
# This file is mostly for generating random text. Other stuff will eventually be moved out of it.

# Key combinations. Supports anything, but using these keys:

# 'dmg': Damage text.
# (AMT): none, scratch, injure, cripple, sever, kill, overkill
# (TYPE): See define.py for a list of possible damage types.
# (SKILL): Margin of success. low, med, high, crit
# (LOC): For specialcasing messages (e.g., decapitation)

# If a tuple is provided, a random choice will be made with equal weight. Tuples can be nested.

class Descriptions():
    hits = {}
    fail = {}

def base_stat(value):
    if value > 20: return "godly"
    elif value > 14: return "amazing"
    elif value > 12: return "exceptional"
    elif value > 10: return "above-average"
    elif value is 10: return "average"
    elif value > 7: return "below-average"
    elif value is 7: return "poor"
    else: return "crippling"

# Utility functions:

# Convert a list of keys into a dash-separated string.
def build_key(keys):
    str = ""
    for key in keys:
        if key != "":
            if str == "":
                str += key
            else:
                str += "-%s" % key
    return str

# Hit the database to find a given string.
def g(str):
    Descriptions.hits[str] = True
    ret = tokens.get(str, None)
    if ret is not None:
        if isinstance(ret, tuple):
            ret = pick(ret)
    return ret

# Choose a random option from the tuple, and keep going if it's another tuple.
def pick(options):
    choice = random.choice(options)
    if isinstance(choice, tuple):
        choice = pick(choice)
    return choice

# Hit the database to find whether a given string failed already
def f(str):
    return Descriptions.fail.get(str, None)

# Logs number of failures to match. Mostly for debugging.
def fail(str):
    if Descriptions.fail.get(str, None) is None:
        Descriptions.fail[str] = 1
    else:
        Descriptions.fail[str] += 1

# String building functions

# Shorthand for main 'describe' function.
def d(str):
    return describe(str)

# Convert a string into relevant text. Anything between @ or ~ is tokenized.
# TODO: Keep @/~ and update the db keys to include them?
def describe(str):
    ret = ""
    for substr in re.split('([@~]\S*[@~])', str):
        if re.search('[@~]', substr) is not None:
            ret += replace(re.sub('[@~]', '', substr))
        else:
            ret += substr
    return ret

# Replace a dash-separated key with text from the database.
def replace(key):
    exact = g(key)
    if exact is not None:
        return exact
    else:
        ret = "!!!"+key+"!!!"
        keys = re.split('-',key)
        for i in range(len(keys)):
            ret = indexed_remove(keys, i, ret)
        return ret

# If an exact match wasn't found, recursively remove keys from the list of keys
# to try to find a partial match using this pattern:
#
# "one-two-three-four" -> "one-two-three", "one-two-four", "one-three-four", "one-two", "one"
#
# If no match for any of those permutations is found, the original key passed into
# indexed_remove by replace() is used; it's overwritten in replace(), though.
def indexed_remove(keys, n, ret):
    # The indices to be possibly removed in this pass:
    for x in reversed(range(len(keys)-n, len(keys))):
        copy = keys[:]
        copy[x]=""
        key = build_key(copy)
        # DEBUG: Change this to 'is None' (vs. 'is not False') and it'll stop checking already-failed.
        if f(key) is not False:
            result = g(key)
            if result is None:
                fail(key)
            else:
                # Return early to avoid looking for worse matches.
                ret = result
                return ret

    if n > 1:
        ret = indexed_remove(copy, n-1, ret)

    return ret

if __name__ == '__main__':
    print_dict("Text Database", Descriptions.dict)

    print "\nResults:"

    strs = ['You @dmg-sever-cut-neck-crit@ the opponent.',
            'You don\'t manage to @dmg-nonsense-herp-derp@ the opponent.',
            'You @dmg-cut-crit@ and @dmg-crush-crit@ your enemies!',
            'You\'ve been @dmg-cripple-neck@ in combat.',
            'You should @dmg-cripple-cut-neck@ your @enemies@.',
           ]

    for str in strs:
        print "%s => %s" % (str, describe(str))

    print ""
    print_dict("DB Hits", Descriptions.hits)
    print ""
    print_dict("DB Misses", Descriptions.fail)
