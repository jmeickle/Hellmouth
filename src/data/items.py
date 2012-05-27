# TODO: Garrotes
# TODO: Ranged combat
# TODO: Nets
# TODO: Kicks (and other techniques)
# TODO: Lances
# TODO: Whips
# TODO: Foreign weapons

from define import *
from objects.items.item import *

item_list = {
# Swords.
    "broadsword" : {
        "class" : Sword,
        "cost" : 500,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : { # Dmg., type, reach, parry, min ST, hands
                "swing"  : ("sw+1", "cut", (1,), 0, 10, 1),
                "thrust" : ("thr+1", "cr", (1,), 0, 10, 1),
            },
        },
    },
    "thrusting broadsword" : {
        "class" : Sword,
        "cost" : 600,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : { # Dmg., type, reach, parry, min ST, hands
                "swing"  : ("sw+1", "cut", (1,), 0, 10, 1),
                "thrust" : ("thr+2", "imp", (1,), 0, 10, 1),
            },
        },
    },
    "bastard sword" : {
        "class" : Sword,
        "cost" : 650,
        "weight" : 5,
        "attack_options" : {
            "Broadsword" : {
                "swing"  : ("sw+1", "cut", (1,2), U0, 11, 1),
                "thrust" : ("thr+1", "cr", (2,), U0, 11, 1),
            },
            "Two-Handed Sword" : {
                "swing"  : ("sw+2", "cut", (1,2), 0, 10, 2),
                "thrust" : ("thr+2", "cr", (2,), 0, 10, 2),
            },
        },
    },
    "thrusting bastard sword" : {
        "class" : Sword,
        "cost" : 750,
        "weight" : 5,
        "attack_options" : {
            "Broadsword" : {
                "swing"  : ("sw+1", "cut", (1,2), U0, 11, 1),
                "thrust" : ("thr+2", "imp", (2,), U0, 11, 1),
            },
            "Two-Handed Sword" : {
                "swing"  : ("sw+2", "cut", (1,2), 0, 10, 2),
                "thrust" : ("thr+3", "imp", (2,), 0, 10, 2),
            },
        },
    },
    "greatsword" : {
        "class" : Sword,
        "cost" : 800,
        "weight" : 7,
        "attack_options" : {
            "Two-Handed Sword" : {
                "swing"  : ("sw+3", "cut", (1,2), 0, 12, 2),
                "thrust" : ("thr+2", "cr", (2,), 0, 12, 2),
            },
        },
    },
    "thrusting greatsword" : {
        "class" : Sword,
        "cost" : 900,
        "weight" : 7,
        "attack_options" : {
            "Two-Handed Sword" : {
                "swing"  : ("sw+3", "cut", (1,2), 0, 12, 2),
                "thrust" : ("thr+3", "imp", (2,), 0, 12, 2),
            },
        },
    },
# Short blades.
    "shortsword" : {
        "class" : Sword,
        "cost" : 400,
        "weight" : 2,
        "attack_options" : {
            "Shortsword" : {
                "swing"  : ("sw", "cut", (1,), 0, 8, 1),
                "thrust" : ("thr", "imp", (1,), 0, 8, 1),
            },
        },
    },
# Knives and daggers.
    "small knife" : {
        "class" : Knife,
        "cost" : 30,
        "weight" : .5,
        "attack_options" : {
            "Knife" : {
                "swing"  : ("sw-3", "cut", (0,1), -1, 5, 1),
                "thrust" : ("thr-1", "imp", (0,), -1, 5, 1),
            },
        },
    },
    "large knife" : {
        "class" : Knife,
        "cost" : 40,
        "weight" : 1,
        "attack_options" : {
            "Knife" : {
                "swing"  : ("sw-2", "cut", (0,1), -1, 6, 1),
                "thrust" : ("thr", "imp", (0,), -1, 6, 1),
            },
        },
    },
    "dagger" : {
        "class" : Dagger,
        "cost" : 20,
        "weight" : .25,
        "attack_options" : {
            "Knife" : {"thrust"  : ("thr-1", "imp", (0,), -1, 5, 1),},
        },
    },

