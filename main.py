import sys
import getopt
from src.lib.util.debug import debug
from src.lib.util.define import *
from src.lib.util import system

# Set up a dictionary of game settings.
arguments = {}

# Set a bitmask for game-wide display modes.
displayflags = {
    "silent" : 0b1,
    "curses" : 0b10,
    "unicode" : 0b100,
    "256" : 0b1000,
}

# Default to displaying with curses
arguments["displaymode"] = displayflags["curses"]

# Default to launching Meat Arena
# TODO: If not provided, always get a game launcher
# arguments["gamemode"] = "meat_arena"

# Default to not using a save
arguments["resume"] = False

# Parse command line arguments
try:
    debug("Parsing command line arguments.")
    options, remainder = getopt.getopt(sys.argv[1:],"a:b:")
except getopt.GetoptError:
    debug("Failed to parse arguments: %s." % sys.argv[1:])

# TODO: Handle more command line arguments.
for opt, arg in options:
    debug("Command line argument '%s': '%s'" % (opt, arg))

    # The game to be launched
    if opt in ('-g', '--gamemode'):
        arguments["gamemode"] = opt
    # The save to be loaded
    elif opt in ('-s', '--savefile'):
        pass
    # The display flags to apply
    elif opt in ('-d', '--displayflag'):
        # Non-recognized flags are a no-op.
        arguments["displaymode"] |= displayflags.get(opt, 0b0)

# Plain curses mode.
if arguments["displaymode"] == displayflags["curses"]:
    import curses

    def main(stdscr):
        # Set curses options.
        curses.curs_set(0) # Make the cursor invisible
        curses.raw() # Use raw input mode.

        # Initialize colors.
        from src.lib.util.color import Color

        # Initialize the root component.
        from src.lib.components.component import RootComponent
        root = RootComponent(stdscr)

        #
        if arguments.get("gamemode"):
            # TODO: Remove extraneous None
            root.launch((arguments.get("gamemode"), None))
        else:
            # Get a list of valid game names.
            choices = []
            for module_name in sorted(system.folders("src/games")):
                module_info = __import__('src.games.%s.info' % module_name, globals(), locals(), ['name', 'version', 'description'])
                choices.append((module_name, module_info))

            # Spawn a game choice menu.
            from src.lib.components.views.screens.screen import MenuScreen
            root.spawn(MenuScreen(root.window, **{"title" : "Start Game!", "choices" : choices, "callback" : root.launch}))

        # Start the application loop.
        while root.alive is True:
            root.loop()

    # Initialize the curses wrapper, which calls the main function after setting up curses.
    curses.wrapper(main)