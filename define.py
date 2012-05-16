# Directional stuff
NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)
dirs = [NW, NE, CE, SE, SW, CW]

# Location statuses
UNHURT = 0
SCRATCHED = 1
INJURED = 2
CRIPPLED = 3
SEVERED = -1

# Damage types
types = {
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
