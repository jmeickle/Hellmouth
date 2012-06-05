tokens = {
    # Damage

    # Current ordering:
    # 1) damage amount
    # 2) damage type
    # 3) attack name

    # Basic damage
    "dmg" : "damages",
    "dmg-burn" : "burns",
    "dmg-cut" : "cuts",
    "dmg-cr" : "crushes",
    "dmg-pi" : "pierces",
    "dmg-imp" : "impales",

    # No-ops
    # TODO: Remove this after attacks look at pre-DR damage
    "dmg-none" : "doesn't harm",
    "dmg-none-burn" : "doesn't harm",
    "dmg-none-cut" : "doesn't harm",
    "dmg-none-cr" : "doesn't harm",
    "dmg-none-pi" : "doesn't harm",
    "dmg-none-imp" : "doesn't harm",

    # Cutting damage
    "dmg-scratch-cut" : ("lightly @dmg-injure-cut@", "scratches", "grazes", "nicks"),
    "dmg-injure-cut" : ("cuts", "slashes", "slices"),
    "dmg-wound-cut" : ("deeply @dmg-injure-cut@", "chops into", "hacks into"),
    "dmg-cripple-cut" : ("brutally @dmg-injure-cut@", "horribly @dmg-injure-cut@", "chops deeply into", "hacks deeply into", "almost @dmg-dismember-cut@"),
    "dmg-dismember-cut" : ("@dmg-injure-cut@ through", "hacks off", "hacks apart", "chops apart", "chops off", "lops off"),

    # Crushing damage
    "dmg-scratch-cr" : ("pokes", "jabs"),
    "dmg-injure-cr" : ("impacts", "whacks"),
    "dmg-wound-cr" : ("batters", "slams", "bludgeons"),
    "dmg-cripple-cr" : ("beats", "mangles", "clobbers"),
    "dmg-dismember-cr" : ("flattens", "completely mangles"),

    # TODO: Piercing damage
    #"dmg-scratch-pi" : "",
    #"dmg-injure-pi" : "",
    #"dmg-wound-pi" : "",
    #"dmg-cripple-pi" : "",
    #"dmg-dismember-pi" : "",

    # Swung impaling damage
    "dmg-scratch-imp-swing" : "grazes",
    "dmg-injure-imp-swing" : "gouges",
    "dmg-wound-imp-swing" : "impales",
    "dmg-cripple-imp-swing" : "buries its weapon in",
    "dmg-dismember-imp-swing" : "buries its weapon to the hilt in",

    # Thrusting impaling damage
    "dmg-scratch-imp-thrust" : "pricks",
    "dmg-injure-imp-thrust" : ("stabs into", "stabs"),
    "dmg-wound-imp-thrust" : ("skewers", "impales"),
    "dmg-cripple-imp-thrust" : "buries its weapon into",
    "dmg-dismember-imp-thrust" : "buries its weapon to the hilt in",

    # Special attacks

    # Punches
    "dmg-scratch-cr-punch" : "punches",
    "dmg-injure-cr-punch" : ("smacks", "solidly punches", "whacks"),
    "dmg-wound-cr-punch" : ("pummels", "thrashes"),
    "dmg-cripple-cr-punch" : ("mauls", "manhandles"),
    "dmg-dismember-cr-punch" : ("pulverizes", "brutalizes"),

    # Bites
    "dmg-scratch-bite" : "nips",
    "dmg-injure-bite" : "chomps on",
    "dmg-wound-bite" : "bites into",
    "dmg-cripple-bite" : ("bites deeply into", "takes a bite out of"),
    "dmg-dismember-cr-punch" : ("bites off", "bites through"),

    # Defenses.
    "def" : "defends",
    "def-dodge" : ("dodges", "evades"),
    "def-dodge-crit" : ("easily dodges", "easily evades"),
    "def-parry" : ("parries", "intercepts"),
    "def-parry-crit" : ("easily parries", "easily intercepts"),
    "def-trivial" : "trivially defends",
    "def-easy" : "easily defends",
    "def-normal" : "defends",
    "def-hard" : "manages to defend",
    "def-difficult" : "barely manages to defend",
    "def-crit-trivial" : "thoroughly and utterly defends",
    "def-crit-easy" : "effortlessly defends",
    "def-crit-normal" : "completely defends",
    "def-crit-hard" : "readily defends",
    "def-crit-difficult" : "defends with nothing but luck",
    "def-crit-insane" : "defends with nothing but blind luck",

    # Misses.
    "miss" : "misses",
    "miss-easy" : ("barely misses", "just misses"),
    "miss-normal" : ("misses", "fails to hit"),
    "miss-hard" : "badly misses",
    "miss-difficult" : "completely misses",
    "miss-unlucky" : "horribly misses",
#    "miss-crit-trivial" : "",
#    "miss-crit-easy" : "",
#    "miss-crit-normal" : "",
#    "miss-crit-hard" : "",
#    "miss-crit-difficult" : "thoroughly defeats the air in front of",

    # Speech
    "speak-dmg" : "screams in pain",
    "screech-dmg" : "screeches in pain",
    "roar-dmg" : "roars in pain",

    # Miscellany.
    "spikes" : "but hits itself for",

}
    # TODO: Can't cripple necks, so we need a standin.
#    "dmg-cripple-cut-neck" : "partially decapitates",
#    "dmg-dismember-cut-neck" : "decapitates",
#    "dmg-dismember-crush-neck" : "crushes the windpipe",
