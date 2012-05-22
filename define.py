# HACK: Define termsize rather than figuring it out.
TERM_X = 80
TERM_Y = 24

# Define some screen region X and Ys.
MAP_START_X = 0
MAP_START_Y = 0
MAP_X = 45
MAP_Y = TERM_Y

PANE_START_X = MAP_X
PANE_START_Y = 0
PANE_X = TERM_X - MAP_X
PANE_Y = TERM_Y

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
"sw"   : ("swing", "swinging"),
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

# Skill difficulties
difficulties = {
"E" : 0,
"A" : -1,
"H" : -2,
"V" : -3
}

# Types of point expenditures
point_types = ("attributes", "skills", "techniques", "traits")
