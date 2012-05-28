# TODO: Define a dict of keys/actions for remappable keys.
from define import *

globals = {"?" : True}

# Return the corresponding control-modified key.
def ctrl(c):
    return ord(c) - 96

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
