import curses
import sys
import getopt
from src.lib.util.debug import *

# Main function, which is called below.
def main(stdscr):
    try:
        DEBUG("Parsing command line arguments.")
        options, remainder = getopt.getopt(sys.argv[1:],"a:b:")
    except getopt.GetoptError:
        DEBUG("Failed to parse arguments: %s." % sys.argv[1:])
        exit()

    # TODO: Handle command line arguments.
    for opt, arg in options:
        DEBUG("Option '%s': '%s'" % (opt, arg))

        # The game to be run
        if opt in ('-g', '--game'):
            pass
        # The save to be loaded
        elif opt in ('-s', '--savefile'):
            pass

    # Make the cursor invisible.
    curses.curs_set(0)
    # Use raw input mode.
    curses.raw()

    # # Initialize the database.
    # TODO: Move.
    # from src.lib.util import db

    # Initialize the game.
    # TODO: Game chooser?
    from src.games.meat_arena.meat import Game
    game = Game(stdscr, resume=False)

    # Main game loop
    while game.alive is True:
        game.loop()

# Initialize the curses wrapper, which calls the main function after setting up curses.
curses.wrapper(main)