import curses
import random

#def init():
#    stdscr = curses.initscr()
    #curses.start_color() # Permit colors.
    #curses.noecho() # Don't display typed keys.
    #curses.cbreak()  # Don't wait for enter.
    #stdscr.keypad(1) # Turn on keypad mode.
#    return stdscr
# Simple coinflip
def flip():
    if random.randint(0, 1) == 1:
        return 1
    else: return -1


# For exiting cleanly.
def gameover():
    #curses.echo()
    #curses.nocbreak()
    #stdscr.keypad(0)
    curses.endwin()

def newwin(window, x, y, startx, starty):
    win = window.subwin(y, x, starty, startx)
    return win

def main(stdscr):
    # HACK:
    term_x = 80
    term_y = 24
    curses.curs_set(0) # Make cursor invisible.

#    stdscr = init()
    from define import NW, NE, CE, SE, SW, CW
    from actor import Actor
    from player import *
    from map import Map, Terrain
    from view import MainMap, Stats, Chargen, Status, Log, View
    import hex
    from random import randint

    # HACK: INTRO SCREEN
    intro = View(stdscr, term_x, term_y, 0, 0)
    intro.x_acc = 10
    intro.line("")
    intro.line('7DRL 2012 ENTRY "HELLMOUTH" HAS BEEN TURNED INTO MEAT')
    intro.line('BASED ROGUELIKE "MEAT ARENA", WITH FABULOUS FEATURES:')
    intro.line("")
    intro.line("  * A MEAT ARENA")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * A MEAT PLAYER")
    intro.line("")
    intro.line("  * SIX DIRECTIONS OF MOVEMENT.")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * UP TO FOUR KINDS OF MEAT ENEMIES")
    intro.line("")
    intro.line("  * HEXAGONS")
    intro.line("")
    intro.line("  * A MEAT ARENA")
    intro.line("")
    intro.line("")
    intro.line("PRESS SPACE TO ENTER THE MEAT ARENA")
    intro.line("")
    intro.line("PRESS ESC TO COWARDLY LEAVE")
    while 1:
        c = stdscr.getch()
        if c == ord(' '):
            break;
        if c == 27:
            exit("COWARD.")

    # Very basic map init
    map = Map()
    map.loadmap(50, 50)

    center_x = map.width/2 - 1
    center_y = map.height/2 - 1

    # Mega hack to draw a hexagonal map
    hex_max = 25
    hex_start = 15

    walls = hex.iterator(map, center_x, center_y, hex_max, True, True, False, hex_start)
    #exit("%s" % walls)
#    terrain = Terrain()
#    exit("%s" % terrain	)
    for pos in walls:
#        print "%s,%s"%pos
        terrain = map.put(Terrain(), pos, True)
