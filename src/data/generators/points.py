# Generators are weighted dictionaries of options for character generation.
# A generator's weight defaults to 100, so new entries should take that into account.
# Generators can reference generators declared before them.

# TODO: Support callback functions for checking eligibility

generators = {
# Default generator, used if none is provided.
"default" : {
    "skills" : { "options" : {
        "melee" : { "options" : {
            "Unarmed" : { "weight" : 10, "options" : {
                 "Brawling" : {},
            }}, # </Unarmed>
            "Melee" : { "options" : {
                "Axe/Mace" : {"weight": 50},
                "Broadsword" : {"weight" : 300},
                "Flail" : {"weight" : 0},
                "Knife" : {"weight" : 0},
                "Polearm" : {"weight": 50},
                "Shortsword" : {"weight" : 150},
                "Spear" : {"weight" : 150},
                "Staff" : {"weight" : 50},
                "Two-Handed Sword" : {"weight" : 50},
            }}, # </Melee>
        }},
#        "magic" : { "weight" : 10, "options" : {
#            "Fire Magic" : {},
#            "Ice Magic" : {},
#            "Necromancy" : {"weight" : 10},
#        }},
    }}, # </skills>
}, # </default>
# Meat slave generator.
"slave" : {
    "traits" : { "options" : {
        "ST" : {"multiplier" : 3},
        "HT" : {"multiplier" : 3},
    }}, # </traits>
    "skills" : { "options" : {
        "Knife" : {},
    }}, # </skills>
} # </slave>
} # </generators>
