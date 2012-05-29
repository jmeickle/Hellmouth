from define import *

# Calculate ranks in skills based on number of points spent and their difficulty.
def calculate_ranks(actor):
    # Reset existing ranks.
    actor.skills = {}
    # Use the skill dictionary to fill out ranks.
    for skill, points in actor.points["skills"].items():
        attribute = skill_list[skill]["attribute"]
        difficulty = difficulties.get(skill_list[skill]["difficulty"])
        spent = 0
        rank = None

        if spent+1 <= points:
            rank = difficulty
            spent += 1
        if spent+1 <= points:
            rank += 1
            spent += 1
        if spent+2 <= points:
            rank += 1
            spent += 2
        while spent+4 <= points:
            rank += 1
            spent += 4

        actor.skills[skill] = (attribute, rank)

# Calculate skills from attributes.
# Should only be run after calculating skill ranks.
def calculate_skills(actor):
    for skill, info in actor.skills.items():
        attribute, rank = info
        stat = actor.attributes.get(attribute)
        actor.base_skills[skill] = (stat+rank, False)

# Calculate defaults from related skills.
# Should only be run after calculating base skills.
def calculate_defaults(actor):
    for current_skill, current_info in actor.skills.items():
        defaults = skill_list[current_skill]["defaults"]
        for default in defaults:
            # Get the information for this default
            default_skill, default_modifier = default
            # Get the current skill's level and the default skill's level
            current_level, current_attribute = actor.base_skills.get(current_skill, (0, None))
            default_level, default_attribute = actor.base_skills.get(default_skill, (0, None))
            # Calculate the default
            new_level = default_level + default_modifier
            # If higher than the current level, save it, noting that it's a default.
            if new_level > current_level:
                actor.base_skills[current_skill] = (new_level, (default_skill, default_modifier))

# DATA. Eventually will be moved to another file.

# Fields for skills:
# 'type' (str): The skill category it falls under.
# 'attribute' (str): What the skill is based on.
# 'difficulty' (str): How hard the skill is to learn.
# 'text' (str): Short, flavorful description of the skill.
# 'defaults' (list of tuples): An associated skill and the penalty when defaulting from it.
skill_list = {
# Unarmed skills
"Brawling" : {
    "type"       : "Unarmed",
    "attribute"  : "DX",
    "difficulty" : "E",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
"Judo" : {
    "type"       : "Unarmed",
    "attribute"  : "DX",
    "difficulty" : "H",
    "text"       : "Hit stuff good",
    "defaults"   : [("Brawling", -3)],
},
"Karate" : {
    "type"       : "Unarmed",
    "attribute"  : "DX",
    "difficulty" : "VH",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
# Melee skills
"Shortsword" : {
    "type"       : "Melee",
    "attribute"  : "DX",
    "difficulty" : "A",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
"Broadsword" : {
    "type"       : "Melee",
    "attribute"  : "DX",
    "difficulty" : "A",
    "text"       : "Hit stuff good",
    "defaults"   : [("Shortsword", -2), ("Two-Handed Sword", -4)],
},
"Axe" : {
    "type"       : "Melee",
    "attribute"  : "DX",
    "difficulty" : "A",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
"Spear" : {
    "type"       : "Melee",
    "attribute"  : "DX",
    "difficulty" : "A",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
# Magic skills
"Fire Magic" : {
    "type"       : "Magic",
    "attribute"  : "IQ",
    "difficulty" : "VH",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
"Ice Magic" : {
    "type"       : "Magic",
    "attribute"  : "DX",
    "difficulty" : "VH",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
"Necromancy" : {
    "type"       : "Magic",
    "attribute"  : "IQ",
    "difficulty" : "VH",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
# Economic skills
"Farming" : {
    "type"       : "Trade",
    "attribute"  : "IQ",
    "difficulty" : "A",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
# End skill dictionary
}

# Skill test code.
if __name__ == "__main__":
    # Import necessary classes.
    from actor import Actor
    from dice import *

    # Generate a dummy actor
    actor = Actor()

    # Put points in a few skills
    actor.points["Skills"]["Brawling"] = r3d6()
    actor.points["Skills"]["Judo"] = max(r3d6() - _3d6(), 1)

    # Calculate skills
    calculate_ranks(actor)
    calculate_skills(actor)
    calculate_defaults(actor)

    # Print out a character sheet:
    print "==ATTRIBUTES=="
    for stat, points in actor.attributes.items():
        print "%s: %s" % (stat, points)
    print "==POINTS=="
    for skill, points in actor.points["Skills"].items():
        print "%s: %s points" % (skill, points)
    print "==RANKS=="
    for skill, info in actor.skills.items():
        print "%s (%s/%s): %s%+d" % (skill, labels[skills[skill]["attribute"]], abbreviations[skills[skill]["difficulty"]], abbreviations[info[0]], info[1])
    print "==SKILLS=="
    for skill, level in actor.base_skills.items():
        print "%s (%s/%s) - %s" % (skill, labels[skills[skill]["attribute"]], abbreviations[skills[skill]["difficulty"]], level[0]),
        if level[1] is not False:
            print "(default: %s%d)" % (level[1][0], level[1][1])
        else:
            print ""

