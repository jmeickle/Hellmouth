import curses

# Directional stuff
NW = (0, -1)
NE = (1, -1)
CE = (1, 0)
SE = (0, 1)
SW = (-1, 1)
CW = (-1, 0)
dirs = [NW, NE, CE, SE, SW, CW]

# Location statuses
UNHURT = 0
SCRATCHED = 1
INJURED = 2
CRIPPLED = 3
SEVERED = -1

class Color:
    # Basic color names and definitions.
    colors = [
        ('black', curses.COLOR_BLACK),
        ('white', curses.COLOR_WHITE),
        ('blue', curses.COLOR_BLUE),
        ('cyan', curses.COLOR_CYAN),
        ('green', curses.COLOR_GREEN),
        ('magenta', curses.COLOR_MAGENTA),
        ('red', curses.COLOR_RED),
        ('yellow', curses.COLOR_YELLOW),
    ]

    # Color names
    names = [x[0] for x in colors]

    #fg-bg colornames : curses colorpair
    pair = {}
    if __name__ == '__main__':
        curses.initscr()
        curses.start_color()

    # Set up all colorpairs
    for i in range(8):
        for j in range(8):
            fg = colors[i%8]
            bg = colors[j%8]
            if i == 0 and j == 0 or fg[1] == 'white' and bg[2] == 'black':
                continue;
            curses.init_pair(i*8+j, fg[1], bg[1])
            pair["%s-%s" % (fg[0], bg[0])] = i*8 + j

# Print colors.
if __name__ == '__main__':
    print Color.pair
    print curses.A_BLINK
