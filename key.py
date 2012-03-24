from define import *
from describe import Descriptions
# Define dict of keys/actions

def keyin(stdscr, views):
        # Keyin stuff for player actions
        c = stdscr.getch()

        # Offer keyin to each view, and continue if any of them returns false
        for view in views:
            if view.keyin(c) is False:
                return False

        if c == ord('q') or c == 27: # Escape key
            exit(Descriptions.fail)
        elif c == ord('7'):
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

# TODO: Convert this into the multiple menu code
#        elif hasattr(chargen.selector, 'parent') is True:
#            if c == curses.KEY_RIGHT:
#                chargen.selector.next()
#            elif c == curses.KEY_LEFT:
#                chargen.selector.prev()
#            elif c == curses.KEY_ENTER or c == ord('\n'):
#                chargen.selector.choose()
#                views.remove(chargen)
