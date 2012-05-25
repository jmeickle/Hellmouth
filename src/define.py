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

STATS_Y = 11

LOG_START_Y = PANE_START_Y + STATS_Y
LOG_Y = PANE_Y - STATS_Y

STATUS_X = 10
STATUS_Y = 5
STATUS_START_X = PANE_START_X - STATUS_X

# Location statuses
UNHURT = 0
SCRATCHED = 1
INJURED = 2
CRIPPLED = 3
SEVERED = -1

# Damage types.
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

# Labels for in-game attributes. Arranged as
#
#     key : (names from shortest to longest)
#
# Either of those may be none.

labels = {
    "ST" : ("ST", "Strength"),
    "DX" : ("DX", "Dexterity"),
    "IQ" : ("IQ", "Intelligence"),
    "HT" : ("HT", "Health"),
    "Will" : ("Will",),
    "Perception" : ("Per.", "Perception"),
    "Move" : ("Move",),
    "Speed" : ("Spd.", "Speed"),
    "Block" : ("Block",),
    "Dodge" : ("Dodge",),
    "Parry" : ("Parry",),
    "HP" : ("HP", "Hit Points"),
    "FP" : ("FP", "Fatigue", "Fatigue Points"),
    "MP" : ("MP", "Mana", "Mana Points"),
    "E" : ("E", "Easy"),
    "A" : ("A", "Average"),
    "H" : ("H", "Hard"),
    "VH" : ("VH", "Very Hard"),
}

# Skill difficulty.
difficulties = {
    "E" : 0,
    "A" : -1,
    "H" : -2,
    "VH" : -3
}

# Types of point expenditures
point_types = ("attributes", "skills", "techniques", "traits")

primary_attributes = ("ST", "DX", "IQ", "HT")
secondary_attributes = ("HP", "FP", "MP", "Will", "Perception", "Speed", "Move")
