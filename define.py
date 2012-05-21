# Location statuses
UNHURT = 0
SCRATCHED = 1
INJURED = 2
CRIPPLED = 3
SEVERED = -1

# Damage types
damage_types = {
"aff"  : ("affliction", "affliction"),
"burn" : ("burn", "burning"),
"cor"  : ("corrosion", "corrosion"),
"cr"   : ("crush", "crushing"),
"cut"  : ("cut", "cutting"),
"fat"  : ("fatigue", "fatigue"),
"imp"  : ("impale", "impaling"),
"pi"   : ("pierce", "piercing"),
"tox"  : ("toxic", "toxic"),
# Not really damage, but.
"thr"  : ("thrust", "thrusting"),
"sw"   : ( "swing", "swinging"),
}

abbreviations = {
"Speed" : "Spd.",
"Perception" : "Per.",
"Strength" : "ST",
"Dexterity" : "DX",
"Intelligence" : "IQ",
"Health" : "HT",
"Hit Points" : "HP",
"Fatigue Points" : "FP",
"Mana Points" : "MP",
"Easy" : "E",
"Average" : "A",
"Hard" : "H",
"Very Hard" : "VH",
}

difficulties = {
"Easy" : 0,
"Average" : -1,
"Hard" : -2,
"Very Hard" : -3
}
