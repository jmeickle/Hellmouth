# Debug code that could, in theory, be imported as needed.

    # DEBUG: Generate log entries
    #for x in range(50):
    #    map.log.add("Log Entry %s" % x)


        # DEBUG: Print currently acting actor name.
        # Has to be here for it to work properly.
        #stdscr.addstr(19, 59, "QUEUE")
        #if map.acting is not None:
        #    stdscr.addstr(20, 59, "Curr: %s" % map.acting.name)
        #else:
        #    stdscr.addstr(20, 59, "Curr: NONE")
        #stdscr.addstr(21, 59, "Next: %s" % map.queue[0].name)

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

        # DEBUG: Print current inventory.
        #stdscr.addstr(16, 59, "INVENTORY")
        #i = 0
        #for appearance, item in player.inventory.items():
        #    stdscr.addstr(17+i, 59, "%s (%s)" % (appearance, len(item)))
        #    i += 1
 
        # DEBUG: Print current torso wounds.
        #stdscr.addstr(16, 59, "TORSO WOUNDS")
        #stdscr.addstr(17, 59, "%s" % player.body.locs.get("Torso").wounds)




# Handle game-related imports.
import random

from actors.actor import Actor
from dice import *
from define import *
from maps.encounter import Encounter
from key import keyin



        # Handle all player keyboard input
        keyin(stdscr, views)


    # Chargen window init
    chargen = Chargen(stdscr, TERM_X, TERM_Y)
    chargen.player = pc

