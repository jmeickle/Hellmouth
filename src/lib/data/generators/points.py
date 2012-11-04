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
                "Broadsword" : {"weight" : 200},
                "Flail" : {"weight" : 25},
                "Knife" : {"weight" : 25},
                "Polearm" : {"weight": 50},
                "Shortsword" : {"weight" : 150},
                "Spear" : {"weight" : 150},
                "Staff" : {"weight" : 50},
                "2H Axe/Mace" : {"weight" : 50},
                "2H Flail" : {"weight" : 25},
                "2H Sword" : {"weight" : 200},
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
}, # </slave>

# Feral/wild monster generator.
"wild" : {
    "traits" : { "options" : {
        "ST" : {"multiplier" : 6},
        "DX" : {"multiplier" : 3},
        "HT" : {"multiplier" : 6},
    }}, # </traits>
    "skills" : { "options" : {
        "Brawling" : {},
    }}, # </skills>
}, # </wild>

# Elite monsters.
"elite" : {
    "traits" : { "options" : {
        "ST" : {"multiplier" : 6},
        "DX" : {"multiplier" : 6},
        "HT" : {"multiplier" : 6},
    }}, # </traits>
    "skills" : { "options" : {
        "Axe/Mace" : {},
        "Flail" : {},
        "Polearm" : {},
        "2H Axe/Mace" : {},
        "2H Flail" : {},
        "2H Sword" : {},
    }}, # </skills>
} # </elite>

} # </generators>
