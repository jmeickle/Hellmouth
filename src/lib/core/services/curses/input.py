import curses

from src.lib.core.kernel import Kernel
from src.lib.core.services.service import Service

class CursesInputService(Service):
    # TODO: Move into YAML?
    key_names = {
        " " : "Space",
        "\n" : "Enter",
        "Ctrl+j" : "Enter",
        curses.KEY_ENTER : "Enter",
        "Ctrl+i" : "Tab",
        "\t" : "Tab",
        curses.KEY_BTAB : "Shift+Tab",
        curses.KEY_BACKSPACE : "Backspace",
        curses.KEY_DC : "Delete",
        curses.KEY_UP : "Up",
        curses.KEY_DOWN : "Down",
        curses.KEY_LEFT : "Left",
        curses.KEY_RIGHT : "Right",
        curses.KEY_END : "End",
        curses.KEY_HOME : "Home",
        curses.KEY_PPAGE : "PgUp",
        curses.KEY_NPAGE : "PgDown",
        curses.KEY_IC : "Insert",
    }

    @Kernel.helper
    def key(self, key_code):
        key_names = CursesInputService.key_names
        # Normalize command characters to e.g. "Ctrl+a", then check overrides.
        if key_code <= 26:
            key_name =  "Ctrl+{}".format(chr(key_code + 96))
            return key_names.get(key_name, key_name)
        # Normalize other ASCII to a character representation, then check overrides.
        elif key_code <= 256:
            return key_names.get(chr(key_code), chr(key_code))
        # Only permit known non-ASCII characters.
        else:
            assert key_code in key_names, "Unrecognized key: {} ({}).".format(key_code, curses.keyname(key_code))
            return key_names.get(key_code, key_code)