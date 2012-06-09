from objects.items.modifiers import *

generators = {

# Armor.
"heavy armor" : { "options" : {
    "body" : { "options" : {
        "bone" : {
            "material" : Bone,
            "construction" : Thick,
            "items" : ["armor", "leggings", "gauntlets", "boots"]
        },
    }}, # </body>
}}, # </heavy armor>
"light armor" : { "options" : {
    "body" : { "weight" : 10, "options" : {
        "bone" : {
            "weight" : 10,
            "material" : Bone,
            "construction" : Thin,
            "quality" : Cheap,
            "items" : ["armor", "leggings", "gloves", "boots"]
        },
        "meat" : {
            "material" : Meat,
            "quality" : Cheap,
            "items" : ["armor", "leggings", "gloves", "boots"]
        },
    }}, # </body>
    "partial" : { "options" : {
        "bone" : {
            "weight" : 10,
            "material" : Bone,
            "construction" : Thin,
            "quality" : Cheap,
            "items" : ["armor", "leggings"]
        },
        "meat" : {
            "material" : Meat,
            "quality" : Cheap,
            "items" : ["armor", "leggings"]
        },
    }}, # </partial>
}}, # </light armor>

# Weapons.

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

"knives" : { "weight" : 20, "options" : {
    "small knife" : {"weight" : 50},
    "large knife" : {},
    "dagger" : {"weight" : 50},
}}, #</knives>

# A heavy weapon. Big! Strong!
"heavy weapon" : { "weight" : 10, "options" : {
    "greatsword" : {},
    "greataxe" : {},
    "flail" : {},
    "maul" : {},
    "warhammer" : {},
    "glaive" : {},
    "halberd" : {},
    "poleaxe" : {},
    "scythe" : {},
}}, #</heavy weapon>
}
