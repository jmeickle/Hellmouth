"""Game constants and decorators that should be available globally."""

# TODO: Gut this file. Most of this stuff is very game specific!

import functools

from src.lib.util import debug

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

STATS_Y = 12

LOG_START_Y = PANE_START_Y + STATS_Y
LOG_Y = PANE_Y - STATS_Y

STATUS_X = 8
STATUS_Y = 3
STATUS_START_X = PANE_START_X - STATUS_X

# Location statuses
UNHURT = 0
SCRATCHED = 1
INJURED = 2
CRIPPLED = 3
DISMEMBERED = 4
SEVERED = 5

# Default interface colors
TEXT = "white"
HIGHLIGHT = "green"
ERROR = "red"
BACKGROUND = "black"

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
    "pi+"  : ("pierce (lg.)", "piercing (lg.)"),
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

# Make the syntax neater for weapon definitions.
U0 = (0, False)

# TODO: Just change the internal names to be cleaner?
hit_locations = { 
    "Torso" : "torso",
    "Groin" : "groin",
    "Neck" : "neck",
    "Head" : "head",
    "Skull" : "skull",
    "Face" : "face",
    "RArm" : "right arm",
    "LArm" : "left arm",
    "RHand" : "right hand",
    "LHand" : "left hand",
    "RLeg" : "right leg",
    "LLeg" : "left leg",
    "RFoot" : "right foot",
    "LFoot" : "left foot",
}

postures = {
    # Posture, melee, defense, ranged, movement cost
    "standing" : (0, 0, 0, 0),
    "crouching" : (-2, 0, -2, .5),
    "kneeling" : (-2, -2, -2, 2),
    "crawling" : (-4, -3, -2, 2),
    "sitting" : (-2, -2, -2, None),
    "lying prone" : (-4, -3, -2, False),
    "lying face up" : (-4, -3, -2, False),
}

def STUB(fn):
    """Decorator to return True when calling a stub method."""
    @functools.wraps(fn)
    def wrapper(self, *args, **kwargs):
        return True
    return wrapper

def UNIMPLEMENTED(fn):
    """Decorator to assert on calling an unimplemented method."""    
    @functools.wraps(fn)
    def wrapper(caller, *args, **kwargs):
        if isinstance(caller, type):
            string = "Unimplemented class method %s.%s()" % (caller.__name__, fn.__name__)
        else:
            string = "Unimplemented instance method %s.%s()" % (caller.__class__.__name__, fn.__name__)

        parts = []
        if args:
            parts.append("args: %s" % (args,))
        if kwargs:
            parts.append("kwargs: %s" % kwargs)
        if parts:
            string += ".\n" + "    " + "    \n".join(parts)
        string += "."
        debug.die(string)
    return wrapper