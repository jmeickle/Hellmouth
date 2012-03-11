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
map.loadmap(5,5,".")

mainmap = MainMap(stdscr, map.width, map.height)
mainmap.map = map
mainmap.add(player)
mainmap.draw()

while 1:
    # Keyin stuff
    c = stdscr.getch()
    if c == ord('q'):
        gameover()
        break
    elif c == curses.KEY_LEFT:
        player.x -= 1
    elif c == curses.KEY_RIGHT:
        player.x += 1
    elif c == curses.KEY_UP:
        player.y -= 1
    elif c == curses.KEY_DOWN:
        player.y += 1

    # Clear screen and tell components to draw themselves.
    stdscr.clear()
    mainmap.draw()
    stdscr.refresh()

def newwin(x, y):
    win = curses.newwin(y, x, starty, startx)
    return win
