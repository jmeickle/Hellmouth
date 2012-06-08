from objects.items.modifiers import *

generators = {

"default_armor" : {
#    "full" : {"weight" : 50},
#    "body" : {},
    "partial" : {"options" : {
        "torso" : {
            "material" : Meat,
            "quality" : Cheap,
            "items" : ["breastplate"],
        },
        "upper body" : {
            "weight" : 50,
            "material" : Meat,
            "quality" : Cheap,
            "items" : ["breastplate", "arms", "gauntlets"],
        },
    }}, #</partial>
},
"default_weapons" : {
    "long swords" : { "weight" : 10, "options" : {
        "broadsword" : { "options" : {
            "broadsword" : {},
            "thrusting broadsword" : {"weight" : 50},
        }},
        "bastard sword" : { "weight" : 50, "options" : {
            "bastard sword" : {},
            "thrusting bastard sword" : {"weight" : 50},
        }},
        "greatsword" : { "weight" : 20, "options" : {
            "greatsword" : {},
            "thrusting greatsword" : {"weight" : 50},
        }},
    }}, #</long swords>
}
}
