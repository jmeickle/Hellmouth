import curses
from actor import Actor
from player import Player
from map import Map
from view import MainMap, Stats, Chargen
from hexes import dist

NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)

def add_view(view):
    components.append(view)

def remove_view(view):
    components.remove(view)

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

stdscr = init()

# Very basic map init
map = Map()
map.loadmap(50, 50, ".")

player = Player()
player.map = map

dummy = Actor(10, 10)
dummy2 = Actor(12, 12)
dummy3 = Actor(15, 15)
dummy4 = Actor(20, 20)

# Map screen init
mainmap = MainMap(stdscr, 62, 24, 0, 0)
mainmap.map = map
mainmap.player = player
mainmap.add(player)
mainmap.add(dummy)
mainmap.add(dummy2)
mainmap.add(dummy3)
mainmap.add(dummy4)
#mainmap.window.overlay(stdscr)
mainmap.draw()

chargen = Chargen(stdscr, 62, 24, 0, 0)
stats = Stats(stdscr, 20, 24, 60, 0)
components = []
add_view(chargen)
add_view(stats)
add_view(mainmap)
#components = [chargen, stats, mainmap]
focus = chargen

while 1:
    # Keyin stuff
    c = stdscr.getch()
    if c == ord('q'):
        gameover()
        break
    if c == 27: # Escape key
        switch_focus(mainmap)
    elif c == ord('7'):
        player.move(NW)
    elif c == ord('4'):
        player.move(CW)
    elif c == ord('1'):
        player.move(SW)
    elif c == ord('9'):
        player.move(NE)
    elif c == ord('6'):
        player.move(CE)
    elif c == ord('3'):
        player.move(SE)
    elif hasattr(chargen.selector, 'parent') is True:
        if c == curses.KEY_RIGHT:
            chargen.selector.next()
        elif c == curses.KEY_LEFT:
            chargen.selector.prev()
        elif c == curses.KEY_ENTER or c == ord('\n'):
            chargen.selector.choose()
            remove_view(chargen)

    # Clear screen and tell components to draw themselves.
    stdscr.clear()
    for component in components:
        component.draw()

    # All non-component drawing is handled below.

    # DEBUG: Print current position.
    stdscr.addstr(22, 59, "POSITION")
    stdscr.addstr(23, 59, '(%s, %s)' % player.pos)

    # DEBUG: Print distance from starting point.
    stdscr.addstr(20, 59, "DIST")
    stdscr.addstr(21, 59, "[%d]" % dist(player.pos[0], player.pos[1], 15, 15))

    # DEBUG: Print current key.
    stdscr.addstr(22, 69, "KEYIN")
    if c < 256 and c > 31: # i.e., ASCII glyphs
        stdscr.addch(23, 69, chr(c))

    # Refresh the display.
    stdscr.refresh()
