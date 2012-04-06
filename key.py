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
        # TODO: Move these!
        if c == ord('7'):
            views[0].player.do(NW)
        elif c == ord('4'):
            views[0].player.do(CW)
        elif c == ord('1'):
            views[0].player.do(SW)
        elif c == ord('9'):
            views[0].player.do(NE)
        elif c == ord('6'):
            views[0].player.do(CE)
        elif c == ord('3'):
            views[0].player.do(SE)
        elif c == ord('5'):
            views[0].player.over()
        elif c == ord('P'):
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