#    exit()
    for x in range(10):
        colsize = random.randint(1, 3)
        pos = (center_x + flip()*randint(4, hex_start)-colsize, center_y + flip() * randint(4,hex_start)-colsize)
        col = hex.iterator(map, pos[0], pos[1], colsize, True, True, False, 0)
        for loc in col:
            map.put(Terrain(), loc, True)       

    # A friendly @
    player = map.put(Player(), (center_x, center_y))
    map.player = player
    monsters = [MeatSlave, MeatSlave, MeatSlave, MeatSlave, MeatWorm, MeatWorm, MeatGolem, MeatHydra] 
    # Spawn enemies for it to fight
    for x in range(100):
        monster = random.choice(monsters)
        map.put(monster(), (center_x + flip()*randint(1, hex_start), center_y + flip() * randint(1,hex_start)))

    # HACK:
    mainmap_width = 45

    # Map screen init
    mainmap = MainMap(stdscr, mainmap_width, term_y, 0, 0)
    mainmap.map = map
    mainmap.player = player
    #mainmap.window.overlay(stdscr)
    mainmap.ready()
    mainmap.draw()

    status_size = 5
    status = Status(stdscr, 80-mainmap_width-status_size, status_size, mainmap_width-status_size, 0)

    #chargen = Chargen(stdscr, 62, term_y, 0, 0)
    # HACK:
    spacing = 2
    stat_height = 11
    stats = Stats(stdscr, 80-mainmap_width-spacing, stat_height, mainmap_width+spacing, 0)
    stats.player = player

    log = Log(stdscr, 80-mainmap_width-status_size, term_y-stat_height, mainmap_width+spacing, stat_height)
    map.log = log

    map.log.add("WELCOME TO THE ARENA OF MEAT")

    # DEBUG: Fill p with log entries
    #for x in range(50):
    #    map.log.add("Log Entry %s" % x)

    views = []
    views.append(mainmap)
    views.append(stats)
    views.append(status)
    views.append(log)
    #views.append(chargen)
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
            if len(map.queue) == 0:
                break;
            if player.hp <= 0:
                break;

        # DEBUG: Print currently acting.
        # Has to be here for it to work properly.
        #stdscr.addstr(19, 59, "QUEUE")
        #if map.acting is not None:
        #    stdscr.addstr(20, 59, "Curr: %s" % map.acting.name)
        #else:
        #    stdscr.addstr(20, 59, "Curr: NONE")
        #stdscr.addstr(21, 59, "Next: %s" % map.queue[0].name)
    
        if map.acting is not player:
            map.acting.act()
            continue

        # Keyin stuff for player actions
        c = stdscr.getch()
        if c == ord('q'):
            exit("MEGACOWARD")
        if c == 27: # Escape key
            exit("MEGACOWARD")
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
#        elif hasattr(chargen.selector, 'parent') is True:
#            if c == curses.KEY_RIGHT:
#                chargen.selector.next()
#            elif c == curses.KEY_LEFT:
#                chargen.selector.prev()
#            elif c == curses.KEY_ENTER or c == ord('\n'):
#                chargen.selector.choose()
#                views.remove(chargen)

        # Clear screen and tell views to draw themselves.
        stdscr.clear()
        for view in views:
            view.draw()

    # All non-component drawing is handled below.

        # DEBUG: Print current position.
        #stdscr.addstr(10, 59, "POSITION", curses.color_pair(1))
        #stdscr.addstr(11, 59, '(%s, %s)' % player.pos, curses.A_REVERSE)

        # DEBUG: Print distance from starting point.
        #stdscr.addstr(13, 59, "DIST FROM (%s, %s)" % (center_x, center_y))
        #stdscr.addstr(14, 59, "[%d]" % hex.dist(player.pos[0], player.pos[1], center_x, center_y))

        # DEBUG: Print current key.
        #stdscr.addstr(16, 59, "KEYIN")
        #if c < 256 and c > 31: # i.e., ASCII glyphs
        #    stdscr.addch(17, 59, chr(c))

        # DEBUG: Print current torso wounds.
        #stdscr.addstr(16, 59, "TORSO WOUNDS")
        #stdscr.addstr(17, 59, "%s" % player.body.locs.get("Torso").wounds)

        # Refresh the display.
        stdscr.refresh()

    # HACK: WIN SCREEN
    stdscr.clear()

    intro = View(stdscr, term_x, term_y, 0, 0)
    intro.x_acc = 10
    intro.line("")
    if player.hp > 0:
        intro.line('YOU HAVE CONQUERED THE MEAT BASED ROGUELIKE "MEAT ARENA"')
        intro.line("")
        intro.line("YOU ARE HUNGRY AFTER YOUR BATTLE AND MANAGE TO EAT YOUR WAY OUT")
        intro.line("")
        intro.line("CONGRATULATIONS!")
    else:
        intro.line('YOU HAVE BEEN SLAIN IN THE MEAT BASED ROGUELIKE "MEAT ARENA"')
        intro.line("")
        intro.line("YOU ARE USED TO FURTHER FORTIFY ITS MEAT WALLS!")
        intro.line("")
        intro.line("CONGRATULATIONS!")
    intro.line("")
    intro.line("")
    intro.line("")
    intro.line("THANKS FOR PLAYING AND MAKE SURE TO FOLLOW HELLMOUTH ON GITHUB:")
    intro.line("")
    intro.line("        https://github.com/Eronarn/Hellmouth")
    intro.line("")
    intro.line("THE REAL GAME WILL BE MUCH BETTER, I PROMISE")
    intro.line("")
    intro.line("")
    intro.line("")
    intro.line("HUGS & KISSES,")
    intro.line("")
    intro.line("    -ERONARN")
    intro.line("")
    intro.line("")
    if player.hp > 0:
        intro.line("PRESS SPACE OR ESC TO EXIT THE ARENA IN TRIUMPH")
    else:
        intro.line("PRESS SPACE OR ESC TO EXIT THE ARENA IN IGNOMINY")

    #intro.window.refresh()

    while 1:
        c = stdscr.getch()
        if c == ord(' '):
            exit("VICTORY IS YOURS.")
        if c == 27:
            exit("VICTORY IS YOURS.")

# Curses wrapper.
curses.wrapper(main)