# Axes.
    "hatchet" : {
        "class" : Axe,
        "cost" : 40,
        "weight" : 2,
        "attack_options" : {
            "Axe/Mace" : { "swing"  : ("sw", "cut", (1,), 0, 8, 1),}
        },
    },
    "axe" : {
        "class" : Axe,
        "cost" : 50,
        "weight" : 4,
        "attack_options" : {
            "Axe/Mace" : { "swing"  : ("sw+2", "cut", (1,), U0, 11, 1),}
        },
    },
    "throwing axe" : {
        "class" : Axe,
        "cost" : 60,
        "weight" : 4,
        "attack_options" : {
            "Axe/Mace" : { "swing" : ("sw+2", "cut", (1,), U0, 11, 1),}
        },
    },
    "great axe" : {
        "class" : Axe,
        "cost" : 100,
        "weight" : 8,
        "attack_options" : {
            "Two-Handed Axe/Mace" : { "swing" : ("sw+3", "cut", (1,2), U0, 12, 3),}
        },
    },
# Maces.
    "mace" : {
        "class" : Mace,
        "cost" : 50,
        "weight" : 5,
        "attack_options" : {
            "Axe/Mace" : { "swing"  : ("sw+3", "cr", (1,), U0, 12, 1),}
        },
    },
    "small mace" : {
        "class" : Mace,
        "cost" : 35,
        "weight" : 3,
        "attack_options" : {
            "Axe/Mace" : { "swing"  : ("sw+2", "cr", (1,), U0, 10, 1),}
        },
    },
# Picks and hammers.
    "pick" : {
        "class" : Pick,
        "cost" : 70,
        "weight" : 3,
        "attack_options" : {
            "Axe/Mace" : { "swing"  : ("sw+1", "imp", (1,), U0, 10, 1),}
        },
    },
    "maul" : {
        "class" : Hammer,
        "cost" : 80,
        "weight" : 12,
        "attack_options" : {
            "Two-Handed Axe/Mace" : { "swing"  : ("sw+4", "cr", (1,2), U0, 12, 3),},
        },
    },
    "warhammer" : {
        "class" : Hammer,
        "cost" : 100,
        "weight" : 7,
        "attack_options" : {
            "Two-Handed Axe/Mace" : { "swing" : ("sw+3", "imp", (1,2), U0, 12, 3),},
        },
    },

# Clubs.
    "baton" : {
        "class" : Club,
        "cost" : 20,
        "weight" : 1,
        "attack_options" : {
            "Shortsword" : {
                "swing"  : ("sw", "cr", (1,), 0, 6, 1),
                "thrust" : ("thr", "cr", (1,), 0, 6, 1),
            },
        },
    },
    "light club" : {
        "class" : Club,
        "cost" : 5,
        "weight" : 3,
        "attack_options" : {
            "Broadsword" : {
                "thrust" : ("thr+1", "cr", (1,), 0, 10, 1),
                "swing"  : ("sw+1", "cr", (1,), 0, 10, 1),
            },
        },
    },
# Flails.
    "morningstar" : {
        "class" : Flail,
        "cost" : 80,
        "weight" : 6,
        "attack_options" : {
            "Flail" : { "swing" : ("sw+3", "cr", (1,), U0, 12, 1),},
        },
    },
    "flail" : {
        "class" : Flail,
        "cost" : 100,
        "weight" : 8,
        "attack_options" : {
            "Two-Handed Flail" : { "swing" : ("sw+4", "cr", (1,2), U0, 13, 2),},
        },
    },
# Long battlefield polearms.
    "glaive" : {
        "class" : Pollaxe,
        "cost" : 100,
        "weight" : 8,
        "attack_options" : {
            "Polearm" : { "swing" : ("sw+3", "cut", (2,3), U0, 11, 3),},
            "Polearm" : { "thrust" : ("thr+3", "imp", (1,2,3), U0, 11, 2),},
        },
    },
    "halberd" : {
        "class" : Pollaxe,
        "cost" : 150,
        "weight" : 12,
        "attack_options" : {
            "Polearm" : { "swing" : ("sw+5", "cut", (2,3), U0, 13, 3),},
            "Polearm" : { "swing" : ("sw+4", "imp", (2,3), U0, 13, 3),},
            "Polearm" : { "thrust" : ("thr+3", "imp", (1,2,3), U0, 12, 2),},
        },
    },
    "poleaxe" : {
        "class" : Pollaxe,
        "cost" : 120,
        "weight" : 10,
        "attack_options" : {
            "Polearm" : { "swing" : ("sw+4", "cut", (2,3), U0, 12, 3),},
            "Polearm" : { "thrust" : ("sw+4", "cr", (2,3), U0, 12, 3),},
        },
    },

# Shorter polearms.

