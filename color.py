import curses

class Color:
    if __name__ == '__main__':
        curses.initscr()
        curses.start_color()

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
    color_names = [x[0] for x in colors]

    #fg-bg colornames : curses colorpair
    pairs = {}

    # Must be hardcoded.
    pairs["white-black"] = 0

    # Set up all other colorpairs
    id = 1
    for i in range(8):
        for j in range(8):
            fg = colors[i%8]
            bg = colors[j%8]
            if fg[0] == 'white' and bg[0] == 'black':
                continue;
            curses.init_pair(id, fg[1], bg[1])
            pairs["%s-%s" % (fg[0], bg[0])] = id
            id += 1

# TEST: Print colors.
if __name__ == '__main__':
    print Color.pairs
    print len(Color.pairs)
