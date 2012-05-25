from objects.items.item import *

item_list = {
    "broadsword" : {# Name
        "class" : Sword, # Object class
        "cost" : 500,
        "attacks" : { # Damage, type, minrange, maxrange, parry, min ST
            "swing" : ("sw+1", "cut", 0, 1, 1, 10),
            "thrust" : ("thr+1", "cr", 0, 1, 1, 10),
        },
    },
    "katana" : {
        "identical" : "broadsword",
    },
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
