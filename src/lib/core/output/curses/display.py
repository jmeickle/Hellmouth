import curses

from src.lib.core.output.curses.layer import CursesLayer
from src.lib.core.output.display import Display, DisplayError

from src.lib.util import debug
from src.lib.util.geometry.space import Point
from src.lib.util.registry import RegistryDict

class CursesDisplay(Display):
    """A console `Display`, implemented using curses."""
    def __init__(self):
        # Initialize curses and store the root window.
        self.stdscr = curses.initscr()

        self.y, self.x = self.stdscr.getmaxyx()

        # The `Layer`s in this display.
        self.layers = RegistryDict()

        # Create a default `Layer` from the root window.
        self.layer("default", window=self.stdscr)

        # Whether there is a saved terminal mode to return to.
        self.mode = False

        # TODO: Move color support to some kind of broker class

        # The color pairs defined by curses.
        # TODO: Convert to RegistryDict
        self.colors = {}

        # Initialize curses color pairs.
        # TODO: Check whether the terminal supports colors first
        self.set_colors()

    def draw(self):
        for layer in self.layers.values():
            layer.draw()

    def layer(self, name, dimensions=None, position=None, window=None):
        if window:
            if dimensions or position:
                raise DisplayError("Provided too many arguments when creating a layer: dimensions={}, position={}, window={}".format(dimensions, position, window))
        else:
            if not dimensions and not position:
                raise DisplayError("Provided too few arguments to create a layer: dimensions={}, position={}, window={}".format(dimensions, position, window))
            dim_x, dim_y = dimensions
            pos_x, pos_y = position
            window = curses.newwin(dim_y, dim_x, pos_y, pos_x)

        window.keypad(True)
        layer = CursesLayer(display=self, window=window)
        self.layers[name] = layer
        return layer

    def save_mode(self):
        """Save the current terminal mode."""
        # Apparently this doesn't work?
        # curses.def_prog_mode()
        # self.mode = True
        curses.savetty()
        self.mode = True

    def reset_mode(self):
        """Restore to the previously saved terminal mode."""
        # Apparently this doesn't work?
        # curses.reset_prog_mode() if self.mode else self.set_mode()
        if self.mode:
            curses.resetty()
        else:
            raise DisplayError("There is no previously saved mode.")

    def set_mode(self):
        """Set the terminal mode."""
        curses.raw() # Use raw input mode. / # curses.cbreak() # Disable keyboard buffering
        curses.noecho() # Disable key echoing.
        curses.curs_set(0) # Disable cursor visibility.

        # Apparently this doesn't work?
        # Save the current "program" terminal mode.
        # curses.def_prog_mode()
        # self.mode = True

    def unset_mode(self):
        """Unset the terminal mode."""
        # Apparently this doesn't work?
        # Restore to the previous "shell" terminal mode.
        # curses.reset_shell_mode()

        curses.nocbreak() # Return to "cooked" input mode.
        curses.echo() # Enable key echoing.
        curses.curs_set(1) # Enable cursor visibility.
        # TODO: disable the terminal keypad?

    def set_colors(self):
        curses.start_color()

        # Basic color names and definitions.
        curses_colors = [
            ('black', curses.COLOR_BLACK),
            ('white', curses.COLOR_WHITE),
            ('blue', curses.COLOR_BLUE),
            ('cyan', curses.COLOR_CYAN),
            ('green', curses.COLOR_GREEN),
            ('magenta', curses.COLOR_MAGENTA),
            ('red', curses.COLOR_RED),
            ('yellow', curses.COLOR_YELLOW),
        ]

        # Color names
        # TODO: Move to color management class
        self.colors = {}

        for x in [x[0] for x in curses_colors]:
            self.colors[x] = (x,)

        # Elemental ('flickery') colors.
        self.colors["meat"] = ('red', 'yellow')

        # fg-bg colornames : curses colorpair
        self.pairs = {}

        # Must be hardcoded.
        self.pairs["white-black"] = 0

        # Set up all other color pairs
        pair_id = 1
        for i in range(8):
            for j in range(8):
                fg = curses_colors[i%8]
                bg = curses_colors[j%8]
                # White-black begins initialized
                if fg[0] == 'white' and bg[0] == 'black':
                    continue;
                curses.init_pair(pair_id, fg[1], bg[1])
                self.pairs["%s-%s" % (fg[0], bg[0])] = pair_id
                pair_id += 1

    def input(self):
        # TODO: handle curses.getmouse()
        return self.stdscr.getch()