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
                 "Judo" : {},
                 "Karate" : {},
            }},
            "Melee" : { "options" : {
                "Axe" : {"weight": 50},
                "Broadsword" : {},
                "Shortsword" : {"weight" : 150},
                "Spear" : {},
            }},
        }},
#        "magic" : { "weight" : 10, "options" : {
#            "Fire Magic" : {},
#            "Ice Magic" : {},
#            "Necromancy" : {"weight" : 10},
#        }},
    }}, #</skills>
} #</default>
} #</generators>
