# TODO: Define a dict of keys/actions for remappable keys.
from define import *
from hex import *

CMD_ATTACK = "attack"
CMD_TALK = "talk"
CMD_MOVE = "move"
CMD_SCROLL = "scroll"

commands = {}
commands[CMD_ATTACK] = ("a",)
commands[CMD_TALK] = ("t",)
commands[CMD_MOVE] = ("1", "3", "4", "6", "7", "9", "5")
commands[CMD_SCROLL] = commands[CMD_MOVE]

# Return the corresponding control-modified key.
def ctrl(c):
    return ord(c) - 96

globals = {}
globals[ord("?")] = True
globals[ctrl("q")] = True

# Return the corresponding hex direction.
def hexkeys(c):
    if c == ord('7'):
        return NW
    elif c == ord('4'):
        return CW
    elif c == ord('1'):
        return SW
    elif c == ord('9'):
        return NE
    elif c == ord('6'):
        return CE
    elif c == ord('3'):
        return SE
    elif c == ord('5'):
        return CC
    return None
