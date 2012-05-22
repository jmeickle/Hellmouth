# Generators are weighted dictionaries of options for character generation.
# A generator's weight defaults to 100, so new entries should take that into account.
# Generators can reference generators declared before them.

# TODO: Support callback functions for checking eligibility

generators = {
# Default generator, used if none is provided.
"default" : {
    "skills" : {
        "melee" : { "options" : {
            "Unarmed" : { "weight" : 10, "options" : {
                 "Unarmed/Brawling" : {},
                 "Unarmed/Judo" : {},
                 "Unarmed/Karate" : {},
            }},
            "Melee" : { "options" : {
                "Melee/Shortsword" : {},
                "Melee/Broadsword" : {},
                "Melee/Axe" : {"weight": 50},
            }},
        }},
        "magic" : { "weight" : 10, "options" : {
            "Magic/Fire Magic" : {},
            "Magic/Ice Magic" : {},
            "Magic/Necromancy" : {"weight" : 10},
        }},
    }, #</skills>
} #</default>
} #</generators>
