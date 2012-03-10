import curses

def init():
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    return stdscr

def gameover():
    curses.echo()
    curses.nocbreak()
    stdscr.keypad(0)
    curses.endwin()

stdscr = init()

while 1:
    c = stdscr.getch()
    if c == ord('q'):
        gameover()
        break
    else:
        stdscr.addch(0, 0, c)
    stdscr.refresh()

def newwin(x, y):
    win = curses.newwin(y, x, starty, startx)
    return win
