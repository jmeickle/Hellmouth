from define import *
from describe import Descriptions
# Define dict of keys/actions

# Return the corresponding control-modified key.
def ctrl(c):
    return ord(c) - 96

def keyin(stdscr, views):
        # Keyin stuff for player actions
        c = stdscr.getch()

        # Always allow quitting.
        if c == ctrl('q'):
            exit(Descriptions.fail)

        # Offer keyin to each view, and continue if any of them returns false
        for view in views:
            if view._keyin(c) is False:
                return False

        # 'Global' keypresses that work anywhere
        if c == ord('P'):
            views[0].player.attack(views[0].player)
        elif c == ord('g'):
            views[0].player.get_all()
        elif c == ord('d'):
            views[0].player.drop_all()

# TODO: Convert this into the multiple menu code
#        elif hasattr(chargen.selector, 'parent') is True:
#            if c == curses.KEY_RIGHT:
#                chargen.selector.next()
#            elif c == curses.KEY_LEFT:
#                chargen.selector.prev()
#            elif c == curses.KEY_ENTER or c == ord('\n'):
#                chargen.selector.choose()
#                views.remove(chargen)

