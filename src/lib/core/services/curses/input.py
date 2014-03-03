import curses

from src.lib.core.kernel import Kernel
from src.lib.core.services.service import Service

from src.lib.util import debug

class CursesInputService(Service):
    # TODO: Move key names into YAML?
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

    def __init__(self, display):
        self.display = display
        self.keys = []

    def pop(self):
        if self.keys:
            return self.keys.pop()

    def push(self, value):
        self.keys.append(value)

    def react(self):
        """Get key codes from the display. If there is one, push it to the keyin service."""
        event = self.display.input()
        if event is not -1:
            # TODO: Handle mice.
            key_name = self.key_name(event)
            debug.log("Input event: `{}` => `{}`".format(event, key_name))
            if key_name == "Ctrl+c":
                assert False, "Keyboard interrupt!"
            self.push(key_name)

    def key_name(self, key_code):
        """Return the key name of a key code."""
        # Normalize command characters to e.g. "Ctrl+a", then check overrides.
        if key_code <= 26:
            key_name =  "Ctrl+{}".format(chr(key_code + 96))
            return self.key_names.get(key_name, key_name)
        # Normalize other ASCII to a character representation, then check overrides.
        elif key_code <= 256:
            return self.key_names.get(chr(key_code), chr(key_code))
        # Only permit known non-ASCII characters.
        else:
            assert key_code in self.key_names, "Unrecognized key: {} ({}).".format(key_code, curses.keyname(key_code))
            return self.key_names.get(key_code, key_code)