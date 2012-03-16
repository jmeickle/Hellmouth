import curses

NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)
dirs = [NW, NE, CE, SE, SW, CW]

class Color:
#    red = curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    colors = [
        ('black', curses.COLOR_BLACK),
        ('blue', curses.COLOR_BLUE),
        ('cyan', curses.COLOR_CYAN),
        ('green', curses.COLOR_GREEN),
        ('magenta', curses.COLOR_MAGENTA),
        ('red', curses.COLOR_RED),
        ('white', curses.COLOR_WHITE),
        ('yellow', curses.COLOR_YELLOW),
    ]

#    $i = 0
#    while $i < 20:
#        curses.init_pair($i % 8, $i % 8 % 8)
#        $i += 1

#    for index, color in enumerate(names):
#        print index
#        print color
#        curses.init_pair(index, color, names["black"])

#    curses.init_pair($i, curses.COLOR_RED
#    print curses.COLORS
#    print curses.COLOR_PAIRS
#    colors = {'red' : ("5", "2")}
#("5", "2"),
#    for color, value in colors.iteritems():
#        print color
#        print value
#curses.init_pair(value, curses.COLOR_

#return 
#def color(col):
#    if 
#    return col