# Spears.
    "spear" : {
        "class" : Spear,
        "cost" : 40,
        "weight" : 4,
        "attack_options" : {
            "Spear"   : {
                "thrust" : ("thr+2", "imp", (1,), 0, 9, 1),
                "thrust" : ("thr+3", "imp", (1,2), 0, 9, 2),
            },
        },
    },
    "long spear" : {
        "class" : Spear,
        "cost" : 60,
        "weight" : 5,
        "attack_options" : {
            "Spear"   : {
                "thrust" : ("thr+2", "imp", (2,3), U0, 10, 1),
                "thrust" : ("thr+3", "imp", (2,3), 0, 10, 2),
            },
        },
    },
# Staves
    "quarterstaff" : {
        "class" : Staff,
        "cost" : 10,
        "weight" : 4,
        "attack_options" : {
            "Staff"   : {
                "swing" : ("sw+2", "cr", (1,2), 2, 7, 2),
                "thrust" : ("thr+2", "cr", (1,2), 2, 7, 2),
            },
            "Two-Handed Sword"   : {
                "swing" : ("sw+2", "cr", (1,2), 0, 9, 2),
                "thrust" : ("thr+1", "cr", (2,), 0, 9, 2),
            },
        },
    },

# Unarmed-augmentors.
    "brass knuckles" : {
        "class" : Glove,
        "cost" : 10,
        "weight" : .25,
        "attack_options" : {
            "Boxing"   : { "thrust" : ("thr", "cr", (0,), 0, None, None),},
            "Brawling" : { "thrust" : ("thr", "cr", (0,), 0, None, None),},
            "Karate"   : { "thrust" : ("thr", "cr", (0,), 0, None, None),},
            "DX"       : { "thrust" : ("thr", "cr", (0,), 0, None, None),},
        },
    },
    "blackjack" : {
        "class" : Weapon,
        "cost" : 20,
        "weight" : 1,
        "attack_options" : { # Damage, type, reach, parry, min ST
            "Brawling" : { "hit" : ("thr", "cr", (0,), 0, 7, 1),},
            "DX"       : { "hit" : ("thr", "cr", (0,), 0, 7, 1),},
        },
    },
# Improvised weapons.
    "wooden stake" : {
        "class" : Weapon,
        "cost" : 4,
        "weight" : .5,
        "attack_options" : {
            "Knife" : {"thrust"  : ("thr(.05)", "imp", (0,), -1, 5, 1),},
        },
    },
    "scythe" : {
        "class" : Tool,
        "cost" : 15,
        "weight" : 5,
        "attack_options" : {
            "Two-Handed Axe/Mace" : {
                "swing"  : ("sw+2", "cut", (1,), U0, 11, 3),
                "swing"  : ("sw", "imp", (1,), U0, 11, 3),
            },
        },
    },
# Fake items.
# Natural attacks.
    "fist" : {
        "class" : Natural,
        "attack_options" : { # Damage, type, reach, parry, min ST
            "Boxing"   : { "punch" : ("thr-1", "cr", (0,), 0, None, None),},
            "Brawling" : { "punch" : ("thr-1", "cr", (0,), 0, None, None),},
            "Karate"   : { "punch" : ("thr-1", "cr", (0,), 0, None, None),},
            "DX"       : { "punch" : ("thr-1", "cr", (0,), 0, None, None),},
        },
    },
    "blunt teeth" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : { "bite" : ("thr-1", "cr", (0,), None, None, None),},
            "DX"       : { "bite" : ("thr-1", "imp", (0,), None, None, None),},
        },
    },
    "sharp teeth" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : { "bite" : ("thr-1", "cut", (0,), None, None, None),},
            "DX"       : { "bite" : ("thr-1", "cut", (0,), None, None, None),},
        },
    },
    "fangs" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : { "bite" : ("thr-1", "imp", (0,), None, None, None),},
            "DX"       : { "bite" : ("thr-1", "imp", (0,), None, None, None),},
        },
    },
    "beak" : {
        "class" : Natural,
        "attack_options" : {
            "Brawling" : { "peck" : ("thr-1", "pi+", (0,), None, None, None),},
            "DX"       : { "peck" : ("thr-1", "pi+", (0,), None, None, None),},
        },
    },
# TODO: A ton of demonic strikers. Tails, wings, etc.
# TODO: Shield bashes.
}

# Test code.
if __name__ == '__main__':
    swords = ("broadsword", "katana")
    for sword in swords:
        stats = item_list[sword]
        if stats.get("identical") is not None:
            stats = item_list[stats["identical"]]
        sword = stats["class"]()
        for stat, value in stats.items():
            print stat, value
            setattr(sword, stat, value)
        print sword.__dict__
