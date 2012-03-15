from define import *
import curses
from actor import Actor
from player import Player
from map import Map
from view import MainMap, Stats, Chargen, Status
import hex

def add_view(view):
    views.append(view)

def remove_view(view):
    views.remove(view)

def switch_focus(new):
    focus = new
    stdscr.addstr(10, 59, "SWITCHED FOCUS")

def init():
    stdscr = curses.initscr()
    curses.start_color() # Permit colors.
    curses.noecho() # Don't display typed keys.
    curses.cbreak()  # Don't wait for enter.
    stdscr.keypad(1) # Turn on keypad mode.
    curses.curs_set(0) # Make cursor invisible.
    return stdscr

# For exiting cleanly.
def gameover():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

def newwin(window, x, y, startx, starty):
    win = window.subwin(y, x, starty, startx)
    return win

# HACK:
term_x = 80
term_y = 24

stdscr = init()
from define import Color

# Very basic map init
map = Map()
map.loadmap(20, 20)

player = map.put(Player(), (15, 15))
for x in range(15):
    map.put(Actor(), (x, 0))

# HACK:
mainmap_width = 45

# Map screen init
mainmap = MainMap(stdscr, mainmap_width, term_y, 0, 0)
mainmap.map = map
mainmap.player = player
#mainmap.window.overlay(stdscr)
mainmap.ready()
mainmap.draw()

#chargen = Chargen(stdscr, 62, term_y, 0, 0)
# HACK:
spacing = 2
stats = Stats(stdscr, 80-mainmap_width-spacing, term_y, mainmap_width+spacing, 0)
stats.player = player

status_size = 5
status = Status(stdscr, 80-mainmap_width-status_size, term_y, mainmap_width-status_size, 0)

views = []
add_view(mainmap)
add_view(stats)
add_view(status)
#add_view(chargen)
#focus = chargen

# HACK: Show the map.
stdscr.clear()
for view in views:
    view.draw()
stdscr.refresh()

while 1:
    # Queue stuff
    if map.acting is None:
        map.acting = map.queue.popleft()

    # DEBUG: Print currently acting.
    # Has to be here for it to work properly.
    stdscr.addstr(19, 59, "QUEUE")
    if map.acting is not None:
        stdscr.addstr(20, 59, "Curr: %s" % map.acting.name)
    else:
        stdscr.addstr(20, 59, "Curr: NONE")
    stdscr.addstr(21, 59, "Next: %s" % map.queue[0].name)

    if map.acting is not player:
        map.acting.act()
        continue

    # Keyin stuff for player actions
    c = stdscr.getch()
    if c == ord('q'):
        gameover()
        break
    if c == 27: # Escape key
        switch_focus(mainmap)
    elif c == ord('7'):
        player.do(NW)
    elif c == ord('4'):
        player.do(CW)
    elif c == ord('1'):
        player.do(SW)
    elif c == ord('9'):
        player.do(NE)
    elif c == ord('6'):
        player.do(CE)
    elif c == ord('3'):
        player.do(SE)
    elif c == ord('5'):
        player.over()
#    elif hasattr(chargen.selector, 'parent') is True:
#        if c == curses.KEY_RIGHT:
#            chargen.selector.next()
#        elif c == curses.KEY_LEFT:
#            chargen.selector.prev()
#        elif c == curses.KEY_ENTER or c == ord('\n'):
#            chargen.selector.choose()
#            remove_view(chargen)

    # Clear screen and tell views to draw themselves.
    stdscr.clear()
    for view in views:
        view.draw()

    # All non-component drawing is handled below.

    # DEBUG: Print current position.
    #stdscr.addstr(10, 59, "POSITION", curses.color_pair(1))
    #stdscr.addstr(11, 59, '(%s, %s)' % player.pos, curses.A_REVERSE)

    # DEBUG: Print distance from starting point.
    #stdscr.addstr(13, 59, "DIST FROM (15, 15)")
    #stdscr.addstr(14, 59, "[%d]" % hex.dist(player.pos[0], player.pos[1], 15, 15))

    # DEBUG: Print current key.
    #stdscr.addstr(16, 59, "KEYIN")
    #if c < 256 and c > 31: # i.e., ASCII glyphs
    #    stdscr.addch(17, 59, chr(c))

    # DEBUG: Print current wounds.
    stdscr.addstr(16, 59, "WOUNDS")
    stdscr.addstr(17, 59, "%s" % player.body.locs.get("Torso").wounds)

    # Refresh the display.
    stdscr.refresh()
