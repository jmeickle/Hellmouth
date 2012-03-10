import curses
from player import Player
from map import Map
from view import MainMap

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

while 1:
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
#    else:
#        stdscr.addch(c)
    stdscr.clear()
    player.draw(stdscr)
    stdscr.refresh()

map = Map()
map.loadmap(5,5,"Hello")
print map.map

def newwin(x, y):
    win = curses.newwin(y, x, starty, startx)
    return win
