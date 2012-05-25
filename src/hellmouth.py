# Main function, which is called below.
def main(stdscr):
    # Make the cursor invisible.
    curses.curs_set(0)
    # Use raw input mode.
    curses.raw()

    from games.meat import Game
    game = Game(stdscr)
#    exit(game.__dict__)
    # Main game loop
    while game.alive is True:
        game.loop()

# Curses import.
import curses

# Initialize the curses wrapper, which calls the main function after setting up curses.
curses.wrapper(main)
