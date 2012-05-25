import curses

class Color:
    if __name__ == '__main__':
        curses.initscr()
        curses.start_color()

    # Basic color names and definitions.
    curses_colors = [
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
    colors = {}

    for x in [x[0] for x in curses_colors]:
        colors[x] = (x,)

    # Elemental colors.
    colors["meat"] = ('red', 'yellow')

    #fg-bg colornames : curses colorpair
    pairs = {}

    # Must be hardcoded.
    pairs["white-black"] = 0

    # Set up all other colorpairs
    id = 1
    for i in range(8):
        for j in range(8):
            fg = curses_colors[i%8]
            bg = curses_colors[j%8]
            if fg[0] == 'white' and bg[0] == 'black':
                continue;
            curses.init_pair(id, fg[1], bg[1])
            pairs["%s-%s" % (fg[0], bg[0])] = id
            id += 1

# TEST: Print colors.
if __name__ == '__main__':
    print Color.pairs
    print len(Color.pairs)
