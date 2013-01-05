# TODO: Define a dict of keys/actions for remappable keys.
from define import *
from hex import *

# Game process commands
CMD_SAVE = "save the game"
CMD_LOAD = "load the game"
CMD_QUIT = "quit the game"

# Player character commands
CMD_ATTACK = "attack"
CMD_TALK = "talk"
CMD_HEX = "hex direction"
CMD_RECT = "rectangular direction"
CMD_CONFIRM = "confirm or submit"
CMD_CANCEL = "cancel or go back"

commands = {}
commands[CMD_ATTACK] = ("a",)
commands[CMD_TALK] = ("t",)
commands[CMD_HEX] = ("1", "3", "4", "6", "7", "9", "5")
commands[CMD_CANCEL] = (' ',)

# Return whether the provided keypress belongs to the provided command.
def cmd(c, command):
    if c <= 256:
        c = chr(c)
    if c in commands[command]:
        return True
    return False

# Return the corresponding control-modified key.
def ctrl(c):
    return ord(c) - 96

# Hack to prevent help screen recursion.
# You won't be able to quit the game while on a help screen, though.
# TODO: Replace with something better! Yikes.
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