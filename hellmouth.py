import curses
from player import Player
from map import Map
from view import MainMap, Stats

NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)

def init():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    curses.curs_set(0) # Make cursor invisible.
    return stdscr

def gameover():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

stdscr = init()

player = Player()
map = Map()
map.loadmap(10, 10,".")

player.map = map

mainmap = MainMap(stdscr, map.width, map.height)
mainmap.map = map
mainmap.add(player)
mainmap.draw()

stats = Stats(stdscr, 60, 0)

while 1:
    # Keyin stuff
    c = stdscr.getch()
    if c == ord('q'):
        gameover()
        break
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

    # Clear screen and tell components to draw themselves.
    stdscr.clear()
    mainmap.draw()
    stats.draw()

    # DEBUG: Print current position.
    stdscr.addstr(12, 12, "POSITION")
    stdscr.addstr(13, 12, '%s, %s' % player.pos)
    stdscr.refresh()

def newwin(x, y):
    win = curses.newwin(y, x, starty, startx)
    return win
