from define import *

# Fields for skills:
# 'name' (str): More friendly display name.
# 'attribute' (str): What the skill is based on.
# 'difficulty' (str): How hard the skill is to learn.
# 'text' (str): Short, flavorful description of the skill.
# 'defaults' (list of tuples): An associated skill and the penalty when defaulting from it.
skills = {
"Brawling" : {
    "name"       : "Brawling",
    "attribute"  : "Dexterity",
    "difficulty" : "Easy",
    "text"       : "Hit stuff good",
    "defaults"   : [("Karate", -3), ("Judo", -3)],
},
"Judo" : {
    "name"       : "Brawling",
    "attribute"  : "Dexterity",
    "difficulty" : "Hard",
    "text"       : "Hit stuff good",
    "defaults"   : [("Brawling", -3)],
},
"Karate" : {
    "name"       : "Brawling",
    "attribute"  : "Dexterity",
    "difficulty" : "Very Hard",
    "text"       : "Hit stuff good",
    "defaults"   : [],
},
# End skill dictionary
}

# Calculate ranks in skills based on number of points spent and their difficulty.
def calculate_ranks(actor):
    # Reset existing ranks.
    actor.skills = {}
    # Use the skill dictionary to fill out ranks.
    for skill, points in actor.points["Skills"].items():
        attribute = skills[skill]["attribute"]
        difficulty = difficulties.get(skills[skill]["difficulty"])
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
        defaults = skills[current_skill]["defaults"]
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

# Skill test code.
if __name__ == "__main__":
    # Import necessary classes.
    from actor import Actor
    from dice import _3d6, _d6, roll

    # Generate a dummy actor
    actor = Actor()

    # Put points in a few skills
    actor.points["Skills"]["Brawling"] = _3d6()
    actor.points["Skills"]["Judo"] = max(_3d6() - _3d6(), 1)

    # Calculate skills
    calculate_ranks(actor)
    calculate_skills(actor)
    calculate_defaults(actor)

    # Print out a character sheet:
    print "==ATTRIBUTESS=="
    for stat, points in actor.attributes.items():
        print "%s: %s" % (stat, points)
    print "==POINTS=="
    for skill, points in actor.points["Skills"].items():
        print "%s: %s points" % (skill, points)
    print "==RANKS=="
    for skill, info in actor.skills.items():
        print "%s (%s/%s): %s%+d" % (skill, abbreviations[skills[skill]["attribute"]], abbreviations[skills[skill]["difficulty"]], abbreviations[info[0]], info[1])
    print "==SKILLS=="
    for skill, level in actor.base_skills.items():
        print "%s (%s/%s) - %s" % (skill, abbreviations[skills[skill]["attribute"]], abbreviations[skills[skill]["difficulty"]], level[0]),
        if level[1] is not False:
            print "(default: %s%d)" % (level[1][0], level[1][1])
        else:
            print ""
